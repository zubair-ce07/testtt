#!/usr/bin/python3
import calendar
import csv
from glob import glob

from weather_records import WeatherRecords


def is_valid_weather_record(record):
    for field in WeathermanFileReader.required_fields:
        if (not field in record) or (not record[field]):
            return False
    return True

class WeathermanFileReader:

    filename_format = "{}**/*{}*{}*"
    required_fields = [
        "PKT", "Min TemperatureC", "Max TemperatureC",
        " Mean Humidity", "Max Humidity"
    ]

    def __init__(self, path):
        self.path = path

    def parse_weather_records(self, given_year, month_number):
        given_month = calendar.month_name[int(month_number)][0:3]
        files = glob(WeathermanFileReader.filename_format.\
                    format(self.path, given_year, given_month))
        weather_records = []

        with open(files[0]) as data_file:
            dict_reader = csv.DictReader(data_file)
            for row in dict_reader:
                if is_valid_weather_record(row):
                    daily_data = WeatherRecords(row)
                    if daily_data:
                        weather_records.append(daily_data)

        return weather_records
