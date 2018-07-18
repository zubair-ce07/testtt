import csv
import glob

from weatherman_records import *


class WeatherReport:
    def __init__(self):
        self.weather_records = list()

    def file_read(self, dir_name):
        file_name_t = f"{dir_name}*.txt"
        for file_path in glob.glob(file_name_t):
            with open(file_path, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                filtered_records = list(filter(lambda line:
                                               line.get('Max TemperatureC')
                                               and line.get('Min TemperatureC')
                                               and line.get('Max Humidity')
                                               and line.get(' Mean Humidity'),
                                               reader))
                for row in filtered_records:
                    self.weather_records.append(DailyRecords(row))

    def yearly_report(self, year):
        yearly_record = list(filter(lambda record: record.date.year == year,
                                    self.weather_records))

        max_temp = max(yearly_record, key=lambda day: day.max_temperature)
        min_temp = min(yearly_record, key=lambda day: day.min_temperature)
        max_humidity = max(yearly_record, key=lambda day: day.max_humidity)

        print(f'Highest: {max_temp.max_temperature}C on '
              f'{max_temp.date.strftime("%b")} {max_temp.date.day}')

        print(f'Lowest: {min_temp.min_temperature}C on '
              f'{min_temp.date.strftime("%b")} {min_temp.date.day}')

        print(f'Highest: {max_humidity.max_humidity}% on '
              f'{max_humidity.date.strftime("%b")} {max_humidity.date.day}')

    def monthly_report(self, year, month):
        monthly_record = list(filter(lambda record: record.date.year == year
                                     and record.date.strftime("%b") == month,
                                     self.weather_records))

        avg_max_temp = sum(day.max_temperature for day in
                           monthly_record)//len(monthly_record)
        avg_min_temp = sum(day.min_temperature for day in
                           monthly_record)//len(monthly_record)
        avg_mean_humidity = sum(day.mean_humidity for day in
                                monthly_record)//len(monthly_record)

        print(f'Highest Average: {avg_max_temp}C')
        print(f'Lowest Average: {avg_min_temp}C')
        print(f'Average Mean Humidity: {avg_mean_humidity}%')

    def daily_report(self, year, month):
        monthly_record = list(filter(lambda record: record.date.year == year
                                     and record.date.strftime("%b") == month,
                                     self.weather_records))
        for day in monthly_record:
            print(str(day.date.day).zfill(2), end=' ')
            print(f'{Colors.BLUE}+'*day.min_temperature, end='')
            print(f'{Colors.RED}+'*day.max_temperature, end='')
            print(f'{Colors.RESET} {day.min_temperature}C - '
                  f'{day.max_temperature}C')
