#!/usr/bin/python3
import calendar
import csv
from glob import glob

from weather_records import WeatherRecords


def is_valid_weather_record(record):
    return all(record.get(field) for field in WeathermanFileReader.required_fields)

class WeathermanFileReader:

    filename_format = "{}**/*"
    required_fields = [
        "PKT", "Min TemperatureC", "Max TemperatureC",
        " Mean Humidity", "Max Humidity"
    ]

    def __init__(self, path):
        self.path = path
        self.weather_records = []

    def read_all_data(self):
        files = glob(WeathermanFileReader.filename_format.\
                    format(self.path))

        for file in files:
            with open(file) as data_file:
                dict_reader = csv.DictReader(data_file)
                for row in dict_reader:
                    if is_valid_weather_record(row):
                        daily_data = WeatherRecords(row)
                        if daily_data:
                            self.weather_records.append(daily_data)

    def get_weather_records(self, year, month=0):
        if month == 0:
            return [weather_record for weather_record in self.weather_records if weather_record.date.year == year]
        return [weather_record for weather_record in self.weather_records \
            if weather_record.date.year == year and weather_record.date.month == month]
