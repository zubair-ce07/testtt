from fnmatch import fnmatch
from datetime import datetime

import csv
import os

from report_calculations import *

RED = "\033[1;31m"
BLUE = "\033[1;34m"
RESET = "\033[1;39m"


class WeatherReport:
    def __init__(self):
        self.readings = list()

    def file_read(self, dir_name, year, month):
        for file_path in os.listdir(dir_name):
            if not fnmatch(file_path, f"Murree_weather_{year}_{month}.txt"):
                continue
            with open(dir_name + file_path, 'r') as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        if not row:
                            continue
                        self.readings.append(DailyRecords(row))

    def yearly_report(self):
        obj_max_temp = max_temperature_record(self.readings)
        month_max_temp = datetime.strptime(obj_max_temp.date,
                                           "%Y-%m-%d").strftime("%b")
        day_max_temp = datetime.strptime(obj_max_temp.date,
                                         "%Y-%m-%d").strftime("%d")

        print(f'Highest: {obj_max_temp.max_temperature}C on {month_max_temp}'
              f' {day_max_temp}')

        obj_min_temp = min_temperature_record(self.readings)
        month_min_temp = datetime.strptime(obj_min_temp.date,
                                           "%Y-%m-%d").strftime("%b")
        day_min_temp = datetime.strptime(obj_min_temp.date,
                                         "%Y-%m-%d").strftime("%d")

        print(f'Lowest: {obj_min_temp.min_temperature}C on {month_min_temp}'
              f' {day_min_temp}')

        obj_max_hum = max_humidity_record(self.readings)
        month_max_hum = datetime.strptime(obj_max_hum.date,
                                          "%Y-%m-%d").strftime("%b")
        day_max_hum = datetime.strptime(obj_max_hum.date,
                                        "%Y-%m-%d").strftime("%d")

        print(f'Highest: {obj_max_hum.max_humidity}% on {month_max_hum} '
              f'{day_max_hum}', end='\n')

    def monthly_report(self):
        avg_max_temp = get_avg_max_temp(self.readings)
        avg_min_temp = get_avg_min_temp(self.readings)
        avg_mean_hum = get_avg_mean_humidity(self.readings)

        print(f'Highest Average: {round(avg_max_temp)}C')
        print(f'Lowest Average: {round(avg_min_temp)}C')
        print(f'Average Mean Humidity: {round(avg_mean_hum)}%', end='\n')

    def daily_report(self):
        for index, day in enumerate(self.readings):
            if not day.min_temperature or not day.max_temperature:
                continue
            print(str(index).zfill(2), end=' ')
            print(RED, end='')
            print('+'*day.min_temperature, end='')
            print(BLUE, end='')
            print('+'*day.max_temperature, end='')
            print(f'{RESET} {day.min_temperature}C - '
                  f'{day.max_temperature}C', end='\n')


class DailyRecords:

    def __init__(self, row):
        self.date = row.get('PKT') or row.get('PKST')

        if row.get('Max TemperatureC') is not '':
            self.max_temperature = int(row.get('Max TemperatureC'))
        else:
            self.max_temperature = None

        if row.get('Min TemperatureC') is not '':
            self.min_temperature = int(row.get('Min TemperatureC'))
        else:
            self.min_temperature = None

        if row.get('Max Humidity') is not '':
            self.max_humidity = int(row.get('Max Humidity'))
        else:
            self.max_humidity = None

        if row.get(' Mean Humidity') is not '':
            self.mean_humidity = int(row.get(' Mean Humidity'))
        else:
            self.mean_humidity = None
