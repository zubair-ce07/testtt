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
        self.input_files = []
        self.read_files = []

    def filter_year_files(self):
        year_files = filter(lambda x: x.startswith('Murree_weather_' + str(self.year)),
                            os.listdir(self.path))
        input_files = []
        for filenames in year_files:
            input_files.append(filenames)
        return input_files

    def filter_month_files(self):
        month_files = filter(lambda x: x.startswith('Murree_weather_' + str(self.year) + "_" + str(self.month)),
                             os.listdir(self.path))
        input_files = []
        for filenames in month_files:
            input_files.append(filenames)
        return input_files

    def read_file(self, input_files):
        read_files = []
        for input_file in input_files:
            read_file = csv.DictReader(open(input_file))
            read_files_ls = list(read_file)
            read_files.append(read_files_ls)
        return read_files

    def extreme_conditions(self, read_files):
        max_temperature = None
        min_temperature = None
        max_humidity = None
        for entry in read_files:
            for row in entry:
                if row["Max TemperatureC"] == "":
                    pass
                else:
                    hi_temperature = int(row["Max TemperatureC"])
                    if max_temperature is None or max_temperature < hi_temperature:
                        max_temperature = hi_temperature
                        hottest_day = datetime.strptime(row["PKT"], '%Y-%m-%d').strftime("%B,%d")
                if row["Min TemperatureC"] == '':
                    pass
                else:
                    lo_temperature = int(row["Min TemperatureC"])
                    if min_temperature is None or min_temperature > lo_temperature:
                        min_temperature = lo_temperature
                        coolest_day = datetime.strptime(row["PKT"], '%Y-%m-%d').strftime("%B,%d")
                if row["Max Humidity"] == '':
                    pass
                else:
                    hi_humidity = int(row["Max Humidity"])
                    if max_humidity is None or max_humidity < hi_humidity:
                        max_humidity = hi_humidity
                        most_humid_day = datetime.strptime(row["PKT"], '%Y-%m-%d').strftime("%B,%d")
        print("Highest:", max_temperature, "C on", hottest_day)
        print("Lowest:", min_temperature, "C on", coolest_day)
        print("Humidity:", max_humidity, "% on", most_humid_day)

    def average_conditions(self, read_files):
        for entry in read_files:
            hi_temperature = []
            lo_temperature = []
            mean_humidity = []
            for row in entry:
                if row["Max TemperatureC"] == '':
                    pass
                else:
                    x = str(row["Max TemperatureC"])
                    hi_temperature.append(x)
            hi_temperature = list(map(int, hi_temperature))
            mean_hi_temperature = mean(hi_temperature)
            for row in entry:
                if row["Min TemperatureC"] == '':
                    pass
                else:
                    x = str(row["Min TemperatureC"])
                    lo_temperature.append(x)
            lo_temperature = list(map(int, lo_temperature))
            mean_lo_temperature = mean(lo_temperature)
            for row in entry:
                if row[" Mean Humidity"] == '':
                    pass
                else:
                    x = str(row[" Mean Humidity"])
                    mean_humidity.append(x)
            mean_humidity = list(map(int, mean_humidity))
            avg_mean_humidity = mean(mean_humidity)
        print("Highest Average:", int(mean_hi_temperature), "C")
        print("Lowest Average:", int(mean_lo_temperature), "C")
        print("Average Mean Humidity:", int(avg_mean_humidity), "C")

    def everyday_weather(self, read_files):
        print(ym.strftime("%B"), year)
        for entry in read_files:
            for row in entry:
                if row["Max TemperatureC"] == '':
                    pass
                else:
                    hi_temperature = int(row["Max TemperatureC"])
                    day = row["PKT"]
                    obj = datetime.strptime(day, '%Y-%m-%d').strftime("%d")
                    print("\033[35m", obj, end='')
                    for i in range(0, hi_temperature):
                        print("\033[91m +", end='')
                    print('\033[35m', hi_temperature, "C")
                if row["Min TemperatureC"] == '':
                    pass
                else:
                    lo_temperature = int(row["Min TemperatureC"])
                    day = row["PKT"]
                    obj = datetime.strptime(day, '%Y-%m-%d').strftime("%d")
                    print("\033[35m", obj, end='')
                    for i in range(0, lo_temperature):
                        print("\033[34m -", end='')
                    print('\033[35m', lo_temperature, "C")

    def days_weather(self, read_files):
        print("\033[0m", ym.strftime("%B"), year)
        for entry in read_files:
            for row in entry:
                if row["Min TemperatureC"] == '':
                    pass
                else:
                    lo_temperature = int(row["Min TemperatureC"])
                    day = row["PKT"]
                    obj = datetime.strptime(day, '%Y-%m-%d').strftime("%d")
                    print("\033[35m", obj, end='')
                    for i in range(0, lo_temperature):
                        print("\033[34m +", end='')
                if row["Max TemperatureC"] == '':
                    pass
                else:
                    hi_temperature = int(row["Max TemperatureC"])
                    for i in range(0, hi_temperature):
                        print("\033[91m +", end='')
                    print('\033[35m', lo_temperature, "C", "-", hi_temperature, "C")


parser = argparse.ArgumentParser()
parser.add_argument("path", help="Path to Directory", type=str)
parser.add_argument("-e", help="For a year, displays highest,lowest temperatures,highest humidity and respective days")
parser.add_argument("-a", help="For month and year, displays the average highest,lowest temperatures and mean humidity")
parser.add_argument("-c", help="For month, displays extreme temperatures in red and blue in two lines for each day")
parser.add_argument("-b", help="For month, displays extreme temperatures in red and blue in same line for each day")
args = parser.parse_args()
path = args.path
if args.e:
    year = args.e
    weatherman1 = Weatherman(path, year)
    year_files = weatherman1.filter_year_files()
    yearly_data = weatherman1.read_file(year_files)
    weatherman1.extreme_conditions(yearly_data)
if args.a:
    ym = datetime.strptime(args.a, '%Y/%m')
    year = ym.strftime("%Y")
    month = ym.strftime("%b")
    weatherman2 = Weatherman(path, year, month)
    month_files = weatherman2.filter_month_files()
    monthly_data = weatherman2.read_file(month_files)
    weatherman2.average_conditions(monthly_data)
if args.c:
    ym = datetime.strptime(args.c, '%Y/%m')
    year = ym.strftime("%Y")
    month = ym.strftime("%b")
    weatherman2 = Weatherman(path, year, month)
    month_files = weatherman2.filter_month_files()
    monthly_data = weatherman2.read_file(month_files)
    weatherman2.everyday_weather(monthly_data)
if args.b:
    ym = datetime.strptime(args.b, '%Y/%m')
    year = ym.strftime("%Y")
    month = ym.strftime("%b")
    weatherman2 = Weatherman(path, year, month)
    month_files = weatherman2.filter_month_files()
    monthly_data = weatherman2.read_file(month_files)
    weatherman2.days_weather(monthly_data)
