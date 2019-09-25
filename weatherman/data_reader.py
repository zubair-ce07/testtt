import csv
import fnmatch
import os


class DataReader:

    def __init__(self):
        self.data = {}

    @staticmethod
    def yearly_file_names(path, year):

        """ Returns list of file names for given year """

        file_names = []

        for file in os.listdir(path):
            if fnmatch.fnmatch(file, f'*_{year}_*'):
                file_names.append(path + '/' + file)

        return file_names

    @staticmethod
    def monthly_file_names(path, year, month):

        """ Returns file name for given month """

        files_names = []

        for file in os.listdir(path):
            if fnmatch.fnmatch(file, f'*_{year}_{month}.txt'):
                full_path = path + '/' + file
                files_names.append(full_path)

        return files_names

    def read_files(self, files):

        """ Reads files and returns dictionary containing required weather records """

        max_temperature = []
        min_temperature = []
        max_humidity = []
        mean_humidity = []
        max_temp_date = []
        min_temp_date = []
        max_humidity_date = []
        try:
            for file in list(files):
                with open(file) as data_file:
                    for row in csv.DictReader(data_file):
                        if row['Max TemperatureC'] != '':
                            max_temperature.append(int(row['Max TemperatureC']))
                            max_temp_date.append(row['PKT'])
                        if row['Min TemperatureC'] != '':
                            min_temperature.append(int(row['Min TemperatureC']))
                            min_temp_date.append(row['PKT'])
                        if row['Max Humidity'] != '':
                            max_humidity.append(int(row['Max Humidity']))
                            max_humidity_date.append(row['PKT'])
                        if row[' Mean Humidity'] != '':
                            mean_humidity.append(int(row[' Mean Humidity']))

            self.data['max_temperature'] = max_temperature
            self.data['min_temperature'] = min_temperature
            self.data['max_humidity'] = max_humidity
            self.data['mean_humidity'] = mean_humidity
            self.data['max_temp_date'] = max_temp_date
            self.data['min_temp_date'] = min_temp_date
            self.data['max_humidity_date'] = max_humidity_date

            return self.data

        except FileNotFoundError as fnfError:
            print(fnfError)
