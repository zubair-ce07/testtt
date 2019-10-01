import csv
from fnmatch import fnmatch
from os import listdir

from weather_record import WeatherRecord


def read_weather_files(path):    
    weather_files = []
    weather_data = []

    for csv_file in listdir(path):
        if fnmatch(csv_file, '*.txt'):
            full_path = f'{path}/{csv_file}'
            weather_files.append(full_path)

    for weather_file in weather_files:
        with open(weather_file) as weather_file:
            reader = csv.DictReader(weather_file)
            weather_data.extend([WeatherRecord(row) for row in reader if is_valid_record(row)])
                                                  
    return weather_data


def is_valid_record(weather_record):
    weather_data = [weather_record.get('Max TemperatureC'), weather_record.get(
            'Min TemperatureC'), weather_record.get('Max Humidity'), weather_record.get(
                    ' Mean Humidity'), weather_record.get('PKT') or weather_record.get('PKST')]

    return all(weather_data)
