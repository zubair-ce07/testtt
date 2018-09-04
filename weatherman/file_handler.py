import os
import re
from datetime import datetime
import csv


class FileHandler:
    def get_file_names(self, year, month):
        """ return files from dir according to month and year"""
        selected_files = []
        files = os.listdir(self.path_to_files)
        if not month:
            regex = re.compile(r'^Murree_weather_' + year)
        else:
            month_str = datetime.strptime(month, '%m').strftime('%b')
            regex = re.compile(r'^Murree_weather_' +
                               year + "_" + month_str.capitalize())
        selected_files = list(filter(regex.search, files))
        return selected_files

    def get_list(self, filenames_list):
        """return list of data from files in filenames_list"""
        list = []
        for file_name in filenames_list:
            file_name = f"{self.path_to_files}/{file_name}"
            with open(file_name, mode='r') as reader:
                csv_reader = csv.DictReader(reader, delimiter=',')
                for row in csv_reader:
                    list.append(row)
        return list

    def __init__(self, path):
        self.path_to_files = path
