#!/usr/bin/python3
import calendar
import csv
import os
from datetime import datetime
from data_holder import *


filename_prefix = "Murree_weather_" #Murree_weather_2004_Aug
file_extention = ".txt"

def get_daily_selected_attributes(record,fields):
    info = {}
    for field in fields:
        if not record[field]:
            return
        else:
            if (field == temperature_fields[0]):
                info[field] = datetime.strptime(record[temperature_fields[0]], "%Y-%m-%d")
            else:
                info[field] = int(record[field])
    return info


class WeathermanFileReader:

    def __init__(self, path):
        self.path = path

    def get_monthly_data(self,given_year, month_number):
        given_month = calendar.month_name[int(month_number)][0:3]
        file_path = self.path + "/" + filename_prefix + given_year + "_" + given_month + file_extention

        attributes = []
        monthly_records = []
        avg_fields = [0,0,0]
        row_count = 0;

        if (os.path.isfile(file_path)):
            with open(file_path) as dataFile:
                dict_reader = csv.DictReader(dataFile)
                for row in dict_reader:

                    daily_data = DayWeather(row)
                    if daily_data:
                        row_count += 1;
                        monthly_records.append(daily_data)

        return monthly_records
