""" Parser for file """
import os
from model_classes import DayRecord
from datetime import datetime
import csv

from constants import FILE_MONTHS

class FileHandler:
    def __init__(self, path):
        self.path_to_files = path


    def get_path_file(self, year, month):
        """Return path to the required file given the year and month"""
        month = month.capitalize()
        file_path = f"{self.path_to_files}/Murree_weather_{year}_{month}.txt"
        return file_path


    def get_day_record(self,row):
        """ get single line record and return class object"""
        day_record = DayRecord(
            date = datetime.strptime(row.get("PKT"), '%Y-%m-%d'),
            max_temperature = row.get("Max TemperatureC"),
            mean_temperature = row.get("Mean TemperatureC"),
            min_temperature = row.get("Min TemperatureC"),
            max_humidity = row.get("Max Humidity"),
            mean_humidity = row.get(" Mean Humidity"),
            min_humidity = row.get(" Min Humidity")
        )
        return day_record


    def get_month_list(self, month, year, rec_list):
        """ get list and append month data to that list"""
        file_name = self.get_path_file(year, month)
        
        if os.path.isfile( file_name):    
            with open(file_name, mode='r') as reader:
                csv_reader = csv.DictReader(reader, delimiter=',')
                for row in csv_reader:
                    day_record = self.get_day_record(row)
                    rec_list.append(day_record)

    def get_year_list(self, year):
        """ get list and append month data to that list """
        year_record_list = []
        for month in FILE_MONTHS:
            month = FILE_MONTHS.get(month)
            self.get_month_list(month,year,year_record_list)
        return year_record_list
