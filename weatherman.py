"""Main Class for WeatherMan"""
import os
import calendar
import csv
from weatherattributes import WeatherAttributes
from collections import defaultdict
from datetime import datetime


class WeatherMan:
    average_max_temp = ""
    average_min_temp = ""
    average_mean_humidity = ""

    def __init__(self):
        self.annual_report = defaultdict(lambda: WeatherAttributes())

    def parse_file_name(self, args):

        files = os.listdir(args.data_dir)
        is_file = False

        for file_name in files:

            if args.year and file_name.__contains__(args.year):
                is_file = True
                with open("%s" % file_name, "r") as reader:
                    file_data = csv.DictReader(reader)
                    self.calculate_weather_data(file_data, args.year)

            if args.year_month:
                year_month = args.year_month.split("/")
                year = year_month[0]
                month = year_month[1]

                if file_name.__contains__(year) and month[:3].lower() in file_name.lower():
                    is_file = True
                    with open("%s" % file_name, "r") as reader:
                        file_data = csv.DictReader(reader)
                        self.calculate_monthly_weather_report(file_data)

            if args.year_month_chart:
                year_month = args.year_month_chart.split("/")
                year = year_month[0]
                month = year_month[1]

                if year in file_name and month[:3].lower() in file_name.lower():
                    is_file = True
                    with open("%s" % file_name, "r") as reader:
                        file_data = csv.DictReader(reader)
                        self.print_monthly_temp_report(file_data, year, month)

            if args.year_month_bonus_chart:
                year_month = args.year_month_bonus_chart.split("/")
                year = year_month[0]
                month = year_month[1]

                if file_name.__contains__(year) and month[:3].lower() in file_name.lower():
                    is_file = True
                    with open("%s" % file_name, "r") as reader:
                        file_data = csv.DictReader(reader)
                        self.print_monthly_temp_report_one_bar_chart(file_data, year, month)
        return is_file

    def calculate_weather_data(self, file_data, year):
        for weather_attr in file_data:

            weather_data = WeatherAttributes(**weather_attr)
            annual_data = self.annual_report[year]

            if (annual_data.max_temp == 'None' or
                    weather_data.max_temp and int(weather_data.max_temp) > int(annual_data.max_temp)):
                self.annual_report[year].max_temp_date = weather_data.max_temp_date
                self.annual_report[year].max_temp = weather_data.max_temp

            if (annual_data.min_temp == 'None' or
                    weather_data.min_temp and int(weather_data.min_temp) < int(annual_data.min_temp)):
                self.annual_report[year].min_temp_date = weather_data.min_temp_date
                self.annual_report[year].min_temp = weather_data.min_temp

            if (annual_data.max_humidity == 'None' or
                    weather_data.max_humidity and int(weather_data.max_humidity) > int(
                        annual_data.max_humidity)):
                self.annual_report[year].max_humidity_date = weather_data.max_humidity_date
                self.annual_report[year].max_humidity = weather_data.max_humidity

    def calculate_monthly_weather_report(self, file_data):
        total_max_temp = 0
        total_min_temp = 0
        total_mean_humidity = 0

        for data in file_data:
            weather_data = WeatherAttributes(**data)
            date = datetime.strptime(weather_data.date, '%Y-%m-%d')

            if weather_data.max_temp:
                total_max_temp = total_max_temp + int(weather_data.max_temp)

            if weather_data.min_temp:
                total_min_temp = total_min_temp + int(weather_data.min_temp)

            if weather_data.mean_humidity:
                total_mean_humidity = total_mean_humidity + int(weather_data.mean_humidity)

        self.average_max_temp = self.calculate_average(total_max_temp, date)
        self.average_min_temp = self.calculate_average(total_min_temp, date)
        self.average_mean_humidity = self.calculate_average(total_mean_humidity, date)

    def calculate_average(self, average, date):
        return average / self.month_range(int(date.year), int(date.month))

    def parse_month(self, date):
        day = date.split("-")
        month_name = calendar.month_abbr[int(day[1])]
        return month_name + " " + day[2]

    def month_range(self, year, month):
        return calendar.monthrange(year, month)[1]

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

    def print_monthly_temp_report(self, file_data, year, month):
        print(month + " " + year + "\n")
        for data in file_data:
            weather_data = WeatherAttributes(**data)
            date = datetime.strptime(weather_data.date, '%Y-%m-%d').day

            if weather_data.max_temp:
                max_bar_count = int(weather_data.max_temp)
                print("\x1b[30m" + str(date) + "\x1b[31m" + ('+' * max_bar_count) + "\x1b[30m" + weather_data.max_temp)

            if weather_data.min_temp:
                min_bar_count = int(weather_data.min_temp)
                print("\x1b[30m" + str(date) + "\x1b[94m" + ('+' * min_bar_count) + "\x1b[30m" + weather_data.min_temp)

    def print_monthly_temp_report_one_bar_chart(self, file_data, year, month):
        print(month + " " + year + "\n")
        for data in file_data:
            weather_data = WeatherAttributes(**data)
            date = datetime.strptime(weather_data.date, '%Y-%m-%d').day

            if weather_data.max_temp and weather_data.min_temp:
                max_bar_count = int(weather_data.max_temp)
                min_bar_count = int(weather_data.min_temp)

                print("\x1b[30m" + str(date) + "\x1b[94m" + ('+' * min_bar_count)
                      + "\x1b[31m" + ('+' * max_bar_count) + "\x1b[30m" + weather_data.min_temp
                      + "-" + "\x1b[30m" + weather_data.max_temp)
