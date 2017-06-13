#!/usr/bin/env python3
import os
import argparse
import calendar
import datetime
import math
import glob
import pandas

from functools import reduce
from termcolor import colored


__author__ = 'ruhaib'


class WeatherData:
    'Class to extract weather data from the desired path'

    def __init__(self, weather_data):
        self.weather_data = weather_data

    def show_task1_results(self, task1_data_to_display):
        print("Highest: %dC on %s %d" %
              (task1_data_to_display['max'][0], task1_data_to_display['max'][1], task1_data_to_display['max'][2]))
        print("Lowest: %dC on %s %d" %
              (task1_data_to_display['min'][0], task1_data_to_display['min'][1], task1_data_to_display['min'][2]))
        print("Humid: %d%% on %s %d" %
              (task1_data_to_display['humid'][0], task1_data_to_display['humid'][1], task1_data_to_display['humid'][2]))

    def task1_max_temperature_data_extraction(self):
        max_temperature_month = reduce(lambda x, y: x if(
            x['Max TemperatureC'].max() > y['Max TemperatureC'].max()) else y, self.weather_data)

        max_temp = max_temperature_month['Max TemperatureC'].max()
        max_temperature_month = max_temperature_month.loc[max_temperature_month[
            'Max TemperatureC'] == max_temp]

        if 'PKT' in max_temperature_month.columns:
            date = datetime.datetime.strptime(
                max_temperature_month['PKT'].iloc[0], "%Y-%m-%d")
        else:
            date = datetime.datetime.strptime(
                max_temperature_month['PKST'].iloc[0], "%Y-%m-%d")
        max_date = date.day
        max_month = calendar.month_name[date.month]
        return [max_temp, max_month, max_date]

    def task1_min_temperature_data_extraction(self):
        min_temperature_month = reduce(lambda x, y: x if(
            x['Min TemperatureC'].min() < y['Min TemperatureC'].min()) else y, self.weather_data)

        min_temp = min_temperature_month['Min TemperatureC'].min()

        min_temperature_month = min_temperature_month.loc[
            min_temperature_month['Min TemperatureC'] == min_temp]

        if 'PKT' in min_temperature_month.columns:
            date = datetime.datetime.strptime(
                min_temperature_month.PKT.iloc[0], "%Y-%m-%d")
        else:
            date = datetime.datetime.strptime(
                min_temperature_month.PKST.iloc[0], "%Y-%m-%d")

        min_date = date.day
        min_month = calendar.month_name[date.month]
        return [min_temp, min_month, min_date]

    def task1_humidity_data_extraction(self):
        max_humidity_month = reduce(lambda x, y: x if(
            x['Max Humidity'].max() > y['Max Humidity'].max()) else y, self.weather_data)

        humid = max_humidity_month['Max Humidity'].max()
        max_humidity_month = max_humidity_month.loc[
            max_humidity_month['Max Humidity'] == humid]

        if 'PKT' in max_humidity_month.columns:
            date = datetime.datetime.strptime(
                max_humidity_month.PKT.iloc[0], "%Y-%m-%d")
        else:
            date = datetime.datetime.strptime(
                max_humidity_month.PKST.iloc[0], "%Y-%m-%d")

        humid_date = date.day
        humid_month = calendar.month_name[date.month]
        return [humid, humid_month, humid_date]

    def show_task1_requirements(self):

        max_temperature_data = self.task1_max_temperature_data_extraction()
        min_temperature_data = self.task1_min_temperature_data_extraction()
        humid_data = self.task1_humidity_data_extraction()

        processed_year_data = {'max': max_temperature_data, 'min': min_temperature_data,
                               'humid': humid_data}

        self.show_task1_results(processed_year_data)

    def show_task2_results(self, task2_data):
        print("Highest Average: %dC" % task2_data['max_temp'])
        print("Lowest Average: %dC" % task2_data['min_temp'])
        print("Average Humidity: %d%%" % task2_data['humid'])

    def show_task2_requirements(self):
        for month_data in self.weather_data:

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

        text += colored('+', "blue")
        print(text * int(day_data_row[3]), end='')

        text = ""

        text += colored('+', "red")
        print(text * int(day_data_row[1]), end='')

        print("%dC - %dC" % (day_data_row[3], day_data_row[1]))

    def show_task3_graphs(self):
        for month_data in self.weather_data:
            for index, row in month_data.iterrows():

                if not math.isnan(row[3]) and not math.isnan(row[1]):
                    self.show_task3_one_day_graph(row)


def year_range(string):
    try:
        year_passed = datetime.datetime.strptime(string, "%Y")

        if year_passed.year > 2011 or year_passed.year < 1996:
            msg = '%r year passed is out of range' % string
            raise argparse.ArgumentTypeError(msg)

        return year_passed.year
    except ValueError:

        msg = '%r The input is incorrect' % string
        raise argparse.ArgumentTypeError(msg)


def year_month_validity(string):

    try:

        date = datetime.datetime.strptime(
            string, "%Y/%m")
        if not datetime.datetime(1996, 12, 1) <= date <= datetime.datetime(2011, 12, 9):
            msg = "%r year or month passed is out of range" % string
            raise argparse.ArgumentTypeError(msg)
    except ValueError:
        msg = '%r incorrect month and year passed' % string
        raise argparse.ArgumentTypeError(msg)

    return string


def get_required_files_data_for_task_1(year, directory):

    data_of_given_year = []

    for filename in glob.glob(directory + '/lahore_weather_' + str(year) + '*.txt'):
        data_of_month = pandas.read_csv(filename, header=0)
        data_of_given_year.append(data_of_month)

    return data_of_given_year


def get_required_files_data_for_given_month(year_and_month, directory):
    date = datetime.datetime.strptime(year_and_month, "%Y/%m")

    month_abbreviated_name = calendar.month_abbr[int(date.month)]

    filename = '{}/lahore_weather_{}_{}.txt'.format(
        directory, date.year, month_abbreviated_name)

    data_of_month = pandas.read_csv(filename, header=0)

    single_month_data = [data_of_month]
    return single_month_data


def main():

    parser = argparse.ArgumentParser(description='WeatherMan data extraction.')

    parser.add_argument(
        '-e', dest='weatherman_task_1', type=year_range,
        help='(usage: -e yyyy) to see maximum temperature,'
             ' minimum temperature and humidity')

    parser.add_argument(
        '-a', dest='weatherman_task_2', type=year_month_validity,
        help='(usage: -a yyyy/mm) to see average maximum, average minimum'
             ' temperature and mean humidity of the month')

    parser.add_argument(
        '-c', dest='weatherman_task_bonus', type=year_month_validity,
        help='(usage: -c yyyy/mm) to see horizontal bar chart'
             ' of highest and lowest temperature on each day')

    parser.add_argument('path_to_files',
                        help='path to the files having weather data')

    args = parser.parse_args()

    if not os.path.isdir(args.path_to_files):
        print("path to directory does not exist")
        quit()

    if args.weatherman_task_1:

        total_data = get_required_files_data_for_task_1(
            args.weatherman_task_1, args.path_to_files)
        weather_data = WeatherData(total_data)

        weather_data.show_task1_requirements()

    if args.weatherman_task_2:
        total_data = get_required_files_data_for_given_month(
            args.weatherman_task_2, args.path_to_files)
        weather_data = WeatherData(total_data)
        weather_data.show_task2_requirements()

    if args.weatherman_task_bonus:
        total_data = get_required_files_data_for_given_month(
            args.weatherman_task_bonus, args.path_to_files)
        weather_data = WeatherData(total_data)
        weather_data.show_task3_graphs()


if __name__ == "__main__":
    main()
