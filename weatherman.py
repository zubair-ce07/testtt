#!/usr/bin/env python3
import os
import argparse
import calendar
import datetime
import math
import glob
import pandas

from termcolor import colored


__author__ = 'ruhaib'


class WeatherData:
    'Class to extract weather data from the desired path'

    def __init__(self, weather_data):
        self.weather_data = weather_data

    def display_analyzed_year_data(self, analyzed_data_of_year):
        print('Highest: %dC on %s %d' %
              (
                  analyzed_data_of_year['max']['temperature'],
                  analyzed_data_of_year['max']['month'],
                  analyzed_data_of_year['max']['date']))

        print('Lowest: %dC on %s %d' %
              (
                  analyzed_data_of_year['min']['temperature'],
                  analyzed_data_of_year['min']['month'],
                  analyzed_data_of_year['min']['date']))

        print('Humid: %d%% on %s %d' %
              (
                  analyzed_data_of_year['humid']['temperature'],
                  analyzed_data_of_year['humid']['month'],
                  analyzed_data_of_year['humid']['date']))

    def max_temperature_data_of_year(self):
        # max_temperature_month = reduce(lambda x, y: x if(
        #     x['Max TemperatureC'].max() > y['Max TemperatureC'].max()) else y, self.weather_data)
        max_temperature_month = max(
            self.weather_data, key=lambda x: x['Max TemperatureC'].max())

        max_temp = max_temperature_month['Max TemperatureC'].max()
        max_temperature_month = max_temperature_month.loc[max_temperature_month[
            'Max TemperatureC'] == max_temp]

        date = datetime.datetime.strptime(
            max_temperature_month['PKT'].iloc[0] or max_temperature_month['PKST'].iloc[0], '%Y-%m-%d')

        max_date = date.day
        max_month = calendar.month_name[date.month]
        return {
            'temperature': max_temp,
            'month': max_month,
            'date': max_date
        }

    def min_temperature_data_of_year(self):
        # min_temperature_month = reduce(lambda x, y: x if(
        #     x['Min TemperatureC'].min() < y['Min TemperatureC'].min()) else y, self.weather_data)
        min_temperature_month = min(
            self.weather_data, key=lambda x: x['Min TemperatureC'].min())
        min_temp = min_temperature_month['Min TemperatureC'].min()

        min_temperature_month = min_temperature_month.loc[
            min_temperature_month['Min TemperatureC'] == min_temp]

        date = datetime.datetime.strptime(
            min_temperature_month['PKT'].iloc[0] or min_temperature_month['PKST'].iloc[0], '%Y-%m-%d')

        min_date = date.day
        min_month = calendar.month_name[date.month]
        return {
            'temperature': min_temp,
            'month': min_month,
            'date': min_date
        }

    def max_humidity_data_of_year(self):
        # max_humidity_month = reduce(lambda x, y: x if(
        #     x['Max Humidity'].max() > y['Max Humidity'].max()) else y, self.weather_data)
        max_humidity_month = max(
            self.weather_data, key=lambda x: x['Max Humidity'].max())

        humid = max_humidity_month['Max Humidity'].max()
        max_humidity_month = max_humidity_month.loc[
            max_humidity_month['Max Humidity'] == humid]

        date = datetime.datetime.strptime(
            max_humidity_month['PKT'].iloc[0] or max_humidity_month['PKST'].iloc[0], '%Y-%m-%d')

        humid_date = date.day
        humid_month = calendar.month_name[date.month]
        return {
            'humidity': humid,
            'month': humid_month,
            'date': humid_date
        }

    def analyze_year_data(self):

        max_temperature_data = self.max_temperature_data_of_year()
        min_temperature_data = self.min_temperature_data_of_year()
        humid_data = self.max_humidity_data_of_year()

        processed_year_data = {'max': max_temperature_data, 'min': min_temperature_data,
                               'humid': humid_data}

        self.show_task1_results(processed_year_data)

    def show_month_analysis_data(self, analyzed_data_of_month):
        print('Highest Average: %dC' % analyzed_data_of_month['avg_max_temp'])
        print('Lowest Average: %dC' % analyzed_data_of_month['avg_min_temp'])
        print('Average Humidity: %d%%' % analyzed_data_of_month['avg_humid'])

    def analyze_month_data(self):
        for month_data in self.weather_data:

            # extracting average highest temperature
            avg_max_temp = month_data['Mean TemperatureC'].max()

            # extracting average lowest temperature
            avg_min_temp = month_data['Mean TemperatureC'].min()

            # extracting average humidity
            avg_humid = month_data['Mean Humidity'].sum(
            ) / month_data['Mean Humidity'].count()

            month_analysis_data = {'avg_max_temp': avg_max_temp,
                                   'avg_min_temp': avg_min_temp,
                                   'avg_humid': avg_humid}
            self.show_month_analysis_data(month_analysis_data)

    def display_one_day_horizontal_bar_graph(self, one_day_data):

        date = (one_day_data['PKT'] or one_day_data['PKST'])
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        print(str(date.day), end='')
        print(' ', end='')
        text = ''

        text += colored('+', 'blue')
        print(text * int(one_day_data['Min TemperatureC']), end='')

        text = ''

        text += colored('+', 'red')
        print(text * int(one_day_data['Max TemperatureC']), end='')

        print(' %dC - %dC' %
              (one_day_data['Min TemperatureC'], one_day_data['Max TemperatureC']))

    def display_temperature_chart_of_given_month_of_year(self):
        for month_data in self.weather_data:
            for index, row in month_data.iterrows():
                if not math.isnan(row['Max TemperatureC']) and not math.isnan(row['Min TemperatureC']):
                    self.display_one_day_horizontal_bar_graph(row)


