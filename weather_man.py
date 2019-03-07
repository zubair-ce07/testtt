
"""
This module generates weather report of respective directory.
It opens and reads all files present in the directory.
"""

import csv
import os
from collections import defaultdict
from datetime import datetime

from weather import Weather


class WeatherMan:

    def __init__(self, dir_path):
        self.annual_report = defaultdict(lambda: Weather())
        self.parse_data_in_directory(dir_path)

    def parse_data_in_directory(self, dir_path):
        """
        Lists through files in respective directory,
        verifies each entry as a file and opens it.

        Args:
            dir_path <str>: directory containing all data files
        """

        for filename in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, filename)):
                self.parse_file_data(os.path.join(dir_path, filename))

    def parse_file_data(self, filename):
        """
        opens file and parses file data to perform calculation for weather report.

        Args:
            filename <str> : file name to be opened

        """

        try:
            with open(filename) as file_data:

                filtered_file_data = self.filter_invalid_data(file_data)
                file_data = csv.DictReader(filtered_file_data, delimiter=',')
                self.calculate_weather_data(file_data)

        except IOError:
            print 'Could not read file: ', filename

    @staticmethod
    def filter_invalid_data(file_data):
        """
        Filters line of a file, yeilds respective line if it's not empty or commented

        Args:
            file_data <arr[str]> : file data
        """

        for line in file_data:
            if not line.isspace() and not line.startswith('<!--'):
                yield line

    def calculate_weather_data(self, file_data):
        """calculates weather data by looping through file data.

        Args:
            file_data <dict> : dictionary for each line of a file
        """
        for row_data in file_data:

            weather_data = Weather(**row_data)
            year = datetime.strptime(weather_data.date, '%Y-%m-%d').year
            annual_data = self.annual_report[year]

            if not annual_data.max_temp or weather_data.max_temp > annual_data.max_temp:
                self.annual_report[year].date = weather_data.date
                self.annual_report[year].max_temp = weather_data.max_temp

            if not annual_data.min_temp or weather_data.min_temp < annual_data.min_temp:
                self.annual_report[year].min_temp = weather_data.min_temp

            if not annual_data.max_humidity or weather_data.max_humidity > annual_data.max_humidity:
                self.annual_report[year].max_humidity = weather_data.max_humidity

            if not annual_data.min_humidity or weather_data.min_humidity < annual_data.min_humidity:
                self.annual_report[year].min_humidity = weather_data.min_humidity

    def print_annual_weather_report(self):
        """prints annual weather data in tabular form. """

        print('-'*80)
        print('{:<10s}{:<10s}{:>12s}{:>18s}{:>20s}'.format(
            'Year', 'MAX Temp', 'MIN Temp', 'MAX Humidity', 'MIN Humidity'
        ))
        print('-'*80)

        for key, value in sorted(self.annual_report.items()):
            print('{:<10d}{:^10s}{:^12s}{:^18s}{:^20s}'.format(
                key, str(value.max_temp), str(value.min_temp),
                str(value.max_humidity), str(value.min_humidity)
            ))

    def print_annual_max_temperature_weather_report(self):
        """prints annual maximum temperature weather data in tabular form. """

        print('-'*40)
        print('{:<10s}{:^10s}{:>10s}'.format('Year', 'Date', 'Temp'))
        print('-'*40)

        for key, value in sorted(self.annual_report.items()):
            print('{:<10d}{:<10s}{:>8s}'.format(
                key, value.date, str(value.max_temp)
            ))
