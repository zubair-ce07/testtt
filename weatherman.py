import argparse
import csv
import os
from datetime import datetime
from statistics import mean


class Weatherman:
    def __init__(self, path, year, month=None):
        self.path = path
        self.year = year
        self.month = month

    def filter_year_files(self):
        all_files = os.listdir(self.path)
        year_files = filter(lambda x: str(self.year) in x, all_files)
        return year_files

    def filter_month_files(self):
        month_files = filter(lambda x: x.endswith(str(self.year) + "_" + str(self.month) + ".txt"),
                             os.listdir(self.path))
        return month_files

    def read_file(self, input_files):
        read_files = []
        for input_file in input_files:
            read_file = csv.DictReader(open(input_file))
            read_files_ls = list(read_file)
            read_files.append(read_files_ls)
        return read_files

    def record(self, read_files):
        for entry in read_files:
            hi_temperature = []
            lo_temperature = []
            mean_humidity = []
            for row in entry:
                if row['Max TemperatureC'] != '':
                    x = str(row['Max TemperatureC'])
                    hi_temperature.append(x)
            self.hi_temperature = list(map(int, hi_temperature))
            for row in entry:
                if row['Min TemperatureC'] != '':
                    x = str(row['Min TemperatureC'])
                    lo_temperature.append(x)
            self.lo_temperature = list(map(int, lo_temperature))
            for row in entry:
                if row[' Mean Humidity'] != '':
                    x = str(row[' Mean Humidity'])
                    mean_humidity.append(x)
            self.mean_humidity = list(map(int, mean_humidity))


    def extreme_conditions(self, read_files):
        max_temperature = None
        min_temperature = None
        max_humidity = None
        for entry in read_files:
            for row in entry:
                if row['Max TemperatureC'] != '':
                    hi_temperature = int(row['Max TemperatureC'])
                    if max_temperature is None or max_temperature < hi_temperature:
                        max_temperature = hi_temperature
                        hottest_day = datetime.strptime(row['PKT'], '%Y-%m-%d').strftime('%B,%d')
                if row['Min TemperatureC'] != '':
                    lo_temperature = int(row['Min TemperatureC'])
                    if min_temperature is None or min_temperature > lo_temperature:
                        min_temperature = lo_temperature
                        coolest_day = datetime.strptime(row['PKT'], '%Y-%m-%d').strftime('%B,%d')
                if row['Max Humidity'] != '':
                    hi_humidity = int(row['Max Humidity'])
                    if max_humidity is None or max_humidity < hi_humidity:
                        max_humidity = hi_humidity
                        most_humid_day = datetime.strptime(row['PKT'], '%Y-%m-%d').strftime('%B,%d')
        print('{0}{1}{2}{3}'.format('Highest: ', max_temperature, 'C on ', hottest_day))
        print('{0}{1}{2}{3}'.format('Lowest: ', min_temperature, 'C on ', coolest_day))
        print('{0}{1}{2}{3}'.format('Humidity: ', max_humidity, '% on ', most_humid_day))

    def average_conditions(self):
        mean_hi_temperature = mean(self.hi_temperature)
        mean_lo_temperature = mean(self.lo_temperature)
        avg_mean_humidity = mean(self.mean_humidity)
        print('{0}{1}{2}'.format('Highest Average: ', int(mean_hi_temperature), 'C'))
        print('{0}{1}{2}'.format('Lowest Average: ', int(mean_lo_temperature), 'C'))
        print('{0}{1}{2}'.format('Average Mean Humidity: ', int(avg_mean_humidity), '%'))

    def everyday_weather(self, read_files):
        print(ym.strftime('%B'), year)
        for entry in read_files:
            for row in entry:
                if row['Max TemperatureC'] != '':
                    hi_temperature = int(row['Max TemperatureC'])
                    day = row['PKT']
                    date_formatted = datetime.strptime(day, '%Y-%m-%d').strftime('%d')
                    print('\033[35m', date_formatted, end='')
                    for i in range(0, hi_temperature):
                        print('\033[91m +', end='')
                    print('{0}{1}{2}'.format('\033[35m', hi_temperature, "C"))
                if row['Min TemperatureC'] != '':
                    lo_temperature = int(row['Min TemperatureC'])
                    day = row['PKT']
                    date_formatted = datetime.strptime(day, '%Y-%m-%d').strftime('%d')
                    print('\033[35m', date_formatted, end='')
                    for i in range(0, lo_temperature):
                        print('\033[34m -', end='')
                    print('{0}{1}{2}'.format('\033[35m', lo_temperature, 'C'))

    def days_weather(self, read_files):
        print('\033[0m', ym.strftime('%B'), year)
        for entry in read_files:
            for row in entry:
                if row['Min TemperatureC'] != '':
                    lo_temperature = int(row['Min TemperatureC'])
                    day = row['PKT']
                    obj = datetime.strptime(day, '%Y-%m-%d').strftime('%d')
                    print('\033[35m', obj, end='')
                    for i in range(0, lo_temperature):
                        print('\033[34m +', end='')
                if row['Max TemperatureC'] != '':
                    hi_temperature = int(row['Max TemperatureC'])
                    for i in range(0, hi_temperature):
                        print('\033[91m +', end='')
                    print('{0}{1}{2}{3}{4}{5}'.format('\033[35m', lo_temperature, 'C', '-', hi_temperature, 'C'))


parser = argparse.ArgumentParser()
parser.add_argument('path', help='Path to Directory', type=str)
parser.add_argument('-e', help='For a year, displays highest, lowest temperatures, highest humidity and respective days')
parser.add_argument('-a', help='For month and year, displays the average highest, lowest temperatures and mean humidity')
parser.add_argument('-c', help='For month, displays extreme temperatures in red and blue in two lines for each day')
parser.add_argument('-b', help='For month, displays extreme temperatures in red and blue in same line for each day')
args = parser.parse_args()
path = args.path
if args.e:
    year = args.e
    month = None
    weatherman1 = Weatherman(path, year, month)
    year_files = weatherman1.filter_year_files()
    yearly_data = weatherman1.read_file(year_files)
    weatherman1.extreme_conditions(yearly_data)
if args.a:
    ym = datetime.strptime(args.a, '%Y/%m')
    year = ym.strftime('%Y')
    month = ym.strftime('%b')
    weatherman1 = Weatherman(path, year, month)
    month_files = weatherman1.filter_month_files()
    monthly_data = weatherman1.read_file(month_files)
    records = weatherman1.record(monthly_data)
    weatherman1.average_conditions()
if args.c:
    ym = datetime.strptime(args.c, '%Y/%m')
    year = ym.strftime('%Y')
    month = ym.strftime('%b')
    weatherman1 = Weatherman(path, year, month)
    month_files = weatherman1.filter_month_files()
    monthly_data = weatherman1.read_file(month_files)
    weatherman1.everyday_weather(monthly_data)
if args.b:
    ym = datetime.strptime(args.b, '%Y/%m')
    year = ym.strftime('%Y')
    month = ym.strftime('%b')
    weatherman1 = Weatherman(path, year, month)
    month_files = weatherman1.filter_month_files()
    monthly_data = weatherman1.read_file(month_files)
    weatherman1.days_weather(monthly_data)
