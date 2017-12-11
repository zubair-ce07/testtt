import calendar
import csv
import fnmatch
import os

from datarow import DataSetRow


class CsvParser:
    """Collect data-set from CSV files"""
    def __init__(self, files_dir, year, month=0):
        if os.path.isdir(files_dir):
            self.files_dir = files_dir
        else:
            raise FileNotFoundError('The directory doesn\'t exist')

        try:
            self.year = int(year)
        except:
            raise ValueError('Enter year in YYYY format')

        self.month = None
        if month:
            try:
                month = int(month)
            except:
                raise ValueError('Enter month in MM format')
            if month in range(1, len(calendar.month_name)):
                self.month = calendar.month_abbr[int(month)]
            else:
                raise ValueError('Month number not valid')

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

    def collect_data_set(self):
        """create data-set from required files"""
        self.find_files()
        if self.csv_files:
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
        else:
            raise ValueError('No files Found for given date')
