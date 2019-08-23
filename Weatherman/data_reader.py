#!/usr/bin/python3
import calendar
import csv
from glob import glob

from weather_records import WeatherRecords

class WeathermanFileReader:

    filename_format = "{}**/*"
    required_fields = [
        "PKT", "Min TemperatureC", "Max TemperatureC",
        " Mean Humidity", "Max Humidity"
    ]

    def __init__(self, path):
        self.path = path
        self.weather_records = []

    def is_valid_weather_record(self, record):
        return all(record.get(field) for field in WeathermanFileReader.required_fields)

    def read_all_data(self):
        files = glob(WeathermanFileReader.filename_format.format(self.path))

        for file_path in files:
            with open(file_path) as data_file:
                for row in csv.DictReader(data_file):
                    if self.is_valid_weather_record(row):
                        self.weather_records.append(WeatherRecords(row))

    def filter_weather_records(self, year, month=0):
        return [weather_record for weather_record in self.weather_records \
            if weather_record.date.year == year and (weather_record.date.month == month or month == 0)]
