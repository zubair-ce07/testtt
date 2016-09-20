import re
import os
import csv
import calendar
import argparse


def date_split(value):
    return str(value).split("-")


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


class WeatherRecord:
    def __init__(self, max_temp=-273, min_temp=100, max_humid=-1):
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humid = max_humid


class Day(WeatherRecord):
    def __init__(self, day, max_temp, min_temp, humidity):
        WeatherRecord.__init__(self, max_temp, min_temp, humidity)
        self.day = day


class WeatherStats(WeatherRecord):
    def __init__(self, year):
        WeatherRecord.__init__(self)
        self.year = year
        self.max_day = 0
        self.min_day = 0
        self.humid_day = 0


class Month(WeatherStats):

    def __init__(self, year, month_num, records):
        WeatherStats.__init__(self, year)
        self.month_num = month_num
        self.records = records
        self.avg_temp_max = -273
        self.avg_temp_min = 100
        self.avg_humidity = -1
        self.monthly_calculations()

    def monthly_calculations(self):
        max_sum = min_sum = humid_sum = days = 0
        for day in self.records:
            max_sum += day.max_temp
            min_sum += day.min_temp
            humid_sum += day.max_humid
            days += 1
            self.find_extremes(day.day, day.max_temp,
                               day.min_temp, day.max_humid)
        self.avg_temp_max = round(max_sum / days)
        self.avg_temp_min = round(min_sum / days)
        self.avg_humidity = round(humid_sum / days)

    def find_extremes(self, day, max_, min_, humid):
        if self.max_temp < max_:
            self.max_temp, self.max_day = max_, day
        if self.min_temp > min_:
            self.min_temp, self.min_day = min_, day
        if self.max_humid < humid:
            self.max_humid, self.humid_day = humid, day


class Year(WeatherStats):
    def __init__(self, months, year):
        WeatherStats.__init__(self, year)
        self.months = months
        self.max_month = self.min_month = self.humid_month = 0
        self.annual_calculations()

    def annual_calculations(self):
        for month in self.months:
            if self.max_temp < month.max_temp:
                self.max_temp = month.max_temp
                self.max_day, self.max_month = month.max_day, month.month_num
            if self.min_temp > month.min_temp:
                self.min_temp = month.min_temp
                self.min_day, self.min_month = month.min_day, month.month_num
            if self.max_humid < month.max_humid:
                self.max_humid = month.max_humid
                self.humid_day = month.humid_day
                self.humid_month = month.month_num


class Weather:
    def __init__(self, path):
        self.path = path
        self.file_names = []
        self.years = []
        self.rows = []

    def load_stuff(self):
        self.get_file_names()
        self.read_rows()
        self.populate_records()

    def get_file_names(self):
        for root, dirs, files in os.walk(self.path):
            for file_name in sorted(files, key=yearly_sort):
                self.file_names.append(os.path.join(root, file_name))

    def read_rows(self):
        for file_name in self.file_names:
            with open(file_name) as file:
                next(file)
                csv_file = csv.DictReader(file)
                for line in skip_last_line(csv_file):
                    if not line["Min TemperatureC"] or \
                            not line["Max TemperatureC"] or \
                            not line["Max Humidity"]:
                        continue
                    self.rows.append(Day(str(line.get("PKT") or
                                             line.get("PKST")),
                                         int(line.get("Max TemperatureC")),
                                         int(line.get("Min TemperatureC")),
                                         int(line.get("Max Humidity"))))

    def populate_records(self):
        months, days = [], []
        prev_year, prev_month, day = date_split(self.rows[0].day)
        for row in self.rows:
            curr_year, curr_month, day = date_split(row.day)
            if prev_month != curr_month:
                months.append(Month(curr_year, int(prev_month), days))
                prev_month, days = curr_month, []
            days.append(Day(int(day), row.max_temp, row.min_temp, row.max_humid))
            if prev_year != curr_year:
                self.years.append(Year(months, prev_year))
                prev_year, months = curr_year, []

    def annual_report(self, year_str):
        for year in self.years:
            if year.year == year_str:
                print("Highest:", year.max_temp, "\bC on",
                      calendar.month_name[year.max_month], year.max_day)
                print("Lowest:", year.min_temp, "\bC on",
                      calendar.month_name[year.min_month], year.min_day)
                print("Humid:", year.max_humid, "\b% on",
                      calendar.month_name[year.humid_month], year.humid_day)
                break

    def find_month(self, year_str, month_str):
        for year in self.years:
            if year.year == year_str:
                for month in year.months:
                    if month.month_num == int(month_str):
                        return month

    def monthly_avg_report(self, year_str, month_str):
        month = self.find_month(year_str, month_str)
        print("Highest Average:", month.avg_temp_max, "\bC")
        print("Lowest Average:", month.avg_temp_min, "\bC")
        print("Average Humidity:", month.avg_humidity, "\b%")

    def month_chart_dual(self, year_str, month_str):
        month = self.find_month(year_str, month_str)
        print(calendar.month_name[int(month.month_num)], month.year, end="")
        for day in month.records:
            print("\033[1;31;47m")
            print("{:2}".format(day.day), "+" * day.max_temp,
                  "{}".format(day.max_temp), "\bC", end="")
            print("\033[1;34;47m")
            print("{:2}".format(day.day), "+" * day.min_temp,
                  "{}".format(day.min_temp), "\bC", end="")
        print("\n")

    def month_chart_bonus(self, year_str, month_str):
        month = self.find_month(year_str, month_str)
        print(calendar.month_name[month.month_num], month.year)
        for day in month.records:
            print("\033[1;30;47m", "{:2}".format(day.day), end=" ")
            print("\033[1;34;47m", "+" * day.min_temp, sep="", end="")
            print("\033[1;31;47m", "+" * (day.max_temp - day.min_temp),
                  sep="", end="")
            print("\033[1;30;47m", "{}".format(day.min_temp), "\bC -",
                  "{}".format(day.max_temp), "\bC")
        print("\n")


def cmd_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", help="Annual Report of Extreme Weather", nargs=2)
    parser.add_argument("-a", help="Monthly average", nargs=2)
    parser.add_argument("-c", help="Monthly Bar Chart", nargs=2)
    parser.add_argument("-b", help="Bonus Chart", nargs=2)
    return parser.parse_args()


def get_weather(path):
    weather = Weather(path)
    weather.load_stuff()
    return weather


def main():
    arg = cmd_parser()
    if arg.e:
        get_weather(arg.e[1]).annual_report(arg.e[0])
    elif arg.a:
        term = str(arg.a[0]).split("/")
        get_weather(arg.a[1]).monthly_avg_report(term[0], term[1])
    elif arg.c:
        term = str(arg.c[0]).split("/")
        get_weather(arg.c[1]).month_chart_dual(term[0], term[1])
    elif arg.b:
        term = str(arg.b[0]).split("/")
        get_weather(arg.b[1]).month_chart_bonus(term[0], term[1])

if __name__ == '__main__':
    main()

