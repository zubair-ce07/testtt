import calendar
import csv
from datetime import datetime
import fnmatch
import math
from os import listdir
from os.path import isfile, join


class Parser:
    def __init__(self, data_path, year=None, month=None):
        self.data_path = data_path
        self.year = year
        self.month = month

    def _files_to_read(self):
        regex = ""
        if self.year and self.month:
            month_name = calendar.month_abbr[int(self.month)]
            regex = f'Murree_weather_{self.year}_{month_name}.txt'
        else:
            regex = f'Murree_weather_{self.year}_*.txt'
        file_names = [f for f in listdir(self.data_path) if isfile(join(self.data_path, f))]
        for file_name in file_names:
            if fnmatch.fnmatch(file_name, regex):
                yield join(self.data_path, file_name)

    def read_files(self):
        data = []
        for file_name in self._files_to_read():
            data.extend(self._file_parser(file_name))
        data = self._data_cleaner(data)
        return data

    def _file_parser(self, month_file):
        with open(month_file, newline='\n') as csvfile:
            reader = csv.DictReader(csvfile)
            reader = list(reader)
            return reader

    def _data_cleaner(self, data):
        for row in data:
            row['Max TemperatureC'] = int(row['Max TemperatureC']) if row['Max TemperatureC'] else None
            row['Min TemperatureC'] = int(row['Min TemperatureC']) if row['Min TemperatureC'] else None
            row['Max Humidity'] = int(row['Max Humidity']) if row['Max Humidity'] else None
            row[' Mean Humidity'] = int(row[' Mean Humidity']) if row[' Mean Humidity'] else None
        return data
