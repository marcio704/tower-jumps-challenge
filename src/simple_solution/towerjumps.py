from typing import Dict, Iterable
import pandas as pd

from src.utils import parse_input

INPUT_FILE_PATH = "TowerJumpsDataSet_CarrierRecords.csv"
OUTPUT_CSV_PATH = "src/simple_solution/output.csv"
HEATMAP_OUTPUT_PATH = "heatmap.html"
CENTER_OF_NEW_YORK_STATE = (40.7128, -74.0060)

def group_locations_by_datetime_intervals(data: pd.DataFrame, interval_minutes:int = 15) -> pd.DataFrame:
    data['Interval Start'] = data['Local Date & Time'].dt.floor(f'{interval_minutes}T')
    return data.groupby('Interval Start')

def estimate_state(grouped_dataset: pd.DataFrame) -> Iterable[Dict]:
    for interval, group in grouped_dataset:
        state_counts = group['State'].value_counts()
        total_pings = len(group)
        top_state = state_counts.idxmax()
        confidence = state_counts.max() / total_pings * 100
        
        yield {
            "Interval Start": interval,
            "Estimated State": top_state,
            "Confidence (%)": round(confidence, 2),
        }

def run(input_file:str = INPUT_FILE_PATH, generate_csv: bool = True) -> list:
    dataset = parse_input(input_file)
    grouped_dataset = group_locations_by_datetime_intervals(dataset)
    results = pd.DataFrame(estimate_state(grouped_dataset))

    if generate_csv:
        results.to_csv(OUTPUT_CSV_PATH, index=False)
        print(f"Results saved to {OUTPUT_CSV_PATH}")
    else:
        return results.to_csv(None, header=False, index=False).split('\n')[0]


if __name__ == "__main__":
    run()
