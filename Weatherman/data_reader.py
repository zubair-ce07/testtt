#!/usr/bin/python3
import calendar
import csv
from glob import glob

from weather_records import WeatherRecords


def is_valid_weather_record(record):
    return all(record.get(field) for field in WeathermanFileReader.required_fields)

class WeathermanFileReader:

    filename_format = "{}**/*{}*{}*"
    required_fields = [
        "PKT", "Min TemperatureC", "Max TemperatureC",
        " Mean Humidity", "Max Humidity"
    ]

    def __init__(self, path):
        self.path = path

    def parse_weather_records(self, given_year, month_number=0):
        month_abbr = ""
        if month_number != 0:
            month_abbr = calendar.month_abbr[month_number]
        files = glob(WeathermanFileReader.filename_format.\
                    format(self.path, given_year, month_abbr))
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
        if month_number != 0:
            return yearly_weather_records[0]
        return yearly_weather_records
