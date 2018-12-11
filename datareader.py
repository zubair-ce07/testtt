import glob as gb
import csv
from weather import WeatherRecord


def data_parser(path):
    weather_reading = []

    for f in gb.glob(f'{path}/*.txt'):
        with open(f) as weather_file:
            reader = csv.DictReader(weather_file)
            weather_reading += [WeatherRecord(record) for record in reader if valid_record(record)]

    return weather_reading


def valid_record(record):
    date = record.get('PKST', record.get('PKT'))
    mean_humid = record[' Mean Humidity']
    return all([date, record['Max TemperatureC'], record['Min TemperatureC'], record['Max Humidity'], mean_humid])
