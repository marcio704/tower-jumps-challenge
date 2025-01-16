from typing import Dict, Iterable
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import nearest_points

from src.utils import parse_input, group_locations_by_datetime_intervals


INPUT_FILE_PATH = "TowerJumpsDataSet_CarrierRecords.csv"
STATE_BOUNDARIES_PATH = "src/accurate_solution/us-states-borders.geojson"
OUTPUT_CSV_PATH = "src/accurate_solution/output.csv"
UNKNOWN_STATE = "Unknown"
MAX_DISTANCE = 1000  # Maximum distance in meters to normalize confidence (adjustable)


def estimate_state_by_avg_point_distance_to_border(grouped_dataset: pd.DataFrame, state_boundaries: gpd.GeoDataFrame) -> Iterable[Dict]:
    for interval, group in grouped_dataset:
        avg_lat = group['Latitude'].mean()
        avg_lon = group['Longitude'].mean()
        avg_point = Point(avg_lon, avg_lat)
        avg_point_gdf = gpd.GeoDataFrame(geometry=[avg_point], crs="EPSG:4326").to_crs(epsg=3857)
        avg_point_projected = avg_point_gdf.iloc[0].geometry
        state_boundaries = state_boundaries.to_crs(epsg=3857)
        
        # Find the state containing the average point
        containing_state = state_boundaries[state_boundaries.contains(avg_point_projected)]
        if containing_state.empty:
            estimated_state = UNKNOWN_STATE
            confidence = 0.0
        else:
            state_row = containing_state.iloc[0]
            estimated_state = state_row['name']
            
            # Calculate the distance to the nearest border
            state_geometry = state_row['geometry']
            nearest_border_point = nearest_points(state_geometry.boundary, avg_point_projected)[0]
            avg_point_distance_to_border = avg_point_projected.distance(nearest_border_point)

            # Normalize confidence: closer to border → lower confidence
            confidence = min(avg_point_distance_to_border / MAX_DISTANCE, 1.0) * 100.0
        
        yield {
            "Interval Start": interval,
            "Estimated State": estimated_state,
            "Confidence (%)": min(round(confidence, 2), 100.0),
        }
        
def run(input_file:str = INPUT_FILE_PATH, generate_csv: bool = True) -> list:
    dataset = parse_input(input_file)
    grouped_dataset = group_locations_by_datetime_intervals(dataset)
    
    state_boundaries = gpd.read_file(STATE_BOUNDARIES_PATH)  # Downloaded from https://www.kaggle.com/datasets/pompelmo/usa-states-geojson/data
    results = pd.DataFrame(estimate_state_by_avg_point_distance_to_border(grouped_dataset, state_boundaries))
    
    if generate_csv:
        results.to_csv(OUTPUT_CSV_PATH, index=False)
        print(f"Results saved to {OUTPUT_CSV_PATH}")
    else:
        return results.to_csv(None, header=False, index=False).split('\n')[0]

if __name__ == "__main__":
    run()
