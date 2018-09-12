import argparse
import csv
from datetime import datetime
import os
from statistics import mean


class Weatherman:

    def __init__(self, years, months, paths):
        self.year = years
        self.month = months
        self.path = paths
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

    def file_reads(self, input_files):
        read_files = []
        self.input_files = input_files
        for input_file in self.input_files:
            read_file = csv.DictReader(open(input_file))
            read_files_ls = list(read_file)
            read_files.append(read_files_ls)
        return read_files

    def extreme_conditions(self, read_files):
        self.read_files = read_files
        max_temp = None
        min_temp = None
        max_hum = None
        hottest_day = None
        coolest_day = None
        most_humid_day = None
        for entry in self.read_files:
            for row in entry:
                if row["Max TemperatureC"] == "":
                    pass
                else:
                    hi_temp = int(row["Max TemperatureC"])
                    if max_temp is None or max_temp < hi_temp:
                        max_temp = hi_temp
                        hottest_day = datetime.strptime(row["PKT"], '%Y-%m-%d').strftime("%B,%d")

                if row["Min TemperatureC"] == '':
                    pass
                else:
                    lo_temp = int(row["Min TemperatureC"])
                    if min_temp is None or min_temp > lo_temp:
                        min_temp = lo_temp
                        coolest_day = datetime.strptime(row["PKT"], '%Y-%m-%d').strftime("%B,%d")

                if row["Max Humidity"] == '':
                    pass
                else:
                    hi_hum = int(row["Max Humidity"])
                    if max_hum is None or max_hum < hi_hum:
                        max_hum = hi_hum
                        most_humid_day = datetime.strptime(row["PKT"], '%Y-%m-%d').strftime("%B,%d")
        print("Highest:", max_temp, "C on", hottest_day)
        print("Lowest:", min_temp, "C on", coolest_day)
        print("Humidity:", max_hum, "% on", most_humid_day)

    def average_conditions(self, read_files):
        self.read_files = read_files
        mean_hi_temp = 0
        mean_lo_temp = 0
        avg_mean_humidity = 0
        for entry in self.read_files:
            hi_temp = []
            lo_temp = []
            mean_hum = []
            for row in entry:
                if row["Max TemperatureC"] == '':
                    pass
                else:
                    x = str(row["Max TemperatureC"])
                    hi_temp.append(x)
            hi_temp = list(map(int, hi_temp))
            mean_hi_temp = mean(hi_temp)

            for row in entry:
                if row["Min TemperatureC"] == '':
                    pass
                else:
                    x = str(row["Min TemperatureC"])
                    lo_temp.append(x)
            lo_temp = list(map(int, lo_temp))
            mean_lo_temp = mean(lo_temp)

            for row in entry:
                if row[" Mean Humidity"] == '':
                    pass
                else:
                    x = str(row[" Mean Humidity"])
                    mean_hum.append(x)
            mean_hum = list(map(int, mean_hum))
            avg_mean_humidity = mean(mean_hum)
        print("Highest Average:", int(mean_hi_temp), "C")
        print("Lowest Average:", int(mean_lo_temp), "C")
        print("Average Mean Humidity:", int(avg_mean_humidity), "C")

    def everyday_weather(self, read_files):
        self.read_files = read_files
        for entry in self.read_files:
            for row in entry:
                if row["Max TemperatureC"] == '':
                    pass
                else:
                    hi_temp = int(row["Max TemperatureC"])
                    day = row["PKT"]
                    obj = datetime.strptime(day, '%Y-%m-%d').strftime("%d")
                    print("\033[35m", obj, end='')
                    for i in range(0, hi_temp):
                        print("\033[91m +", end='')
                    print('\033[35m', hi_temp, "C")
                if row["Min TemperatureC"] == '':
                    pass
                else:
                    lo_temp = int(row["Min TemperatureC"])
                    day = row["PKT"]
                    obj = datetime.strptime(day, '%Y-%m-%d').strftime("%d")
                    print("\033[35m", obj, end='')
                    for i in range(0, lo_temp):
                        print("\033[34m -", end='')
                    print('\033[35m', lo_temp, "C")

    def days_weather(self, read_files):
        self.read_files = read_files
        for entry in self.read_files:
            for row in entry:
                if row["Min TemperatureC"] == '':
                    pass
                else:
                    lo_temp = int(row["Min TemperatureC"])
                    day = row["PKT"]
                    obj = datetime.strptime(day, '%Y-%m-%d').strftime("%d")
                    print("\033[35m", obj, end='')
                    for i in range(0, lo_temp):
                        print("\033[34m +", end='')
                if row["Max TemperatureC"] == '':
                    pass
                else:
                    hi_temp = int(row["Max TemperatureC"])
                    for i in range(0, hi_temp):
                        print("\033[91m +", end='')
                    print('\033[35m', lo_temp, "C", "-", hi_temp, "C")


parser = argparse.ArgumentParser()
parser.add_argument("path", help="Path to Directory", type = str)
parser.add_argument("-e", help="For a year, displays highest,lowest temperatures,highest humidity and respective days")
parser.add_argument("-a", help="For month and year, displays the average highest,lowest temperatures and mean humidity")
parser.add_argument("-c", help="For month, displays extreme temperatures in red and blue in two lines for each day")
parser.add_argument("-b", help="For month, displays extreme temperatures in red and blue in same line for each day")
args = parser.parse_args()
path = args.path
if args.e:
    year = args.e
    w1 = Weatherman(year, 8, path)
    w1_files = w1.filter_year_files()
    rows = w1.file_reads(w1_files)
    w1.extreme_conditions(rows)
if args.a:
    ym = datetime.strptime(args.a, '%Y/%m')
    year = ym.strftime("%Y")
    month = ym.strftime("%b")
    w2 = Weatherman(year, month, path)
    w2_files = w2.filter_month_files()
    rows = w2.file_reads(w2_files)
    w2.average_conditions(rows)
if args.c:
    ym = datetime.strptime(args.c, '%Y/%m')
    year = ym.strftime("%Y")
    month = ym.strftime("%b")
    print(ym.strftime("%B"), year)
    w3 = Weatherman(year, month, path)
    w3_files = w3.filter_month_files()
    rows = w3.file_reads(w3_files)
    w3.everyday_weather(rows)
if args.b:
    ym = datetime.strptime(args.b, '%Y/%m')
    year = ym.strftime("%Y")
    month = ym.strftime("%b")
    print("\033[0m", ym.strftime("%B"), year)
    w4 = Weatherman(year, month, path)
    w4_files = w4.filter_month_files()
    rows = w4.file_reads(w4_files)
    w4.days_weather(rows)
