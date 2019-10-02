import csv
from fnmatch import fnmatch
from os import listdir

from weather_record import WeatherRecord


def read_weather_files(path):       
    weather_data = []

    for weather_record_file in listdir(path):
        if fnmatch(weather_record_file, '*.txt'):
            weather_record_file_path = f'{path}/{weather_record_file}'
            
        with open(weather_record_file_path) as weather_file:
            reader = csv.DictReader(weather_file)
            weather_data.extend([WeatherRecord(row) for row in reader if is_valid_record(row)])
                                                  
    return weather_data


def is_valid_record(weather_record):
    weather_data = [weather_record.get('Max TemperatureC'), weather_record.get(
            'Min TemperatureC'), weather_record.get('Max Humidity'), weather_record.get(
                    ' Mean Humidity'), weather_record.get('PKT') or weather_record.get('PKST')]

    return all(weather_data)
