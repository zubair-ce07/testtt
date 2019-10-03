import csv
from fnmatch import fnmatch
from os import listdir

from weather_record import WeatherRecord


def read_weather_files(path):       
    weather_records = []

    for weather_record_file in listdir(path):
        if fnmatch(weather_record_file, '*.txt'):
            weather_record_file_path = f'{path}/{weather_record_file}'
            
        with open(weather_record_file_path) as weather_file:
            reader = csv.DictReader(weather_file)
            weather_records.extend([WeatherRecord(row) for row in reader if is_valid_record(row)])
                                                  
    return weather_records


def is_valid_record(weather_record):
    required_fields = ['Max TemperatureC', 'Min TemperatureC', 'Max Humidity', ' Mean Humidity']
    weather_records = [weather_record.get(column) for column in required_fields] \
                    + [weather_record.get('PKT') or weather_record.get('PKST')]
    
    return all(weather_records)
