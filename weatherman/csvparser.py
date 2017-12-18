import calendar
import csv
import fnmatch
import os

from datarow import DataSetRow


class CsvParser:
    """Collect data-set from CSV files"""
    def __init__(self, files_dir, year, month=None):
        self.files_dir = files_dir
        self.year = year
        self.month = calendar.month_abbr[int(month)]

        self.csv_files = []
        self.data_set = []
        self.collect_data_set()

    def find_files(self):
        """create list of files from given directory"""
        if self.month:
            pattern = '*{0}_{1}*'.format(self.year, self.month)
        else:
            pattern = '*{0}_*'.format(self.year)
        self.csv_files = list(fnmatch.filter(os.listdir(self.files_dir), pattern))
        if self.csv_files:
            raise ValueError('No files Found for given date')

    def collect_data_set(self):
        """create data-set from required files"""
        self.find_files()
        for file in self.csv_files:
            with open(self.files_dir + file, newline='') as csv_file:
                dict_records = csv.DictReader(csv_file)
                for dict_row in dict_records:
                    data_set_row = DataSetRow(dict_row['PKT'],
                                              dict_row['Max TemperatureC'],
                                              dict_row['Min TemperatureC'],
                                              dict_row['Max Humidity'],
                                              dict_row[' Mean Humidity']
                                              )
                    self.data_set.append(data_set_row)

