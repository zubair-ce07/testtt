#!/usr/bin/env python3
import os
import pandas
import calendar
import datetime
import argparse
from termcolor import colored
import math

__author__ = 'ruhaib'


class WeatherData:
    'Class to extract weather data from the desired path'
    def __init__(self, arguments):
        self.arguments = arguments
        self.file_names_in_path = pandas.DataFrame(os.listdir(arguments.path))

    def show_task1_requirements(self):

        files_names_of_year = self.file_names_in_path[
            self.file_names_in_path[0].str.contains("lahore_weather_"+str(self.arguments.e))]

        max_temp = -100000
        max_date = 0
        max_month = 'Jan'
        min_temp = 100000
        min_date = 0
        min_month = 'jan'
        humid = -100000
        humid_date = 100000
        humid_month = 'jan'

        for index, row in files_names_of_year.iterrows():

            data_of_month = pandas.read_csv(self.arguments.path+"/"+row[0], header=0)

            if(data_of_month['Max TemperatureC'].max() > max_temp):
                temp_max_temperature = data_of_month.loc[
                    data_of_month['Max TemperatureC'] == data_of_month['Max TemperatureC'].max()]
                max_temp = data_of_month['Max TemperatureC'].max()
                date = datetime.datetime.strptime(
                    temp_max_temperature[temp_max_temperature.columns[0]].iloc[0], "%Y-%m-%d")
                max_date = date.day
                max_month = calendar.month_name[date.month]

            if(data_of_month['Min TemperatureC'].min() < min_temp):
                min_temp = data_of_month['Min TemperatureC'].min()
                temp_max_temperature = data_of_month.loc[
                    data_of_month['Min TemperatureC'] == data_of_month['Min TemperatureC'].min()]
                date = datetime.datetime.strptime(
                    temp_max_temperature[temp_max_temperature.columns[0]].iloc[0], "%Y-%m-%d")
                min_date = date.day
                min_month = calendar.month_name[date.month]

            if(data_of_month['Max Humidity'].max() > humid):
                humid = data_of_month['Max Humidity'].max()
                temp_max_temperature = data_of_month.loc[
                    data_of_month['Max Humidity'] == data_of_month['Max Humidity'].max()]
                date = datetime.datetime.strptime(
                    temp_max_temperature[temp_max_temperature.columns[0]].iloc[0], "%Y-%m-%d")
                humid_date = date.day
                humid_month = calendar.month_name[date.month]

        print("Highest: %dC on %s %d" % (max_temp, max_month, max_date))
        print("Lowest: %dC on %s %d" % (min_temp, min_month, min_date))
        print("Humid: %d%% on %s %d" % (humid, humid_month, humid_date))

    def show_task2_requirements(self):

        date = self.arguments.a
        y = int(date.split("/")[0])

        # extracting path of the file required
        temp_data_frame = self.file_names_in_path[self.file_names_in_path[0].str.contains(
            "lahore_weather_"+str(y))]

        abbr = calendar.month_abbr[int(date.split("/")[1])]

        month_file_filename = self.arguments.path+"/" + temp_data_frame[
            temp_data_frame[0].str.contains("lahore_weather_" + str(y) +
                                            "_" + abbr)][0].iloc[0]

        month_data = pandas.read_csv(month_file_filename, header=0)

        # extracting average highest temperature
        max_temp = month_data[month_data.columns[2]].max()

        # extracting average lowest temperature
        min_temp = month_data[month_data.columns[2]].min()

        # extracting average humidity
        humid = month_data[month_data.columns[8]].sum()/month_data[month_data.columns[8]].count()

        print("Highest Average: %dC" % max_temp)
        print("Lowest Average: %dC" % min_temp)
        print("Average Humidity: %d%%" % humid)

    def show_task3_graphs(self):

        date = self.arguments.c
        y = int(date.split("/")[0])

        # extracting path of the file required
        temp_data_frame = self.file_names_in_path[self.file_names_in_path[0].str.contains(
            "lahore_weather_"+str(y))]

        abbr = calendar.month_name[int(date.split("/")[1])]

        print("%s %d" % (abbr, y))

        abbr = calendar.month_abbr[int(date.split("/")[1])]

        month_file_name = self.arguments.path+"/"+temp_data_frame[
            temp_data_frame[0].str.contains(
                "lahore_weather_"+str(y)+"_"+abbr)][0].iloc[0]

        month_data = pandas.read_csv(month_file_name, header=0)

        for index, row in month_data.iterrows():

            if (not (math.isnan(row[3]))) and (not (math.isnan(row[1]))):
                print(row[0].split("-")[2], end=" ")
                print(' ', end=" ")
                text = ""

                for i in range(0, int(row[3])):
                    text += colored('+', "blue")
                    print(text, end=' ')

                text = ""

                for i in range(0, int(row[1])):
                    text += colored('+', "red")
                    print(text, end=' ')

                print("%dC - %dC" % (row[3], row[1]))


def year_range(string):

    if (string.find('/') == -1):

        year_passed = int(string)

        if(year_passed > 2011 or year_passed < 1996):
            msg = '%r year passed is out of range' % string
            raise argparse.ArgumentTypeError(msg)

        return year_passed

    else:

        msg = '%r only year is required the input is incorrect' % string
        raise argparse.ArgumentTypeError(msg)


def year_month_validity(string):

    if(string.count('/') != 1):
        msg = '%r incorrect month and year passed' % string
        raise argparse.ArgumentTypeError(msg)

    year_passed = int(string.split("/")[0])
    month_passed = int(string.split("/")[1])

    if(year_passed > 2011 or year_passed < 1996):
        msg = "%r year passed is out of range" % string
        raise argparse.ArgumentTypeError(msg)

    if(month_passed > 12 or month_passed < 1):
        msg = "%r month, passed is out of range" % string
        raise argparse.ArgumentTypeError(msg)

    return string


def main():

    parser = argparse.ArgumentParser(description='WeatherMan data extraction.')

    parser.add_argument(
        '-e', type=year_range,
        help='(usage: -e yyyy) to see maximum temperature,'
             ' minimum temperature and humidity')

    parser.add_argument(
        '-a', type=year_month_validity,
        help='(usage: -a yyyy/mm) to see average maximum, average minimum'
             ' temperature and mean humidity of the month')

    parser.add_argument(
        '-c', type=year_month_validity,
        help='(usage: -c yyyy/mm) to see horizontal bar chart'
             ' of highest and lowest temperature on each day')

    parser.add_argument('path',
                        help='path to the files having weather data')

    args = parser.parse_args()

    if not (os.path.isdir(args.path)):
        print("path to directory does not exist")
        quit()

    weather_data = WeatherData(args)

    if args.e:

        weather_data.show_task1_requirements()

    if args.a:

        weather_data.show_task2_requirements()

    if args.c:

        weather_data.show_task3_graphs()


if __name__ == "__main__":
    main()
