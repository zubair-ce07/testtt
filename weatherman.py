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
                  analyzed_data_of_year['max']['day']))

        print('Lowest: %dC on %s %d' %
              (
                  analyzed_data_of_year['min']['temperature'],
                  analyzed_data_of_year['min']['month'],
                  analyzed_data_of_year['min']['day']))

        print('Humid: %d%% on %s %d' %
              (
                  analyzed_data_of_year['humid']['humidity'],
                  analyzed_data_of_year['humid']['month'],
                  analyzed_data_of_year['humid']['day']))

    def max_temperature_data_of_year(self):

        max_temperature_month = max(self.weather_data, key=lambda x:
                                    x['Max TemperatureC'].max())

        max_temperature_day_data = max_temperature_month.ix[
            max_temperature_month['Max TemperatureC'].idxmax()]

        max_temp = max_temperature_day_data['Max TemperatureC']

        date = datetime.datetime.strptime(
            max_temperature_day_data['PKT'] or max_temperature_day_data['PKST'], '%Y-%m-%d')
        max_day = date.day
        max_month = calendar.month_name[date.month]
        return {
            'temperature': max_temp,
            'month': max_month,
            'day': max_day
        }

    def min_temperature_data_of_year(self):
        min_temperature_month = min(
            self.weather_data, key=lambda x: x['Min TemperatureC'].min())
        min_temp = min_temperature_month['Min TemperatureC'].min()

        min_temperature_day_data = min_temperature_month.ix[
            min_temperature_month['Min TemperatureC'].idxmin()]

        date = datetime.datetime.strptime(
            min_temperature_day_data['PKT'] or min_temperature_day_data['PKST'], '%Y-%m-%d')

        min_day = date.day
        min_month = calendar.month_name[date.month]
        return {
            'temperature': min_temp,
            'month': min_month,
            'day': min_day
        }

    def max_humidity_data_of_year(self):
        max_humidity_month = max(
            self.weather_data, key=lambda x: x['Max Humidity'].max())

        humid = max_humidity_month['Max Humidity'].max()
        max_humidity_day_data = max_humidity_month.ix[
            max_humidity_month['Max Humidity'].idxmax()]

        date = datetime.datetime.strptime(
            max_humidity_day_data['PKT'] or max_humidity_day_data['PKST'], '%Y-%m-%d')

        humid_day = date.day
        humid_month = calendar.month_name[date.month]
        return {
            'humidity': humid,
            'month': humid_month,
            'day': humid_day
        }

    def analyze_year_data(self):

        max_temperature_data = self.max_temperature_data_of_year()
        min_temperature_data = self.min_temperature_data_of_year()
        humid_data = self.max_humidity_data_of_year()

        processed_year_data = {'max': max_temperature_data,
                               'min': min_temperature_data,
                               'humid': humid_data}

        self.display_analyzed_year_data(processed_year_data)

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
            avg_humid = month_data[' Mean Humidity'].sum(
            ) / month_data[' Mean Humidity'].count()

            month_analysis_data = {'avg_max_temp': avg_max_temp,
                                   'avg_min_temp': avg_min_temp,
                                   'avg_humid': avg_humid}
            self.show_month_analysis_data(month_analysis_data)

    def display_one_day_horizontal_bar_graph(self, one_day_data, is_bars=False):

        date = (one_day_data['PKT'] or one_day_data['PKST'])
        date = datetime.datetime.strptime(date, "%Y-%m-%d")

        text = str(date.day)
        text += ' '

        text += colored('+' * int(one_day_data['Min TemperatureC']), 'blue')

        if is_bars:
            text += ' {}C'.format(one_day_data['Min TemperatureC'])
            print(text)
            text = str(date.day)

        text += colored('+' * int(one_day_data['Max TemperatureC']), 'red')
        if is_bars:
            text += ' {}C'.format(one_day_data['Max TemperatureC'])
            print(text)
        else:
            text += ' {}C - {}C'.format(
                one_day_data['Min TemperatureC'],
                one_day_data['Max TemperatureC'])
            print(text)

    def display_temperature_chart_of_given_month(self, is_bars=False):
        for month_data in self.weather_data:
            for index, row in month_data.iterrows():
                if not math.isnan(row['Max TemperatureC']) and not math.isnan(
                        row['Min TemperatureC']):

                    self.display_one_day_horizontal_bar_graph(row, is_bars)


