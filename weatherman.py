#!/usr/bin/env python3
import os
import argparse
import calendar
import datetime
import math
import pandas

from termcolor import colored


__author__ = 'ruhaib'


class WeatherData:
    'Class to extract weather data from the desired path'

    def __init__(self, data):
        self.data = data

    def show_task1_results(self, data_dict):
        print("Highest: %dC on %s %d" %
              (data_dict['max'][0], data_dict['max'][1], data_dict['max'][2]))
        print("Lowest: %dC on %s %d" %
              (data_dict['min'][0], data_dict['min'][1], data_dict['min'][2]))
        print("Humid: %d%% on %s %d" %
              (data_dict['humid'][0], data_dict['humid'][0], data_dict['humid'][0]))

    def show_task1_requirements(self):

        max_temp = -100000
        max_date = 0
        max_month = 'Jan'
        min_temp = 100000
        min_date = 0
        min_month = 'jan'
        humid = -100000
        humid_date = 100000
        humid_month = 'jan'

        for data_of_month in self.data:
            if data_of_month['Max TemperatureC'].max() > max_temp:

                max_temp = data_of_month['Max TemperatureC'].max()

                temp_max_temperature = data_of_month.loc[
                    data_of_month['Max TemperatureC'] == max_temp]

                if 'PKT' in temp_max_temperature.columns:

                    date = datetime.datetime.strptime(
                        temp_max_temperature['PKT'].iloc[0], "%Y-%m-%d")
                else:
                    date = datetime.datetime.strptime(
                        temp_max_temperature['PKST'].iloc[0], "%Y-%m-%d")

                max_date = date.day
                max_month = calendar.month_name[date.month]

            if data_of_month['Min TemperatureC'].min() < min_temp:
                min_temp = data_of_month['Min TemperatureC'].min()

                temp_max_temperature = data_of_month.loc[
                    data_of_month['Min TemperatureC'] == min_temp]

                if 'PKT' in temp_max_temperature.columns:
                    date = datetime.datetime.strptime(
                        temp_max_temperature.PKT.iloc[0], "%Y-%m-%d")
                else:
                    date = datetime.datetime.strptime(
                        temp_max_temperature.PKST.iloc[0], "%Y-%m-%d")

                min_date = date.day
                min_month = calendar.month_name[date.month]

            if data_of_month['Max Humidity'].max() > humid:
                humid = data_of_month['Max Humidity'].max()

                temp_max_temperature = data_of_month.loc[
                    data_of_month['Max Humidity'] == humid]

                if 'PKT' in temp_max_temperature.columns:
                    date = datetime.datetime.strptime(
                        temp_max_temperature.PKT.iloc[0], "%Y-%m-%d")
                else:
                    date = datetime.datetime.strptime(
                        temp_max_temperature.PKST.iloc[0], "%Y-%m-%d")

                humid_date = date.day
                humid_month = calendar.month_name[date.month]
        max_temperature_data = [max_temp, max_month, max_date]
        min_temperature_data = [min_temp, min_month, min_date]
        humid_data = [humid, humid_month, humid_date]
        data_dict = {'max': max_temperature_data, 'min': min_temperature_data,
                     'humid': humid_data}

        self.show_task1_results(data_dict)

    def show_task2_results(self, task2_data):
        print("Highest Average: %dC" % task2_data['max_temp'])
        print("Lowest Average: %dC" % task2_data['min_temp'])
        print("Average Humidity: %d%%" % task2_data['humid'])

    def show_task2_requirements(self):
        for month_data in self.data:

            # extracting average highest temperature
            max_temp = month_data[month_data.columns[2]].max()

            # extracting average lowest temperature
            min_temp = month_data[month_data.columns[2]].min()

            # extracting average humidity
            humid = month_data[month_data.columns[8]].sum(
            ) / month_data[month_data.columns[8]].count()

            task2_data = {'max_temp': max_temp,
                          'min_temp': min_temp, 'humid': humid}
            self.show_task2_results(task2_data)

    def show_task3_one_day_graph(self, day_data_row):
        print(day_data_row[0].split("-")[2], end="")
        print(' ', end="")
        text = ""

        for iteration in range(0, int(day_data_row[3])):
            text += colored('+', "blue")
            print(text, end='')

        text = ""

        for iteration in range(0, int(day_data_row[1])):
            text += colored('+', "red")
            print(text, end='')

        print("%dC - %dC" % (day_data_row[3], day_data_row[1]))

    def show_task3_graphs(self):
        for month_data in self.data:
            for index, row in month_data.iterrows():

                if not math.isnan(row[3]) and not math.isnan(row[1]):
                    self.show_task3_one_day_graph(row)


def year_range(string):

    if string.find('/') == -1:

        year_passed = int(string)

        if(year_passed > 2011 or year_passed < 1996):
            msg = '%r year passed is out of range' % string
            raise argparse.ArgumentTypeError(msg)

        return year_passed

    else:

        msg = '%r only year is required the input is incorrect' % string
        raise argparse.ArgumentTypeError(msg)


def year_month_validity(string):

    if string.count('/') != 1:
        msg = '%r incorrect month and year passed' % string
        raise argparse.ArgumentTypeError(msg)

    date = datetime.datetime.strptime(
        string, "%Y/%m")

    if date.year > 2011 or date.year < 1996:
        msg = "%r year passed is out of range" % string
        raise argparse.ArgumentTypeError(msg)

    if date.month > 12 or date.month < 1:
        msg = "%r month, passed is out of range" % string
        raise argparse.ArgumentTypeError(msg)

    return string


def get_month_file_path(date, directory, file_names_in_path):
    file_names_of_year = file_names_in_path[file_names_in_path[0].str.contains(
        "lahore_weather_" + str(date.year))]

    month_abbr = calendar.month_abbr[int(date.month)]

    month_file_path = directory + "/" + file_names_of_year[
        file_names_of_year[0].str.contains("lahore_weather_" + str(date.year) +
                                           "_" + month_abbr)].iloc[0, 0]
    return month_file_path


def get_required_files_data(year, directory):

    file_names_in_directory = pandas.DataFrame(os.listdir(directory))
    if len(str(year)) == 4:

        files_names_of_year = file_names_in_directory[
            file_names_in_directory[0].str.contains("lahore_weather_" + str(year))]

        list_of_data_of_year = []

        for index, row in files_names_of_year.iterrows():
            data_of_month = pandas.read_csv(directory + "/" + row[0], header=0)
            list_of_data_of_year.append(data_of_month)

        return list_of_data_of_year
    else:
        date = datetime.datetime.strptime(year, "%Y/%m")
        file_path_of_month = get_month_file_path(
            date, directory, file_names_in_directory)
        data_of_month = pandas.read_csv(file_path_of_month, header=0)
        list_single_month = [data_of_month]
        return list_single_month


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

    if not os.path.isdir(args.path):
        print("path to directory does not exist")
        quit()

    if args.e:

        total_data = get_required_files_data(args.e, args.path)
        weather_data = WeatherData(total_data)

        weather_data.show_task1_requirements()

    if args.a:
        total_data = get_required_files_data(args.a, args.path)
        weather_data = WeatherData(total_data)
        weather_data.show_task2_requirements()

    if args.c:
        total_data = get_required_files_data(args.c, args.path)
        weather_data = WeatherData(total_data)
        weather_data.show_task3_graphs()


if __name__ == "__main__":
    main()
