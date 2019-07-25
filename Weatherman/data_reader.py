#!/usr/bin/python3
import calendar
import csv
import os
from datetime import datetime
import glob
from weather_records import *
from weather_results import *

filename_format = "{}**/*{}*{}*"

class WeathermanFileReader:

    def __init__(self, path):
        self.path = path

    def get_monthly_data(self,given_year, month_number):
        given_month = calendar.month_name[int(month_number)][0:3]
        files = glob.glob(filename_format.format(self.path,given_year,given_month))
        monthly_records = []

        if (files):
            with open(files[0]) as data_file:
                dict_reader = csv.DictReader(data_file)
                for row in dict_reader:
                    if (row["PKT"] and row["Min TemperatureC"] and row["Max TemperatureC"] and row[" Mean Humidity"] and row["Max Humidity"]):
                        daily_data = WeatherRecords(row)
                        if daily_data:
                            monthly_records.append(daily_data)

        return monthly_records
