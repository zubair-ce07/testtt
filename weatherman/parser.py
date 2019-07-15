import csv
from datetime import datetime
import calendar
from os import listdir
from os.path import isfile, join
from calculations import WeatherCalculator


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
            year_num = month.split('/')[0]
            month_num = int(month.split('/')[1])
            month_name = calendar.month_abbr[month_num]
            month_file = f"{data_path}Murree_weather_{year_num}_{month_name}.txt"
            return month_file

    def read_files(self, data_path=None, year=None, month=None):
        """This function will read all the weather data."""

        if year is not None:
            files_to_read = self.files_to_read(data_path=data_path, year=year)
            data = [[], [], [], [], []]
            for file_ in files_to_read:
                data = self.file_parser(file_, data)
            return data
        elif month is not None:
            data = [[], [], [], [], []]
            file_to_read = self.files_to_read(data_path=data_path, month=month)
            data = self.file_parser(file_to_read, data)
            return data

    def file_parser(self, month_file, data):
        """This function will read a File in a dictionary object."""

        with open(month_file, newline='\n') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'PKT' in reader.fieldnames:
                    data[0].append(row['PKT'])
                elif 'PKST' in reader.fieldnames:
                    data[0].append(row['PKST'])
                if row['Max TemperatureC']:
                    data[1].append(int(row['Max TemperatureC']))
                else:
                    data[1].append(None)
                if row['Min TemperatureC']:
                    data[2].append(int(row['Min TemperatureC']))
                else:
                    data[2].append(None)
                if row['Max Humidity']:
                    data[3].append(int(row['Max Humidity']))
                else:
                    data[3].append(None)
                if row[' Mean Humidity']:
                    data[4].append(int(row[' Mean Humidity']))
                else:
                    data[4].append(None)
            return data
