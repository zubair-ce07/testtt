import csv
import calendar
import datetime
from os import listdir
from os.path import isfile, join

from record import Record


class ParsingFiles:
    def __init__(self, path, argument_list):
        self.path = path
        self.argument_list = argument_list
        self.all_files_names = self.get_all_files_names()

    def get_all_files_names(self):
        return [file_name for file_name in listdir(self.path) for arg in self.argument_list
                if isfile(join(self.path, file_name)) and arg in file_name]

    def reading_files(self):
        all_weather_readings = {}
        for file_name in self.all_files_names:
            with open(''.join([self.path, file_name]), 'r') as in_file:
                file_reader = csv.DictReader(in_file)
                for line in file_reader:
                    date = line.get('PKT', line.get('PKST'))
                    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                    record = Record(line)
                    date_key = "{}_{}_{}".format(date.year, calendar.month_abbr[date.month], date.day)
                    all_weather_readings[date_key] = record

        return all_weather_readings

