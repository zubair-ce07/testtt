"""Main Class for WeatherMan"""
import os
import calendar
import csv
from weatherattributes import WeatherAttributes
from collections import defaultdict
from datetime import datetime


class WeatherReport:

    def __init__(self):
        self.annual_report = defaultdict(lambda: WeatherAttributes())
        self.average_max_temp = ""
        self.average_min_temp = ""
        self.average_mean_humidity = ""

    def parse_file_name(self, args):
        files = os.listdir(args.data_dir)
        is_file = False

        for file_name in files:
            if args.year and file_name.endswith('.txt'):
                is_file = True
                with open(file_name, "r") as reader:
                    file_data = csv.DictReader(reader)
                    self.calculate_weather_data(file_data, args.year)

            if args.year_month and file_name.endswith('.txt'):
                year_month = args.year_month.split("/")
                year = year_month[0]
                month = year_month[1]
                is_file = True
                with open(file_name, "r") as reader:
                    file_data = csv.DictReader(reader)
                    self.calculate_monthly_weather_report(file_data, int(year), self.parse_month_into_num(month[:3]))

            if args.year_month_chart and file_name.endswith('.txt'):
                year_month = args.year_month_chart.split("/")
                year = year_month[0]
                month = year_month[1]

                is_file = True
                with open(file_name, "r") as reader:
                    file_data = csv.DictReader(reader)
                    self.calculate_monthly_temp_report(file_data, int(year), self.parse_month_into_num(month[:3]))

            if args.year_month_bonus_chart and file_name.endswith('.txt'):
                year_month = args.year_month_bonus_chart.split("/")
                year = year_month[0]
                month = year_month[1]

                is_file = True
                with open(file_name, "r") as reader:
                    file_data = csv.DictReader(reader)
                    self.calculate_monthly_temp_report_one_bar_chart(file_data, int(year),
                                                                     self.parse_month_into_num(month[:3]))
        return is_file

    def calculate_weather_data(self, file_data, year):
        for weather_attr in file_data:
            date = weather_attr.get('PKT', weather_attr.get('PKST'))

            if date and year in date:
                weather_data = WeatherAttributes(**weather_attr)
                annual_data = self.annual_report[year]

                if (annual_data.max_temp == 200 or
                        weather_data.max_temp != 200 and weather_data.max_temp > annual_data.max_temp):
                    self.annual_report[year].max_temp_date = weather_data.max_temp_date
                    self.annual_report[year].max_temp = weather_data.max_temp

                if (annual_data.min_temp == 200 or
                        weather_data.min_temp != 200 and weather_data.min_temp < annual_data.min_temp):
                    self.annual_report[year].min_temp_date = weather_data.min_temp_date
                    self.annual_report[year].min_temp = weather_data.min_temp

                if (annual_data.max_humidity == 200 or
                        weather_data.max_humidity != 200 and weather_data.max_humidity > annual_data.max_humidity):
                    self.annual_report[year].max_humidity_date = weather_data.max_humidity_date
                    self.annual_report[year].max_humidity = weather_data.max_humidity

    def calculate_monthly_weather_report(self, file_data, year, month):
        total_max_temp = 0
        total_min_temp = 0
        total_mean_humidity = 0

        for data in file_data:
            weather_data = WeatherAttributes(**data)
            date = self.parse_date(weather_data.date)

            if year == date.year and month == date.month:
                if weather_data.max_temp != 200:
                    total_max_temp = total_max_temp + weather_data.max_temp

                if weather_data.min_temp != 200:
                    total_min_temp = total_min_temp + weather_data.min_temp

                if weather_data.mean_humidity != 200:
                    total_mean_humidity = total_mean_humidity + weather_data.mean_humidity

                self.average_max_temp = self.calculate_average(total_max_temp, date)
                self.average_min_temp = self.calculate_average(total_min_temp, date)
                self.average_mean_humidity = self.calculate_average(total_mean_humidity, date)

    def calculate_average(self, average, date):
        return average / self.month_range(date.year, date.month)

    def parse_month(self, date):
        day = date.split("-")
        month_name = calendar.month_abbr[int(day[1])]
        return month_name + " " + day[2]

    def parse_date(self, date):
        return datetime.strptime(date, '%Y-%m-%d')

    def month_range(self, year, month):
        return calendar.monthrange(year, month)[1]

    def parse_month_into_num(self, month):
        abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
        return abbr_to_num[month]

    def print_annual_report(self):
        print('-' * 50)
        for year, weather_att in self.annual_report.items():
            print("Highest: {}C on {}".format(weather_att.max_temp, self.parse_month(weather_att.max_temp_date)))
            print("Lowest: {}C on {}".format(weather_att.min_temp, self.parse_month(weather_att.min_temp_date)))
            print(
                "Humidity: {}% on {}".format(weather_att.max_humidity, self.parse_month(weather_att.max_humidity_date)))
        print('-' * 50)

    def print_monthly_average_report(self):
        print('-' * 50)
        print("Highest Average: {}C ".format(int(self.average_max_temp)))
        print("Lowest Average: {}C ".format(int(self.average_min_temp)))
        print("Humidity Mean Average: {}% ".format(int(self.average_mean_humidity)))
        print('-' * 50)

    def calculate_monthly_temp_report(self, file_data, year, month):
        for data in file_data:
            weather_data = WeatherAttributes(**data)
            date = self.parse_date(weather_data.date)

            if year == date.year and month == date.month and weather_data.max_temp != 200 and weather_data.min_temp != 200:
                self.print_monthly_temp_report(date.day, weather_data.max_temp, weather_data.min_temp)

    def calculate_monthly_temp_report_one_bar_chart(self, file_data, year, month):
        for data in file_data:
            weather_data = WeatherAttributes(**data)
            date = self.parse_date(weather_data.date)

            if year == date.year and month == date.month and weather_data.max_temp != 200 and weather_data.min_temp != 200:
                self.print_monthly_temp_report_one_bar_chart(date.day, weather_data.max_temp, weather_data.min_temp)

    def print_monthly_temp_report(self, date, weather_max_temp, weather_min_temp):
        max_bar_count = int(weather_max_temp)
        print("\x1b[30m{} \x1b[31m{} \x1b[30m{}".format(date, ('+' * max_bar_count), weather_max_temp))

        min_bar_count = int(weather_min_temp)
        print("\x1b[30m{} \x1b[94m{} \x1b[30m{}".format(date, ('+' * min_bar_count), weather_min_temp))

    def print_monthly_temp_report_one_bar_chart(self, date, weather_max_temp, weather_min_temp):
        max_bar_count = weather_max_temp
        min_bar_count = weather_min_temp
        print("\x1b[30m{} \x1b[94m{}\x1b[31m{} \x1b[30m{}-\x1b[30m{}".format(date, ('+' * min_bar_count),
                                                                             ('+' * max_bar_count), weather_min_temp,
                                                                             weather_max_temp))
