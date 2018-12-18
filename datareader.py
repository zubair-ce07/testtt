import glob as gb
import csv

from weatherman_data_structure import WeatherRecord


def data_parser(path):
    weather_reading = []

    for f in gb.glob(f'{path}/*.txt'):
        with open(f) as weather_file:
            reader = csv.DictReader(weather_file)
            weather_reading += [WeatherRecord(record) for record in reader if is_valid_record(record)]

    return weather_reading


def is_valid_record(record):
    req_fields = ['Max TemperatureC', 'Min TemperatureC', 'Max Humidity', ' Mean Humidity']
    return all([record[f] for f in req_fields] + [record.get('PKST', record.get('PKT'))])
