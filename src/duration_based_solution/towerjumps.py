import csv
from datetime import datetime

import sys

import pandas as pd


start, end =pd.Timestamp(sys.argv[1]), pd.Timestamp(sys.argv[2])

INPUT_FILE_PATH = "TowerJumpsDataSet_CarrierRecords.csv"
OUTPUT_PATH = 'src/duration_based_solution/output.csv'
LOCATIONS_SUMMARY_PATH = 'src/duration_based_solution/location_summary.csv'
NOISE_DURATION_IN_HOURS = 0.5

def time_converter(time):
    return datetime.strptime(time, '%m/%d/%y %H:%M')


def cleanup_data(csv_reader):
    return {time_converter(row['Local Date & Time']):row['State'] for row in csv_reader if row['State'] != 'unknown' if start <= time_converter(row['Local Date & Time']) <= end}

with open(INPUT_FILE_PATH, mode='r', newline='', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    data_list = cleanup_data(csv_reader)

sorted_data_list = dict(sorted(data_list.items()))
current_location = None
start_time = None
data_grouped_by_location_and_time_diff = []

for row in sorted_data_list.items():
    timestamp, location = row
    if location != current_location:
        if current_location is not None:
            end_time = previous_timestamp
            duration = (end_time - start_time).total_seconds() / 3600  # Duration in hours
            data_grouped_by_location_and_time_diff.append((current_location, start_time, end_time, duration))
        
        # Update to new location
        current_location = location
        start_time = timestamp

    previous_timestamp = timestamp


total_durations = {}
total_duration = 0.0
    
for row in data_grouped_by_location_and_time_diff:
    if row:
        location = row[0]
        duration = float(row[3]) 

        if duration <= NOISE_DURATION_IN_HOURS:
            continue

        total_durations[location] = total_durations.get(location, 0) + duration
        total_duration += duration
            

results = {location: (total, (total / total_duration) * 100) for location, total in total_durations.items()}         
print(f'Results from {start} to {end}: {results}')


# Output the results
with open(LOCATIONS_SUMMARY_PATH, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Location", "Start Time", "End Time", "Duration (Hours)"])
    writer.writerows([(loc, start, end, f"{dur:.2f}") for loc, start, end, dur in data_grouped_by_location_and_time_diff])

highest_duration_item = max(results.items(), key=lambda item: item[1][0])
print(highest_duration_item)
with open(OUTPUT_PATH, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Interval Start","Estimated State","Confidence (%)"])
    writer.writerows([(f'{start} - {end}', highest_duration_item[0], f"{highest_duration_item[1][1]:.2f}%")])
