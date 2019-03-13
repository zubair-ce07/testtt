"""Main Class for WeatherMan"""
import os
import calendar
import csv
from weatherattributes import WeatherAttributes
from datetime import datetime
import glob


class WeatherReport:

    def __init__(self):
        self.max_temp = None
        self.min_temp = None
        self.max_humidity = None
        self.max_temp_date = None
        self.min_temp_date = None
        self.max_humidity_date = None
        self.average_max_temp = None
        self.average_min_temp = None
        self.average_mean_humidity = None
        self.total_max_temp = 0
        self.total_min_temp = 0
        self.total_mean_humidity = 0

    def parse_file_name(self, args):
        for file_name in glob.glob(os.path.join(args.directory, '*.txt')):
            with open(file_name, "r") as reader:
                file_record = csv.DictReader(reader)
                for record in file_record:
                    weather_attribute = self.parse_weather_attributes(record)
                    self.calculate_weather_record(weather_attribute, args)

    def calculate_weather_record(self, weather_attribute, args):
        if args.year:
            self.calculate_annual_weather_report(weather_attribute, int(args.year))

        if args.year_month:
            year_month = args.year_month.split("/")
            year = year_month[0]
            month = year_month[1]
            self.calculate_monthly_weather_report(weather_attribute, int(year), self.parse_month_into_num(month[:3]))

        if args.year_month_chart:
            year_month = args.year_month_chart.split("/")
            year = year_month[0]
            month = year_month[1]
            self.calculate_monthly_temp_report(weather_attribute, int(year), self.parse_month_into_num(month[:3]))

        if args.year_month_bonus_chart:
            year_month = args.year_month_bonus_chart.split("/")
            year = year_month[0]
            month = year_month[1]
            self.calculate_monthly_temp_report_one_bar_chart(weather_attribute, int(year),
                                                             self.parse_month_into_num(month[:3]))

    def parse_weather_attributes(self, file_record):
        highest_temp = None
        lowest_temp = None
        most_humidity = None
        mean_humidity = None
        date = None

        date = datetime.strptime(file_record.get('PKT', file_record.get('PKST')), '%Y-%m-%d')

        """If conditions are added to check if valid attributes exists or not."""

        if file_record['Max TemperatureC'] != "":
            highest_temp = int(file_record['Max TemperatureC'])

        if file_record['Min TemperatureC'] != "":
            lowest_temp = int(file_record['Min TemperatureC'])

        if file_record['Max Humidity'] != "":
            most_humidity = int(file_record['Max Humidity'])

        if file_record[' Mean Humidity'] != "":
            mean_humidity = int(file_record[' Mean Humidity'])

        return WeatherAttributes(date=date, max_temp=highest_temp, min_temp=lowest_temp
                                 , max_humidity=most_humidity, mean_humidity=mean_humidity)

    def calculate_annual_weather_report(self, weather_attribute, year):
        if year == weather_attribute.date.year:
            if self.max_temp == None or weather_attribute.max_temp and weather_attribute.max_temp > int(
                    self.max_temp):
                self.max_temp_date = weather_attribute.date
                self.max_temp = weather_attribute.max_temp

            if self.min_temp == None or weather_attribute.min_temp and weather_attribute.min_temp < int(
                    self.min_temp):
                self.min_temp_date = weather_attribute.date
                self.min_temp = weather_attribute.min_temp

            if (self.max_humidity == None or weather_attribute.max_humidity and
                    weather_attribute.max_humidity > int(self.max_humidity)):
                self.max_humidity_date = weather_attribute.date
                self.max_humidity = weather_attribute.max_humidity

    def calculate_monthly_weather_report(self, weather_attributes, year, month):
        if year == weather_attributes.date.year and month == weather_attributes.date.month:
            if weather_attributes.max_temp:
                self.total_max_temp = self.total_max_temp + weather_attributes.max_temp

            if weather_attributes.min_temp:
                self.total_min_temp = self.total_min_temp + weather_attributes.min_temp

            if weather_attributes.mean_humidity:
                self.total_mean_humidity = self.total_mean_humidity + weather_attributes.mean_humidity

            self.average_max_temp = self.calculate_average(self.total_max_temp, weather_attributes.date)
            self.average_min_temp = self.calculate_average(self.total_min_temp, weather_attributes.date)
            self.average_mean_humidity = self.calculate_average(self.total_mean_humidity, weather_attributes.date)

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

    def calculate_monthly_temp_report(self, weather_attributes, year, month):
        if (year == weather_attributes.date.year and month == weather_attributes.date.month
                and weather_attributes.max_temp and weather_attributes.min_temp):
            self.print_monthly_temp_report(weather_attributes.date.day, weather_attributes.max_temp,
                                           weather_attributes.min_temp)

    def calculate_monthly_temp_report_one_bar_chart(self, weather_attributes, year, month):
        if (year == weather_attributes.date.year and month == weather_attributes.date.month and
                weather_attributes.max_temp and weather_attributes.min_temp):
            self.print_monthly_temp_report_one_bar_chart(weather_attributes.date.day, weather_attributes.max_temp,
                                                         weather_attributes.min_temp)

    def print_monthly_temp_report(self, date, weather_max_temp, weather_min_temp):
        print("\x1b[30m{} \x1b[31m{} \x1b[30m{}".format(date, ('+' * weather_max_temp), weather_max_temp))
        print("\x1b[30m{} \x1b[94m{} \x1b[30m{}".format(date, ('+' * weather_min_temp), weather_min_temp))

    def print_monthly_temp_report_one_bar_chart(self, date, weather_max_temp, weather_min_temp):
        print("\x1b[30m{} \x1b[94m{}\x1b[31m{} \x1b[30m{}-\x1b[30m{}".format(date, ('+' * weather_min_temp),
                                                                             ('+' * weather_max_temp), weather_min_temp,
                                                                             weather_max_temp))