def year_range(string):
    try:
        year_passed = datetime.datetime.strptime(string, '%Y')

        if not datetime.datetime(1996, 12, 1) <= year_passed <= datetime.datetime(2011, 12, 9):
            msg = '%r year passed is out of range' % string
            raise argparse.ArgumentTypeError(msg)

        return year_passed.year
    except ValueError:

        msg = '%r The input is incorrect' % string
        raise argparse.ArgumentTypeError(msg)


def year_month_validity(string):

    try:

        date = datetime.datetime.strptime(
            string, '%Y/%m')
        if not datetime.datetime(1996, 12, 1) <= date <= datetime.datetime(2011, 12, 9):
            msg = '%r year or month passed is out of range' % string
            raise argparse.ArgumentTypeError(msg)
    except ValueError:
        msg = '%r incorrect month and year passed' % string
        raise argparse.ArgumentTypeError(msg)

    return string


def get_required_files_data_for_given_year(year, directory):

    data_of_given_year = []

    for filename in glob.glob(directory + '/lahore_weather_' + str(year) + '*.txt'):
        data_of_month = pandas.read_csv(filename, header=0)
        data_of_given_year.append(data_of_month)

    return data_of_given_year


def get_required_files_data_for_given_month(year_and_month, directory):
    date = datetime.datetime.strptime(year_and_month, '%Y/%m')

    month_abbreviated_name = calendar.month_abbr[int(date.month)]

    filename = '{}/lahore_weather_{}_{}.txt'.format(
        directory, date.year, month_abbreviated_name)

    data_of_month = pandas.read_csv(filename, header=0)

    single_month_data = [data_of_month]
    return single_month_data


def main():

    parser = argparse.ArgumentParser(description='WeatherMan data analysis.')

    parser.add_argument(
        '-e', dest='weatherman_year_data_analysis', type=year_range,
        help='(usage: -e yyyy) to see maximum temperature,'
        ' minimum temperature and humidity')

    parser.add_argument(
        '-a', dest='weatherman_month_of_year_data_analysis', type=year_month_validity,
        help='(usage: -a yyyy/mm) to see average maximum, average minimum'
        ' temperature and mean humidity of the month')

    parser.add_argument(
        '-c', dest='weatherman_temperature_chart_of_given_month_of_year', type=year_month_validity,
        help='(usage: -c yyyy/mm) to see horizontal bar chart'
        ' of highest and lowest temperature on each day')

    parser.add_argument('path_to_files',
                        help='path to the files having weather data')

    args = parser.parse_args()

    if not os.path.isdir(args.path_to_files):
        print('path to directory does not exist')
        exit(1)

    if args.weatherman_year_data_analysis:

        total_data = get_required_files_data_for_given_year(
            args.weatherman_year_data_analysis, args.path_to_files)
        weather_data = WeatherData(total_data)

        weather_data.analyze_year_data()

    if args.weatherman_month_of_year_data_analysis:
        total_data = get_required_files_data_for_given_month(
            args.weatherman_month_of_year_data_analysis, args.path_to_files)
        weather_data = WeatherData(total_data)
        weather_data.analyze_month_data()

    if args.weatherman_temperature_chart_of_given_month_of_year:
        total_data = get_required_files_data_for_given_month(
            args.weatherman_temperature_chart_of_given_month_of_year, args.path_to_files)
        weather_data = WeatherData(total_data)
        weather_data.display_temperature_chart_of_given_month_of_year()


if __name__ == '__main__':
    main()
