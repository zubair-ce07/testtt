import re
import os
import csv
import calendar
import argparse
from collections import namedtuple

red = "\033[1;31;47m"
blu = "\033[1;34;47m"
black = "\033[1;30;47m"

min_col = "Min TemperatureC"
max_col = "Max TemperatureC"
hum_col = "Max Humidity"

Date = namedtuple("Date", ["y", "m", "d"])
Day = namedtuple("Day", ["date", "max_temp", "min_temp", "humidity"])
Month = namedtuple("Month", ["month", "days", "max_avg", "min_avg", "hum_avg"])
Year = namedtuple("Year", ["year", "months", "max_day", "min_day", "humid_day"])


def date_split(value):
    return map(int, str(value).split('-'))


def yearly_sort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def skip_last_line(it):
    prev = next(it)
    for item in it:
        yield prev
        prev = item


def get_files_sorted(path):
    file_names = []
    for root, dirs, files in os.walk(path):
        for file_name in sorted(files, key=yearly_sort):
            file_names.append(os.path.join(root, file_name))
    return file_names


class Weather:
    def __init__(self):
        self.days = []
        self.months = []
        self.years = []

    def read_rows(self, files):
        for file_name in files:
            with open(file_name) as file:
                next(file)
                csv_file = csv.DictReader(file)
                for line in skip_last_line(csv_file):
                    if line[min_col] and line[max_col] and line[hum_col]:
                        self.parse_rows(line)

    def parse_rows(self, line):
        date_line = line.get("PKT") or line.get("PKST")
        y, m, d = date_split(date_line)
        max_temp = int(line[max_col])
        min_temp = int(line[min_col])
        humidity = int(line[hum_col])
        date = Date(y, m, d)
        day = Day(date, max_temp, min_temp, humidity)
        self.days.append(day)

    def populate_records(self):
        months, days = [], []
        prev_year, prev_month, prev_day = self.days[0].date
        for d in self.days:
            curr_year, curr_month, day = d.date
            if prev_month != curr_month:
                self.add_month(days, curr_month)
                months.append(self.months[-1])
                prev_month, days = curr_month, []
                if prev_year != curr_year:
                    self.add_year(months, curr_year)
                    prev_year, months = curr_year, []
            days.append(d)

    def add_month(self, days, month):
        max_sum = min_sum = humid_sum = 0
        days_in_month = 0
        for day in days:
            max_sum += day.max_temp
            min_sum += day.min_temp
            humid_sum += day.humidity
            days_in_month += 1
        max_ = round(max_sum / days_in_month)
        min_ = round(min_sum / days_in_month)
        hum_ = round(humid_sum / days_in_month)
        self.months.append(Month(month, days, max_, min_, hum_))

    def add_year(self, months, year):
        max_t, min_t, humid = -273, 100, -1
        max_d, min_d, hum_d = (), (), ()
        for month in months:
            for day in month.days:
                if max_t < day.max_temp:
                    max_t, max_d = day.max_temp, day
                if min_t > day.min_temp:
                    min_t, min_d = day.min_temp, day
                if humid < day.humidity:
                    humid, hum_d = day.humidity, day
        self.years.append(Year(year, months, max_d, min_d, hum_d))

    def annual_report(self, year_str):
        for year in self.years:
            if year.year == int(year_str):
                max_d = year.max_day
                min_d = year.min_day
                humid = year.humid_day
                print("Highest:", max_d.max_temp, "\bC on",
                      calendar.month_name[max_d.date.m], max_d.date.d)
                print("Lowest:", min_d.min_temp, "\bC on",
                      calendar.month_name[min_d.date.m], min_d.date.d)
                print("Humid:", humid.humidity, "\b% on",
                      calendar.month_name[humid.date.m], humid.date.m)
                return
        print("Not Found!")

    def find_month(self, year_str, month_str):
        m, y = int(month_str), int(year_str)
        for year in self.years:
            if year.year == y:
                for month in year.months:
                    if month.month == m:
                        print(calendar.month_name[m], y)
                        return month

    def monthly_avg_report(self, year_str, month_str):
        month = self.find_month(year_str, month_str)
        print("Highest Average:", month.max_avg, "\bC")
        print("Lowest Average:", month.min_avg, "\bC")
        print("Average Humidity:", month.hum_avg, "\b%")

    def month_chart_dual(self, year_str, month_str):
        month = self.find_month(year_str, month_str)
        for day in month.days:
            d, max_, min_ = day.date.d, day.max_temp, day.min_temp
            print(red, "{:2}".format(d), "+" * max_, "{}".format(max_), "\bC")
            print(blu, "{:2}".format(d), "+" * min_, "{}".format(min_), "\bC")

    def month_chart_bonus(self, year_str, month_str):
        month = self.find_month(year_str, month_str)
        for day in month.days:
            d, max_, min_ = day.date.d, day.max_temp, day.min_temp
            print(black, "{:2}".format(d), end=" ")
            print(blu, "+" * min_, sep="", end="")
            print(red, "+" * (max_ - min_), sep="", end="")
            print(black, "{}".format(min_), "\bC -", "{}".format(max_), "\bC")


def cmd_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", help="Annual Report of Extremes", nargs=2)
    parser.add_argument("-a", help="Monthly average", nargs=2)
    parser.add_argument("-c", help="Monthly Bar Chart", nargs=2)
    parser.add_argument("-b", help="Bonus Chart", nargs=2)
    return parser.parse_args()


def driver(path):
    weather = Weather()
    weather.read_rows(get_files_sorted(path))
    weather.populate_records()
    return weather


def main():
    arg = cmd_parser()
    if arg.e:
        driver(arg.e[1]).annual_report(arg.e[0])
    elif arg.a:
        term = str(arg.a[0]).split("/")
        driver(arg.a[1]).monthly_avg_report(term[0], term[1])
    elif arg.c:
        term = str(arg.c[0]).split("/")
        driver(arg.c[1]).month_chart_dual(term[0], term[1])
    elif arg.b:
        term = str(arg.b[0]).split("/")
        driver(arg.b[1]).month_chart_bonus(term[0], term[1])

if __name__ == '__main__':
    main()

