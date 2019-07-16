import csv
import math
from datetime import datetime
import calendar
from os import listdir
from os.path import isfile, join


class Parser:
    """Parser class to extract data and parse it."""

    def files_to_read(self, data_path=None, year=None, month=None):
        """This function will return the filenames that we had to read for a given month or year."""

        if year is not None:
            files = [f for f in listdir(data_path) if isfile(join(data_path, f))]
            year_files = []
            for file_name in files:
                if not file_name.startswith('.') and year in file_name:
                    year_files.append(f"{data_path}{file_name}")
            return year_files
        elif month is not None:
            month_file = []
            year_num = month.split('/')[0]
            month_num = int(month.split('/')[1])
            month_name = calendar.month_abbr[month_num]
            month_file.append(f"{data_path}Murree_weather_{year_num}_{month_name}.txt")
            return month_file

    def read_files(self, data_path=None, year=None, month=None):
        """This function will read all the weather data."""

        if year is not None:
            files_to_read = self.files_to_read(data_path=data_path, year=year)
            data = []
            for f in files_to_read:
                data.extend(self.file_parser(f))
            return data
        elif month is not None:
            file_to_read = self.files_to_read(data_path=data_path, month=month)
            data = self.file_parser(file_to_read[0])
            return data

    def file_parser(self, month_file):
        """This function will read a File in a dictionary object."""

        with open(month_file, newline='\n') as csvfile:
            reader = csv.DictReader(csvfile)
            reader = list(reader)
            for row in reader:
                if row['Max TemperatureC']:
                    row['Max TemperatureC'] = int(row['Max TemperatureC'])
                else:
                    row['Max TemperatureC'] = -math.inf
                if row['Min TemperatureC']:
                    row['Min TemperatureC'] = int(row['Min TemperatureC'])
                else:
                    row['Min TemperatureC'] = math.inf
                if row['Max Humidity']:
                    row['Max Humidity'] = int(row['Max Humidity'])
                else:
                    row['Max Humidity'] = -math.inf
                if row[' Mean Humidity']:
                    row[' Mean Humidity'] = int(row[' Mean Humidity'])
                else:
                    row[' Mean Humidity'] = math.inf
            return reader
