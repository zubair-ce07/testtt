import csv
import re
from os import listdir
from os.path import isfile, join

from weather_day_reading import WeatherReading


class WeatherReadingsReader:

    @staticmethod
    def read_day_reading(reading):
        day_reading = WeatherReading(reading)
        return day_reading

    @staticmethod
    def validate_day_reading(reading):
        required_fields = ['Mean TemperatureC', 'Min TemperatureC', 'Max TemperatureC',
                           ' Mean Humidity', 'Max Humidity', ' Min Humidity']
        return all(reading.get(f) for f in required_fields)

    @staticmethod
    def read_file(path):
        weather_readings = []
        month_file = csv.DictReader(open(path))
        for reading in month_file:
            if WeatherReadingsReader.validate_day_reading(reading):
                weather_readings.append(WeatherReadingsReader.read_day_reading(reading))
        return weather_readings

    @staticmethod
    def get_weather_files(directory):
        return [f for f in listdir(directory) if isfile(join(directory, f))]

    @staticmethod
    def file_needs_to_be_read(file_name, year, month):
        regex = f'.*{str(year)}_{month}.txt'
        return bool(re.match(regex, file_name))

    @staticmethod
    def read_readings(dir_path, year, month='.*'):
        weather_readings = []
        file_names = WeatherReadingsReader.get_weather_files(dir_path)
        for file_name in file_names:
            if WeatherReadingsReader.file_needs_to_be_read(file_name, year, month):
                weather_readings += WeatherReadingsReader.read_file(join(dir_path, file_name))
        return weather_readings
