import csv
import math
from datetime import datetime
import calendar
from os import listdir
from os.path import isfile, join
import fnmatch


class Parser:
    def __init__(self, data_path, input_data):
        self.data_path = data_path
        self.input_data = input_data

    def _files_to_read(self):
        regex = ""
        if '/' in self.input_data:
            year, month = self.input_data.split('/')
            month_name = calendar.month_abbr[int(month)]
            regex = f'Murree_weather_{year}_{month_name}.txt'
        else:
            regex = f'Murree_weather_{self.input_data}_*.txt'
        files = [f for f in listdir(self.data_path) if isfile(join(self.data_path, f))]
        for f in files:
            if fnmatch.fnmatch(f, regex):
                yield join(self.data_path, f)

    def read_files(self):
        data = []
        for f in self._files_to_read():
            data.extend(self._file_parser(f))
        return data

    def _file_parser(self, month_file):
        with open(month_file, newline='\n') as csvfile:
            reader = csv.DictReader(csvfile)
            reader = list(reader)
            reader = self._data_cleaner(reader)
            return reader

    def _data_cleaner(self, data):
        for row in data:
            row['Max TemperatureC'] = int(row['Max TemperatureC']) if row['Max TemperatureC'] else None
            row['Min TemperatureC'] = int(row['Min TemperatureC']) if row['Min TemperatureC'] else None
            row['Max Humidity'] = int(row['Max Humidity']) if row['Max Humidity'] else None
            row[' Mean Humidity'] = int(row[' Mean Humidity']) if row[' Mean Humidity'] else None
        return data
