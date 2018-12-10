import glob as gb
import csv
from weather import WeatherRecord
from datetime import datetime


def data_parser(path):
    path = f'{path}/*.txt'
    weather_reading = []
    for f in gb.glob(path):
        with open(f) as weather_file:
            reader = csv.DictReader(weather_file)
            for reading in reader:
                weather_record(weather_reading, reading)

    return weather_reading


def weather_record(weather_reading, reading):
    reading = {k.strip(): v for k, v in reading.items()}
    date = reading.get('PKST', reading.get('PKT'))
    date = datetime.strptime(date, '%Y-%m-%d')

    max_temp = reading.get('Max TemperatureC')
    if not max_temp:
        return

    low_temp = reading.get('Min TemperatureC')
    if not low_temp:
        return

    max_humid = reading.get('Max Humidity')
    if not max_humid:
        return

    mean_humid = reading.get('Mean Humidity')
    if not mean_humid:
        return

    weather_reading.append(WeatherRecord(date, max_temp, low_temp, max_humid, mean_humid))
