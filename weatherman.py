import sys

import os

import csv

import datetime

import argparse

import calendar


class WeatherMan:
    def __init__(self):
        return

    @staticmethod
    def generate_annual_report(filename_list):

        high_temp = 0
        high_temp_date = ""

        low_temp = ''
        low_temp_date = ""

        max_humidity = 0
        most_humid_day = ""

        for temperature_file in filename_list:
            if os.path.isfile(temperature_file):
                header = WeatherMan(). \
                    read_csv_file(temperature_file).fieldnames

                for row in WeatherMan().read_csv_file(temperature_file):
                    if row['Max TemperatureC'] != '' \
                            and int(row['Max TemperatureC']) >= high_temp:
                        high_temp = int(row['Max TemperatureC'])
                        high_temp_date = str(row[header[0]])

                for row in WeatherMan().read_csv_file(temperature_file):
                    if row['Min TemperatureC'] != '' \
                            and int(row['Min TemperatureC']) <= low_temp:
                        low_temp = int(row['Min TemperatureC'])
                        low_temp_date = str(row[header[0]])

                for row in WeatherMan().read_csv_file(temperature_file):
                    if row['Max Humidity'] != '' \
                            and int(row['Max Humidity']) >= max_humidity:
                        max_humidity = int(row['Max Humidity'])
                        most_humid_day = str(row[header[0]])

        date_to_month = high_temp_date.split('-')
        month_of_highest = int(date_to_month[1])
        day_of_highest = date_to_month[2]
        print("Highest: " + str(high_temp) +
              "C on " + year_month[month_of_highest - 1] +
              " " + str(day_of_highest))

        date_to_month = low_temp_date.split('-')
        month_of_lowest = int(date_to_month[1])
        day_of_lowest = date_to_month[2]
        print("Lowest: " + str(low_temp) + "C on " +
              year_month[month_of_lowest - 1] + " " +
              str(day_of_lowest))

        date_to_month = most_humid_day.split('-')
        month_of_humidity = int(date_to_month[1])
        day_of_humidity = date_to_month[2]

        print("Humidity: " + str(max_humidity) +
              "% on " + year_month[month_of_humidity - 1] +
              " " + str(day_of_humidity))

    @staticmethod
    def generate_monthly_report(filename):
        daily_maximum_temperature = []
        daily_minimum_temperature = []
        daily_mean_humidity = []
        if os.path.isfile(filename):
            file_reader = WeatherMan().read_csv_file(filename)
            header = file_reader.fieldnames
            for row in file_reader:
                if row['Max TemperatureC'] != '':
                    daily_maximum_temperature.append(int(row[header[1]]))
                if row['Min TemperatureC'] != '':
                    daily_minimum_temperature.append(int(row[header[3]]))
                if row[' Mean Humidity'] != '':
                    daily_mean_humidity.append(int(row[header[8]]))
            highest_average = int(sum(daily_maximum_temperature) /
                                  len(daily_maximum_temperature))
            lowest_average = int(sum(daily_minimum_temperature) /
                                 len(daily_minimum_temperature))
            daily_mean_humidity = int(sum(daily_mean_humidity) /
                                      len(daily_mean_humidity))

            print("Highest Average: " + str(highest_average) + "C")
            print("Lowest Average : " + str(lowest_average) + "C")
            print ("Average Mean Humidity: " +
                   str(daily_mean_humidity) + "%")

    @staticmethod
    def generate_monthly_bar_chart(filename):
        if os.path.isfile(filename):
            day_counter = 1
            file_reader = WeatherMan().read_csv_file(filename)
            for row in file_reader:
                if row['Max TemperatureC'] != '':
                    highest_temp = int(row['Max TemperatureC'])
                    red_text = "+" * highest_temp
                    red_color_bar = "\033[1;31m" + \
                                    red_text + \
                                    "\033[1;m"
                    print(str(day_counter) +
                          red_color_bar +
                          str(highest_temp))
                if row['Min TemperatureC'] != '':
                    lowest_temp = int(row['Min TemperatureC'])
                    blue_text = "+" * lowest_temp
                    blue_color_bar = "\033[1;34m" + \
                                     blue_text + \
                                     "\033[1;m"
                    print(str(day_counter) +
                          blue_color_bar +
                          str(lowest_temp))
                day_counter += 1
        return

    @staticmethod
    def generate_monthly_oneline_chart(filename):
        if os.path.isfile(filename):
            day_counter = 1
            file_reader = WeatherMan().read_csv_file(filename)
            for row in file_reader:

                if row['Max TemperatureC'] != '':
                    highest_temp = row['Max TemperatureC']
                    red_text = "+" * int(highest_temp)
                    red_color_bar = "\033[1;31m" + \
                                    red_text + "\033[1;m"
                if row['Min TemperatureC'] != '':
                    lowest_temp = row['Min TemperatureC']
                    blue_text = "+" * int(lowest_temp)
                    blue_color_bar = "\033[1;34m" + \
                                     blue_text + "\033[1;m"
                    print(str(day_counter) + blue_color_bar +
                          red_color_bar + lowest_temp + "-" +
                          highest_temp)
                    day_counter += 1
        else:
            print ("No such file found")
        return

    @staticmethod
    def read_csv_file(filename):
        if os.path.isfile(filename):
            with open(filename, 'r') as csvfile:
                next(csvfile)
                file_reader = csv.DictReader(
                    filter(lambda row: row[0] != '<', csvfile)
                )
                return file_reader


if __name__ == '__main__':

    year_month = [month for month in calendar.month_abbr]
    year_month.pop(0)
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-e", "--annual", action="store_true")
    group.add_argument("-a", "--monthly", action="store_true")
    group.add_argument("-c", "--bar_chart", action="store_true")
    group.add_argument("-c4", "--oneline_chart", action="store_true")
    parser.add_argument("report_date", help="Path of folder containing Temperature record")
    parser.add_argument("path_to_file", help="Path of folder containing Temperature record")
    args = parser.parse_args()

    files_in_dir = [file for file in os.listdir(args.path_to_file)]
    file_dir_name = []

    if (args.annual):
        year = args.report_date
        if len(str(args.report_date).split('/')) > 1:
            print("invalid date .Please enter in YYYY format")
            sys.exit()
        file_list = []
        for filename in files_in_dir:
            if (filename.__contains__(args.report_date)):
                file_prefix = args.path_to_file + "/" + filename
                file_list.append(file_prefix)
        WeatherMan().generate_annual_report(file_list)

    else:
        yearPlusMonth = str(args.report_date).split('/')
        if len(yearPlusMonth) < 2:
            print("invalid month or date .Please enter in YYYY/MM format")
            sys.exit()
        year = yearPlusMonth[0]
        month = int(yearPlusMonth[1])
        if month > 12 or month < 1:
            print("invalid month")
            sys.exit()
        fileprefix = ""
        for filename in files_in_dir:
            if (filename.__contains__(year_month[month - 1])) and filename.__contains__(year):
                file_prefix = args.path_to_file + "/" + filename

        if (args.monthly):
            WeatherMan().generate_monthly_report(file_prefix)
        else:
            if (args.bar_chart):
                WeatherMan().generate_monthly_bar_chart(file_prefix)
            else:
                if (args.oneline_chart):
                    WeatherMan().generate_monthly_oneline_chart(file_prefix)

