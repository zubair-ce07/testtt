import fnmatch
import os
from datetime import datetime

import sys


class FileReader:

    @staticmethod
    def get_month_file_name(dir, year_month):
        date  = datetime.strptime(year_month, "%Y/%m")
        formatted_date = date.strftime("%Y_%b")
        filename = os.path.join(dir, 'Murree_weather_' + formatted_date + '.txt')
        return [filename,]

    @staticmethod
    def get_filenames_from_dir_for_year(dir, year):
        filenames = []
        for file in os.listdir(dir):
            if fnmatch.fnmatch(file, 'Murree_weather_' + year + '_*.txt'):
                filename = os.path.join(dir, file)
                filenames.append(filename)
        return filenames

    def read_files(self, filenames):
        filesdata = {}
        for filename in filenames:
            filedata = open(filename, 'rU').readlines()
            filesdata[filename] = filedata
        return filesdata

    def read_files_from_path(self, dir, year):
        try:
            if "/" in year:
                filenames = self.get_month_file_name(dir, year)
            else:
                filenames = self.get_filenames_from_dir_for_year(dir, year)
            filesdata = self.read_files(filenames)
            return filesdata
        except OSError:
            sys.stderr.write("Unable to locate directory\n")
            sys.exit(1)
