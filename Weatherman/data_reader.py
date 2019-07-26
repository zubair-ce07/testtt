#!/usr/bin/python3
import calendar
import csv
import glob
from weather_records import *
from weather_results import *



class WeathermanFileReader:

    filename_format = "{}**/*{}*{}*"

    def __init__(self, path):
        self.path = path

    def parse_weather_records(self,given_year, month_number):
        given_month = calendar.month_name[int(month_number)][0:3]
        files = glob.glob(WeathermanFileReader.filename_format.format(self.path,given_year,given_month))
        weather_records = []

        with open(files[0]) as data_file:
            dict_reader = csv.DictReader(data_file)
            for row in dict_reader:
                if (row["PKT"] and row["Min TemperatureC"] and row["Max TemperatureC"] and row[" Mean Humidity"] and row["Max Humidity"]):
                    daily_data = WeatherRecords(row)
                    if daily_data:
                        weather_records.append(daily_data)

        return weather_records
