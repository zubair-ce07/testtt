import os
import csv
from fnmatch import fnmatch
from datetime import datetime

from report_calculations import *


class Colors:
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
                        if row:
                            self.readings.append(DailyRecords(row))

    def yearly_report(self):
        obj_max_temp = max_temperature_record(self.readings)
        month_max_temp = obj_max_temp.date.strftime("%b")
        day_max_temp = obj_max_temp.date.day

        print(f'Highest: {obj_max_temp.max_temperature}C on {month_max_temp}'
              f' {day_max_temp}')

        obj_min_temp = min_temperature_record(self.readings)
        month_min_temp = obj_min_temp.date.strftime("%b")
        day_min_temp = obj_min_temp.date.day

        print(f'Lowest: {obj_min_temp.min_temperature}C on {month_min_temp}'
              f' {day_min_temp}')

        obj_max_hum = max_humidity_record(self.readings)
        month_max_hum = obj_max_hum.date.strftime("%b")
        day_max_hum = obj_max_hum.date.day

        print(f'Highest: {obj_max_hum.max_humidity}% on {month_max_hum} '
              f'{day_max_hum}', end='\n')

    def monthly_report(self):
        avg_max_temp = get_avg_max_temp(self.readings)
        avg_min_temp = get_avg_min_temp(self.readings)
        avg_mean_hum = get_avg_mean_humidity(self.readings)

        print(f'Highest Average: {avg_max_temp}C')
        print(f'Lowest Average: {avg_min_temp}C')
        print(f'Average Mean Humidity: {avg_mean_hum}%', end='\n')

    def daily_report(self):
        for day in self.readings:
            if not day.min_temperature or not day.max_temperature:
                continue
            print(str(day.date.day).zfill(2), end=' ')

            print(Colors.RED, end='')
            print('+'*day.min_temperature, end='')

            print(Colors.BLUE, end='')
            print('+'*day.max_temperature, end='')

            print(f'{Colors.RESET} {day.min_temperature}C - '
                  f'{day.max_temperature}C', end='\n')


class DailyRecords:

    def __init__(self, row):

        date = row.get('PKT') or row.get('PKST')
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.max_temperature = int(row.get('Max TemperatureC') or 0) or None
        self.min_temperature = int(row.get('Min TemperatureC')or 0) or None
        self.max_humidity = int(row.get('Max Humidity')or 0) or None
        self.mean_humidity = int(row.get(' Mean Humidity')or 0) or None
