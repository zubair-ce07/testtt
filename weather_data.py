import os
from record import *
import csv
import calendar


class FileReader:
    def __init__(self, file_path, year, month=None):

        file_names = os.listdir(file_path)
        years = []
        self.records = []
        type(int(year))
        if month:
            month = int(month)
            month = calendar.month_abbr[month]

        for file_name in file_names:
            if year in file_name:
                if month:
                    if month in file_name:
                        years.append(file_name)
                else:
                    years.append(file_name)
        for file_name in years:
            with open(file_path + file_name) as records:
                file_reader = csv.DictReader(records)
                for row in file_reader:
                    new_record = WeatherData(
                        row['PKT'], row['Max TemperatureC'],
                        row['Min TemperatureC'], row['Max Humidity'], row[' Mean Humidity'])
                    self.records.append(new_record)