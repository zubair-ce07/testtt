import calendar
import csv
import fnmatch
import math
from datetime import datetime
from os import listdir
from os.path import isfile, join


class Parser:
    def __init__(self, data_path, year=None, month=None):
        self.data_path = data_path
        self.year = year
        self.month = month

    def _get_filenames(self):
        month_name = calendar.month_abbr[int(self.month)] if self.month else '*'
        filename_re = f'Murree_weather_{self.year}_{month_name}.txt'
        for file_name in listdir(self.data_path):
            if isfile(join(self.data_path, file_name)) and fnmatch.fnmatch(file_name, filename_re):
                yield join(self.data_path, file_name)

    def read_files(self):
        records = []
        for file_name in self._get_filenames():
            records.extend(self._parse_file(file_name))
        return self._clean_records(records)

    def _parse_file(self, month_file):
        with open(month_file, newline='\n') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)

    def _clean_records(self, records):
        for row in records:
            row['Max TemperatureC'] = int(row['Max TemperatureC']) if row['Max TemperatureC'] else None
            row['Min TemperatureC'] = int(row['Min TemperatureC']) if row['Min TemperatureC'] else None
            row['Max Humidity'] = int(row['Max Humidity']) if row['Max Humidity'] else None
            row[' Mean Humidity'] = int(row[' Mean Humidity']) if row[' Mean Humidity'] else None
        return records
