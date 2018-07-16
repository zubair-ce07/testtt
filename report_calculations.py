import csv
import glob

from data_structure import *


class WeatherReport:
    def __init__(self):
        self.readings = list()

    def file_read(self, dir_name, year, month):
        dir_file_path = f'{dir_name}Murree_weather_{year}_{month}.txt'
        for file_path in glob.glob(dir_file_path):
            with open(file_path, 'r') as csv_file:
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

        obj_max_humidity = max_humidity_record(self.readings)
        month_max_humidity = obj_max_humidity.date.strftime("%b")
        day_max_humidity = obj_max_humidity.date.day

        print(f'Highest: {obj_max_humidity.max_humidity}% on '
              f'{month_max_humidity} {day_max_humidity}', end='\n')

    def monthly_report(self):
        avg_max_temp = get_avg_max_temp(self.readings)
        avg_min_temp = get_avg_min_temp(self.readings)
        avg_mean_humidity = get_avg_mean_humidity(self.readings)

        print(f'Highest Average: {avg_max_temp}C')
        print(f'Lowest Average: {avg_min_temp}C')
        print(f'Average Mean Humidity: {avg_mean_humidity}%', end='\n')

    def daily_report(self):
        for day in self.readings:
            if not day.min_temperature or not day.max_temperature:
                continue
            print(str(day.date.day).zfill(2), end=' ')
            print(f'{Colors.RED}+'*day.min_temperature, end='')
            print(f'{Colors.BLUE}+'*day.max_temperature, end='')
            print(f'{Colors.RESET} {day.min_temperature}C - '
                  f'{day.max_temperature}C', end='\n')


def max_temperature_record(readings):
    readings = [day for day in readings if day.max_temperature]
    return max(readings, key=lambda day: day.max_temperature)


def min_temperature_record(readings):
    readings = [day for day in readings if day.min_temperature]
    return min(readings, key=lambda day: day.min_temperature)


def max_humidity_record(readings):
    readings = [day for day in readings if day.max_humidity]
    return max(readings, key=lambda day: day.max_humidity)


def get_avg_max_temp(readings):
    total_days = len([day for day in readings if day.max_temperature])
    return sum(day.max_temperature for day in readings
               if day.max_temperature)//total_days


def get_avg_min_temp(readings):
    total_days = len([day for day in readings if day.min_temperature])
    return sum(day.min_temperature for day in readings
               if day.min_temperature)//total_days


def get_avg_mean_humidity(readings):
    total_days = len([day for day in readings if day.mean_humidity])
    return sum(day.mean_humidity for day in readings
               if day.mean_humidity)//total_days