class Validation:

    def verify_date(self, date):

        if date.count('/') == 1:
            pattern_to_match = "%Y/%m"
        else:
            pattern_to_match = "%Y"
        try:
            year_passed = datetime.datetime.strptime(date, pattern_to_match)
            return year_passed.year
        except ValueError:
            msg = '%r The input is incorrect' % date
            raise argparse.ArgumentTypeError(msg)
        return date


class Filer:
    def dataframe_from_file(self, filename):
        return pandas.read_csv(filename, header=0)

    def make_month_file_name(self, directory, date):
        month_abbreviated_name = calendar.month_abbr[int(date.month)]
        return '{}/lahore_weather_{}_{}.txt'.format(
            directory, date.year, month_abbreviated_name)


class ExtractData:

    def __init__(self, date):
        if str(date).count('/') == 1:
            self.date = datetime.datetime.strptime(date, "%Y/%m")
        else:
            self.date = datetime.datetime.strptime(str(date), "%Y")
        self.file_reader = Filer()

    def data_for_given_year(self, directory):

        year_data = []
        for filename in glob.glob(directory + '/lahore_weather_' + str(self.date.year) + '*.txt'):
            month_data = self.file_reader.dataframe_from_file(filename)
            year_data.append(month_data)
        return year_data

    def data_for_given_month(self, directory):

        filename = self.file_reader.make_month_file_name(directory, self.date)

        data_of_month = self.file_reader.dataframe_from_file(filename)

        return [data_of_month]


def main():

    date_type = Validation()
    parser = argparse.ArgumentParser(description='WeatherMan data analysis.')

    parser.add_argument(
        '-e', '--year', dest='given_year', type=date_type.verify_date,
        metavar='', help='(usage: -e yyyy) to see maximum temperature,'
        ' minimum temperature and humidity')

    parser.add_argument(
        '-a', '--month', dest='given_month_for_analysis', type=date_type.verify_date,
        metavar='', help='(usage: -a yyyy/mm) to see average maximum, average minimum'
        ' temperature and mean humidity of the month')

    parser.add_argument(
        '-c', '--bars', type=date_type.verify_date, dest='given_month_for_bars',
        metavar='', help='(usage: -c yyyy/mm) to see horizontal bar chart'
        ' of highest and lowest temperature on each day')

    parser.add_argument(
        '-s', '--charts', type=date_type.verify_date, dest='given_month_for_charts',
        metavar='', help='(usage: -c yyyy/mm) to see horizontal bar chart'
        ' of highest and lowest temperature on each day')

    parser.add_argument('path_to_files',
                        help='path to the files having weather data')

    args = parser.parse_args()

    if not os.path.isdir(args.path_to_files):
        print('path to directory does not exist')
        exit(1)
    date = args.given_year or args.given_month_for_analysis or args.given_month_for_charts or args.given_month_for_bars
    data_reader = ExtractData(date)

    if args.given_year:
        total_data = data_reader.data_for_given_year(
            args.path_to_files)

        weather_data = WeatherData(total_data)
        weather_data.analyze_year_data()

    else:
        total_data = data_reader.data_for_given_month(
            args.path_to_files)
        weather_data = WeatherData(total_data)

        if args.given_month_for_analysis:
            weather_data.analyze_month_data()

        if args.given_month_for_charts:
            weather_data.display_temperature_chart_of_given_month()

        if args.given_month_for_bars:
            weather_data.display_temperature_chart_of_given_month(True)


if __name__ == '__main__':
    main()
