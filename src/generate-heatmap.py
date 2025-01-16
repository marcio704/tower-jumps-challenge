import sys
import pandas as pd
import folium
from folium.plugins import HeatMap

from src.utils import parse_input

start_date = sys.argv[1] if len(sys.argv) > 1 else None
end_date = sys.argv[2] if len(sys.argv) > 1 else None

DATA_FILE_PATH = "TowerJumpsDataSet_CarrierRecords.csv"
OUTPUT_CSV_PATH = "simple-solution/output.csv"
HEATMAP_OUTPUT_PATH = "heatmap.html"
CENTER_OF_NEW_YORK_STATE = (40.7128, -74.0060)


def create_heatmap(data: pd.DataFrame, map_center=CENTER_OF_NEW_YORK_STATE, zoom_start=9, map_output=HEATMAP_OUTPUT_PATH):
    map = folium.Map(location=map_center, zoom_start=zoom_start)
    heat_data = data[['Latitude', 'Longitude']].values.tolist()
    HeatMap(heat_data, radius=10, blur=15, max_zoom=1).add_to(map).save(map_output)

def run() -> None:
    inputs = [DATA_FILE_PATH, start_date, end_date] if start_date and end_date else [DATA_FILE_PATH]
    dataset = parse_input(*inputs)
    create_heatmap(dataset)

if __name__ == "__main__":
    run()
