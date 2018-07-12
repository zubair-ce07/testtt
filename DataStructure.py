from calculate import *
from datetime import datetime

import csv
import os
import fnmatch


class WeatherReport:
    def __init__(self):
        self.readings = list()

    def file_read(self, dir_name, year, month):
        for file_path in os.listdir(dir_name):
            if fnmatch.fnmatch(file_path,
                               'Murree_weather_{}_{}.txt'.format(year, month)):
                with open(dir_name + file_path, 'r') as csv_file:
                        reader = csv.DictReader(csv_file)
                        self.parser(reader)

    def parser(self, reader):
        for row in reader:
            if row:
                dt = Data(row)
                self.readings.append(dt)

    def print_reading(self):
        for r in self.readings:
            print(r.max_temperature)

    def yearly_report(self):
        obj_max_temp = get_max_temp(self.readings)
        month_max_temp = datetime.strptime(obj_max_temp.date,
                                           "%Y-%m-%d").strftime("%b")
        day_max_temp = datetime.strptime(obj_max_temp.date,
                                         "%Y-%m-%d").strftime("%d")

        print('Highest: {}C on {} {}'.format(obj_max_temp.max_temperature,
                                             month_max_temp,
                                             day_max_temp))

        obj_min_temp = get_min_temp(self.readings)
        month_min_temp = datetime.strptime(obj_min_temp.date,
                                           "%Y-%m-%d").strftime("%b")
        day_min_temp = datetime.strptime(obj_min_temp.date,
                                         "%Y-%m-%d").strftime("%d")

        print('Lowest: {}C on {} {}'.format(obj_min_temp.min_temperature,
                                            month_min_temp,
                                            day_min_temp))

        obj_max_hum = get_max_hum(self.readings)
        month_max_hum = datetime.strptime(obj_max_hum.date,
                                          "%Y-%m-%d").strftime("%b")
        day_max_hum = datetime.strptime(obj_max_hum.date,
                                        "%Y-%m-%d").strftime("%d")

        print('Highest: {}% on {} {}'.format(obj_max_hum.max_humidity,
                                             month_max_hum,
                                             day_max_hum))
        print('')

    def monthly_report(self):
        avg_max_temp = get_avg_max_temp(self.readings)
        avg_min_temp = get_avg_min_temp(self.readings)
        avg_mean_hum = get_avg_mean_hum(self.readings)

        print('Highest Average: {}C'.format(round(avg_max_temp)))
        print('Lowest Average: {}C'.format(round(avg_min_temp)))
        print('Average Mean Humidity: {}%'.format(round(avg_mean_hum)))
        print('')

    def daily_report(self):
        for index, day in enumerate(self.readings):

            if day.min_temperature is not None or day.max_temperature is not \
                    None:
                    print(str(index).zfill(2), end=' ')

            if day.min_temperature is not None:
                print('\033[1;34m', end='')
                for i in range(round(int(day.min_temperature))):
                    print('+', end='')

            if day.max_temperature is not None:
                print('\033[1;31m', end='')
                for i in range(round(int(day.max_temperature))):
                    print('+', end='')

            print('\033[1;39m', end='')

            if day.min_temperature is not None or day.max_temperature is not \
                    None:
                    print(' {}C - {}C'.format(day.min_temperature,
                                      day.max_temperature))


class Data:

    def __init__(self, row):
        self.date = row['PKT'] or row['PKST']
        if row['Max TemperatureC'] is not '':
            self.max_temperature = int(row['Max TemperatureC'])
        else:
            self.max_temperature = None

        if row['Min TemperatureC'] is not '':
            self.min_temperature = int(row['Min TemperatureC'])
        else:
            self.min_temperature = None

        if row['Max Humidity'] is not '':
            self.max_humidity = int(row['Max Humidity'])
        else:
            self.max_humidity = None

        if row[' Mean Humidity'] is not '':
            self.mean_humidity = int(row[' Mean Humidity'])
        else:
            self.mean_humidity = None
