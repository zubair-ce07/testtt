import argparse
import csv
import os
from datetime import datetime
from statistics import mean


class Weatherman:
    def __init__(self, path):
        self.path = path

    def filter_year_files(self):
        all_files = os.listdir(self.path)
        year_files = filter(lambda x: str(year) in x, all_files)
        return year_files

    def filter_month_files(self):
        month_files = filter(lambda x: x.endswith(str(year) + "_" + str(month) + ".txt"),
                             os.listdir(self.path))
        return month_files

    def weatherman_readings(self, input_files):
        required_data = []
        for input_file in input_files:
            read_file = csv.DictReader(open(input_file))
            required_data.append(read_file)
        return required_data

    def record(self, required_data):
        highest_temperature = []
        lowest_temperature = []
        highest_humidity = []
        year_dates = []
        for data in required_data:
            high_temperature = []
            low_temperature = []
            mean_humidity = []
            max_humidity = []
            day =[]
            date = []
            for row in data:
                if row['Max TemperatureC'] != '':
                    x = str(row['Max TemperatureC'])
                    high_temperature.append(x)
                if row['Min TemperatureC'] != '':
                    x = str(row['Min TemperatureC'])
                    low_temperature.append(x)
                if row[' Mean Humidity'] != '':
                    x = str(row[' Mean Humidity'])
                    mean_humidity.append(x)
                if row['Max Humidity'] != '':
                    x = str(row['Max Humidity'])
                    max_humidity.append(x)
                if row['PKT'] != '':
                    x = datetime.strptime(row['PKT'], '%Y-%m-%d').strftime('%d')
                    y = datetime.strptime(row['PKT'], '%Y-%m-%d').strftime('%B,%d')
                    day.append(x)
                    date.append(y)
            self.high_temperature = list(map(int, high_temperature))
            self.low_temperature = list(map(int, low_temperature))
            self.mean_humidity = list(map(int, mean_humidity))
            self.max_humidity = list(map(int, max_humidity))
            self.day = list(day)
            self.date = list(date)
            highest_temperature.append(self.high_temperature)
            lowest_temperature.append(self.low_temperature)
            year_dates.append(self.date)
            highest_humidity.append(self.max_humidity)
        self.highest_temperature = highest_temperature
        self.lowest_temperature = lowest_temperature
        self.highest_humidity = highest_humidity
        self.year_dates = year_dates

    def extreme_conditions(self):
        max_high_temperature, hottest_day = max((x, (i, j))
                                   for i, row in enumerate(self.highest_temperature)
                                   for j, x in enumerate(row))
        min_low_temperature, coolest_day = min((x, (i, j))
                                   for i, row in enumerate(self.lowest_temperature)
                                   for j, x in enumerate(row))
        max_high_humidity, most_humid_day = max((x, (i, j))
                                   for i, row in enumerate(self.highest_humidity)
                                   for j, x in enumerate(row))
        print('{0}{1}{2}{3}'.format('Highest: ', max_high_temperature, 'C on ', self.year_dates[hottest_day[0]][hottest_day[1]]))
        print('{0}{1}{2}{3}'.format('Lowest: ', min_low_temperature, 'C on ', self.year_dates[coolest_day[0]][coolest_day[1]]))
        print('{0}{1}{2}{3}'.format('Humidity: ', max_high_humidity, '% on ', self.year_dates[most_humid_day[0]][most_humid_day[1]]))

    def average_conditions(self):
        mean_hi_temperature = mean(self.high_temperature)
        mean_lo_temperature = mean(self.low_temperature)
        avg_mean_humidity = mean(self.mean_humidity)
        print('{0}{1}{2}'.format('Highest Average: ', int(mean_hi_temperature), 'C'))
        print('{0}{1}{2}'.format('Lowest Average: ', int(mean_lo_temperature), 'C'))
        print('{0}{1}{2}'.format('Average Mean Humidity: ', int(avg_mean_humidity), '%'))

    def everyday_weather(self):
        print(ym.strftime('%B'), year)
        for i in range(0, len(self.high_temperature)):
            print('{0}{1}{2}'.format('\033[35m', self.day[i], '\033[91m +'*self.high_temperature[i]), end='')
            print('{0}{1}{2}'.format('\033[35m', self.high_temperature[i], 'C'))
            print('{0}{1}{2}'.format('\033[35m', self.day[i], '\033[34m +' * self.low_temperature[i]), end='')
            print('{0}{1}{2}'.format('\033[35m', self.low_temperature[i], 'C'))

    def days_weather(self):
        print('\033[0m', ym.strftime('%B'), year)
        for i in range(0, len(self.high_temperature)):
            print('\033[35m', self.day[i], end='')
            print('\033[34m +' * self.low_temperature[i], end='')
            print('\033[91m +' * self.high_temperature[i], end='')
            print('{0}{1}{2}{3}{4}'.format('\033[35m', self.low_temperature[i], 'C-', self.high_temperature[i], 'C'))


parser = argparse.ArgumentParser()
parser.add_argument('path', help='Path to Directory', type=str)
parser.add_argument('-e', help='For a year, displays highest, lowest temperatures, highest humidity and respective days')
parser.add_argument('-a', help='For month and year, displays the average highest, lowest temperatures and mean humidity')
parser.add_argument('-c', help='For month, displays extreme temperatures in red and blue in two lines for each day')
parser.add_argument('-b', help='For month, displays extreme temperatures in red and blue in same line for each day')
args = parser.parse_args()
path = args.path
weatherman1 = Weatherman(path)
if args.e:
    year = args.e
    month = None
    year_files = weatherman1.filter_year_files()
    yearly_data = weatherman1.weatherman_readings(year_files)
    records = weatherman1.record(yearly_data)
    weatherman1.extreme_conditions()
if args.a:
    ym = datetime.strptime(args.a, '%Y/%m')
    year = ym.strftime('%Y')
    month = ym.strftime('%b')
    weatherman1 = Weatherman(path)
    month_files = weatherman1.filter_month_files()
    monthly_data = weatherman1.weatherman_readings(month_files)
    records = weatherman1.record(monthly_data)
    weatherman1.average_conditions()
if args.c:
    ym = datetime.strptime(args.c, '%Y/%m')
    year = ym.strftime('%Y')
    month = ym.strftime('%b')
    weatherman1 = Weatherman(path)
    month_files = weatherman1.filter_month_files()
    monthly_data = weatherman1.weatherman_readings(month_files)
    records = weatherman1.record(monthly_data)
    weatherman1.everyday_weather()
if args.b:
    ym = datetime.strptime(args.b, '%Y/%m')
    year = ym.strftime('%Y')
    month = ym.strftime('%b')
    weatherman1 = Weatherman(path)
    month_files = weatherman1.filter_month_files()
    monthly_data = weatherman1.weatherman_readings(month_files)
    records = weatherman1.record(monthly_data)
    weatherman1.days_weather()
