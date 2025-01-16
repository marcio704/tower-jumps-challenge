import pandas as pd


def parse_input(file_path: str, start_date:str = None, end_end:str = None) -> pd.DataFrame:
    dataset = pd.read_csv(file_path, delimiter=",")
    dataset.columns = dataset.columns.str.strip()

    dataset = remove_empty_rows(dataset)
    dataset = format_dates(dataset)
    
    if start_date and end_end:
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_end)
        dataset = dataset[(dataset['Local Date & Time'] >= start_date) & (dataset['Local Date & Time'] <= end_date)]
    
    return dataset.sort_values(by='Local Date & Time')

def remove_empty_rows(dataset: pd.DataFrame) -> pd.DataFrame:
    return dataset[(dataset['State'] != 'unknown') & (dataset['Latitude'] != 0) & (dataset['Longitude'] != 0)]

def format_dates(dataset: pd.DataFrame) -> pd.DataFrame:
    dataset['Local Date & Time'] = pd.to_datetime(dataset['Local Date & Time'], format='%m/%d/%y %H:%M')
    return dataset
