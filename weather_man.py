"""Main Class for WeatherMan"""
import os
import calendar
import csv
from weatherattributes import WeatherAttributes


class WeatherReport:

    def __init__(self):
        self.max_temp = ""
        self.min_temp = ""
        self.max_humidity = ""
        self.max_temp_date = ""
        self.min_temp_date = ""
        self.max_humidity_date = ""
        self.average_max_temp = ""
        self.average_min_temp = ""
        self.average_mean_humidity = ""

    def parse_file_name(self, args):
        files = os.listdir(args.data_dir)
        is_file = False

        for file_name in files:
            if file_name.endswith('.txt'):
                is_file = True
                with open(file_name, "r") as reader:
                    file_data = csv.DictReader(reader)
                    self.weather_readings(file_data, args)

        return is_file

    def weather_readings(self, file_data, args):
        if args.year:
            self.calculate_annual_weather_report(file_data, int(args.year))

        if args.year_month:
            year_month = args.year_month.split("/")
            year = year_month[0]
            month = year_month[1]
            self.calculate_monthly_weather_report(file_data, int(year), self.parse_month_into_num(month[:3]))

        if args.year_month_chart:
            year_month = args.year_month_chart.split("/")
            year = year_month[0]
            month = year_month[1]
            self.calculate_monthly_temp_report(file_data, int(year), self.parse_month_into_num(month[:3]))

        if args.year_month_bonus_chart:
            year_month = args.year_month_bonus_chart.split("/")
            year = year_month[0]
            month = year_month[1]
            self.calculate_monthly_temp_report_one_bar_chart(file_data, int(year), self.parse_month_into_num(month[:3]))

    def calculate_annual_weather_report(self, file_data, year):
        for weather_attr in file_data:
            weather_data = WeatherAttributes(**weather_attr)

            if hasattr(weather_data, 'date'):
                if year == weather_data.date.year:
                    if self.max_temp == '' or weather_data.max_temp and weather_data.max_temp > int(self.max_temp):
                        self.max_temp_date = weather_data.max_temp_date
                        self.max_temp = weather_data.max_temp

                    if self.min_temp == '' or weather_data.min_temp and weather_data.min_temp < int(self.min_temp):
                        self.min_temp_date = weather_data.min_temp_date
                        self.min_temp = weather_data.min_temp

                    if (self.max_humidity == '' or weather_data.max_humidity and
                            weather_data.max_humidity > int(self.max_humidity)):
                        self.max_humidity_date = weather_data.max_humidity_date
                        self.max_humidity = weather_data.max_humidity

    def calculate_monthly_weather_report(self, file_data, year, month):
        total_max_temp = 0
        total_min_temp = 0
        total_mean_humidity = 0

        for data in file_data:
            weather_data = WeatherAttributes(**data)
            if hasattr(weather_data, 'date'):
                if year == weather_data.date.year and month == weather_data.date.month:
                    if weather_data.max_temp:
                        total_max_temp = total_max_temp + weather_data.max_temp

                    if weather_data.min_temp:
                        total_min_temp = total_min_temp + weather_data.min_temp

                    if weather_data.mean_humidity:
                        total_mean_humidity = total_mean_humidity + weather_data.mean_humidity

                    self.average_max_temp = self.calculate_average(total_max_temp, weather_data.date)
                    self.average_min_temp = self.calculate_average(total_min_temp, weather_data.date)
                    self.average_mean_humidity = self.calculate_average(total_mean_humidity, weather_data.date)

    def calculate_average(self, average, date):
        return average / self.month_range(date.year, date.month)

    def parse_month(self, month):
        return calendar.month_abbr[month]

    def month_range(self, year, month):
        return calendar.monthrange(year, month)[1]

    def parse_month_into_num(self, month):
        abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
        return abbr_to_num[month]

    def print_annual_report(self):
        print('-' * 50)
        print("Highest: {}C on {} {}".format(self.max_temp, self.parse_month(self.max_temp_date.month),
                                             self.max_temp_date.day))
        print("Lowest: {}C on {} {}".format(self.min_temp, self.parse_month(self.min_temp_date.month),
                                            self.min_temp_date.day))
        print("Humidity: {}% on {} {}".format(self.max_humidity, self.parse_month(self.max_humidity_date.month),
                                              self.max_temp_date.day))
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
            if hasattr(weather_data, 'date'):
                if (year == weather_data.date.year and month == weather_data.date.month
                        and weather_data.max_temp and weather_data.min_temp):
                    self.print_monthly_temp_report(weather_data.date.day, weather_data.max_temp, weather_data.min_temp)

    def calculate_monthly_temp_report_one_bar_chart(self, file_data, year, month):
        for data in file_data:
            weather_data = WeatherAttributes(**data)
            if hasattr(weather_data, 'date'):
                if (year == weather_data.date.year and month == weather_data.date.month and
                        weather_data.max_temp and weather_data.min_temp):
                    self.print_monthly_temp_report_one_bar_chart(weather_data.date.day, weather_data.max_temp,
                                                                 weather_data.min_temp)

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

