import csv
from fnmatch import fnmatch
from os import listdir

from weather_record import WeatherRecord


def read_file_names(path, year_month):
    files_names = []
    year = year_month.get('year') if isinstance(year_month, dict) else year_month
    month = year_month.get('month') if isinstance(year_month, dict) else '*'
    
    for weather_file in listdir(path):
        if fnmatch(weather_file, f'*_{year}_{month}.txt'):
            full_path = f'{path}/{weather_file}'
            files_names.append(full_path)

    return files_names


def read_files(weather_files):
    weather_data = []
                 
    for weather_file in weather_files:
        with open(weather_file) as weather_file:
            reader = csv.DictReader(weather_file)
            weather_data.extend([WeatherRecord(row) for row in reader])
                                                  
    return weather_data
