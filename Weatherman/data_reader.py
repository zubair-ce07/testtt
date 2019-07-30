#!/usr/bin/python3
import calendar
import csv
from glob import glob

from weather_records import WeatherRecords


def is_valid_weather_record(record):
    for field in WeathermanFileReader.required_fields:
        if not record.get(field):
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

    def parse_weather_records(self, given_year, month_number=""):
        if month_number != "":
            month_number = calendar.month_abbr[int(month_number)]
        files = glob(WeathermanFileReader.filename_format.\
                    format(self.path, given_year, month_number))
        yearly_weather_records = []

        for file in files:
            monthly_weather_records = []
            with open(file) as data_file:
                dict_reader = csv.DictReader(data_file)
                for row in dict_reader:
                    if is_valid_weather_record(row):
                        daily_data = WeatherRecords(row)
                        if daily_data:
                            monthly_weather_records.append(daily_data)
            yearly_weather_records.append(monthly_weather_records)
        if month_number != "":
            return yearly_weather_records[0]
        return yearly_weather_records
