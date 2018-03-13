"""
Class and methods for weatherman task
Pylint Score: 10.00
"""

import csv
from functions import get_date, get_dates, get_file, get_files
from colored import fg, attr


class WeatherClass:
    """Weather data class"""

    def __init__(self):
        """Constructor method"""
        self.max_temp = 0
        self.min_temp = 0
        self.max_humid = 0
        self.max_temp_dates = []
        self.min_temp_dates = []
        self.max_humid_dates = []
        self.data = {
            'PKT': [],
            'MaxTemp': [],
            'MinTemp': [],
            'MeanHumid': [],
            'MaxHumid': []
        }

    def read_data(self, args, files):
        """Method to read the required data from files"""
        for file in files:
            path = '{}/{}'.format(args.directory, file)

            with open(path, 'r') as read_file:
                reader = csv.DictReader(read_file)
                if not reader.fieldnames:
                    reader = csv.DictReader(read_file)

                for i, header in enumerate(reader.fieldnames):
                    if header.find('PKT') != -1 or header.find('PKST') != -1:
                        reader.fieldnames[i] = 'PKT'
                    if header.find('Max TemperatureC') != -1:
                        reader.fieldnames[i] = 'Max TemperatureC'
                    if header.find('Min TemperatureC') != -1:
                        reader.fieldnames[i] = 'Min TemperatureC'
                    if header.find('Mean Humidity') != -1:
                        reader.fieldnames[i] = 'Mean Humidity'
                    if header.find('Max Humidity') != -1:
                        reader.fieldnames[i] = 'Max Humidity'

                self.get_data(reader)

    def get_data(self, reader):
        """Method ro read data"""
        for row in reader:
            if row['PKT'] and row['Max TemperatureC']:
                self.data['PKT'].append(row['PKT'])
            if row['Max TemperatureC']:
                self.data['MaxTemp'].append(int(row['Max TemperatureC']))
            if row['Min TemperatureC']:
                self.data['MinTemp'].append(int(row['Min TemperatureC']))
            if row['Mean Humidity']:
                self.data['MeanHumid'].append(int(row['Mean Humidity']))
            if row['Max Humidity']:
                self.data['MaxHumid'].append(int(row['Max Humidity']))

    def peak_days(self, args):
        """Method to show the peak days of year"""
        files = get_files(args)

        if files:
            self.read_data(args, files)

            self.max_temp = max(self.data['MaxTemp'])
            self.min_temp = min(self.data['MinTemp'])
            self.max_humid = max(self.data['MaxHumid'])

            for index, item in enumerate(self.data['MaxTemp']):
                if item == self.max_temp:
                    self.max_temp_dates.append(self.data['PKT'][index])
            for index, item in enumerate(self.data['MinTemp']):
                if item == self.min_temp:
                    self.min_temp_dates.append(self.data['PKT'][index])
            for index, item in enumerate(self.data['MaxHumid']):
                if item == self.max_humid:
                    self.max_humid_dates.append(self.data['PKT'][index])

            print('Year {}'.format(args.year))
            print('Highest: {}C on {}'.format(self.max_temp, get_dates(self.max_temp_dates)))
            print('Lowest: {}C on {}'.format(self.min_temp, get_dates(self.min_temp_dates)))
            print('Humid: {}% on {}'.format(self.max_humid, get_dates(self.max_humid_dates)))

        else:
            print('No data found for given year')
            print('Year value range: 1996 - 2011')

    def calculate_averages(self, args):
        """Method to show averages of month"""
        file = get_file(args)

        if file:
            self.read_data(args, file)

            avg_max_temp = round(sum(self.data['MaxTemp']) / len(self.data['MaxTemp']))
            avg_min_temp = round(sum(self.data['MinTemp']) / len(self.data['MinTemp']))
            avg_mean_humid = round(sum(self.data['MeanHumid']) / len(self.data['MeanHumid']))

            print('Highest Average: {}C'.format(avg_max_temp))
            print('Lowest Average: {}C'.format(avg_min_temp))
            print('Average Humidity: {}%'.format(avg_mean_humid))

        else:
            print('No data found for given year and month')
            print('Year/Month value range: 1996/12 - 2011/12')

    def make_graph(self, args):
        """Method to display daily weather graph"""
        file = get_file(args)

        if file:
            self.read_data(args, file)

            for index, item in enumerate(self.data['PKT']):
                day = get_date(item)[1]

                max_temp = self.data['MaxTemp'][index]
                min_temp = self.data['MinTemp'][index]
                min_temp_bar = '{}'.format('+' * int(min_temp))
                min_temp_bar = '{}{}{}'.format(fg('light_blue'), min_temp_bar, attr('reset'))
                max_temp_bar = '{}'.format('+' * int(max_temp))
                max_temp_bar = '{}{}{}'.format(fg('red'), max_temp_bar, attr('reset'))

                print('{} {}{} {}C - {}C'.format(day, min_temp_bar, max_temp_bar,
                                                 min_temp, max_temp))

        else:
            print('No data found for given year and month')
            print('Year/Month value range: 1996/12 - 2011/12')
