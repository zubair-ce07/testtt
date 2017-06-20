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

    def column_analysis(self, column_key, is_max_required=True):

        if is_max_required:
            day_data = max(
                self.weather_data,
                key=lambda x:
                float('-inf') if math.isnan(x[column_key]) else
                x[column_key]
            )
        else:
            day_data = min(
                self.weather_data,
                key=lambda x: float('inf') if math.isnan(x[column_key])
                else x[column_key])

        value = day_data[column_key]

        date = datetime.datetime.strptime(
            day_data['PKT'] or
            day_data['PKST'],
            '%Y-%m-%d')
        day = date.day
        month = calendar.month_name[date.month]
        return {
            'value': value,
            'month': month,
            'day': day
        }

    def analyze_data(self,
                     max_temperature_key,
                     min_temperature_key,
                     humid_key,
                     is_average_data=False):

        max_temperature = self.column_analysis(
            max_temperature_key)

        min_temperature = self.column_analysis(
            min_temperature_key, False)

        if is_average_data:
            humidity_data_of_month = pandas.DataFrame(self.weather_data)
            humidity = {
                'value': humidity_data_of_month[humid_key].mean()
            }
        else:
            humidity = self.column_analysis(humid_key)

        processed_data = {'max': max_temperature,
                          'min': min_temperature,
                          'humid': humidity}

        if is_average_data:
            self.display_analyzed_month_data(processed_data)
        else:
            self.display_analyzed_year_data(processed_data)

    def display_analyzed_year_data(self, analyzed_data_of_year):

        print('Highest: {0[value]}C on {0[month]}s {0[day]}d'.format(
                  analyzed_data_of_year['max']))
        print('Highest: {0[value]}C on {0[month]}s {0[day]}d'.format(
                  analyzed_data_of_year['min']))
        print('Highest: {0[value]}C on {0[month]}s {0[day]}d'.format(
                  analyzed_data_of_year['humid']))

    def display_analyzed_month_data(self, analyzed_data_of_month):
        print('Highest Average: {0[value]}C'.format(
            analyzed_data_of_month['max']))
        print('Lowest Average: {0[value]}C'.format(
            analyzed_data_of_month['min']))
        print('Average Humidity: {0[value]}%%'.format(
              analyzed_data_of_month['humid']))

    def display_stacked_horizontal_chart(self, one_day_data):
        date = (one_day_data['PKT'] or one_day_data['PKST'])
        date = datetime.datetime.strptime(date, "%Y-%m-%d")

        text = str(date.day) + ' '
        text += colored('+' * int(one_day_data['Min TemperatureC']), 'blue')
        text += colored('+' * int(one_day_data['Max TemperatureC']), 'red')

        text += ' {}C - {}C'.format(
            one_day_data['Min TemperatureC'],
            one_day_data['Max TemperatureC'])

        print(text)

    def display_simple_horizontal_chart(self, one_day_data):

        date = (one_day_data['PKT'] or one_day_data['PKST'])
        date = datetime.datetime.strptime(date, "%Y-%m-%d")

        start_of_line = str(date.day) + ' '
        end_of_line = ' {}C'.format(one_day_data['Min TemperatureC'])

        coldness = colored('+' * int(one_day_data['Min TemperatureC']), 'blue')
        hotness = colored('+' * int(one_day_data['Max TemperatureC']), 'red')

        print(start_of_line + coldness + end_of_line)
        print(start_of_line + hotness + end_of_line)

    def display_temperature_chart_of_given_month(self, is_stacked_chart=False):
        for day_data in self.weather_data:
            if not math.isnan(day_data['Max TemperatureC']) and not math.isnan(
                    day_data['Min TemperatureC']):
                if is_stacked_chart:
                    self.display_stacked_horizontal_chart(day_data)
                else:
                    self.display_simple_horizontal_chart(day_data)


class Validation:

    def verify_date(self, date):

        if date.count('/') == 1:
            pattern_to_match = "%Y/%m"
        else:
            pattern_to_match = "%Y"

        try:
            datetime.datetime.strptime(date, pattern_to_match)
        except ValueError:
            msg = '%r The input is incorrect' % date
            raise argparse.ArgumentTypeError(msg)
        return date


class ExtractData:

    def __init__(self, date, directory):
        self.directory = directory
        self.date_string = str(date)
        if str(date).count('/') == 1:
            self.date = datetime.datetime.strptime(date, "%Y/%m")
        else:
            self.date = datetime.datetime.strptime(str(date), "%Y")

    def file_name(self):

        if self.date_string.count('/') == 1:
            month_abbreviated_name = calendar.month_abbr[int(self.date.month)]
            return '{}/lahore_weather_{}_{}.txt'.format(
                self.directory, self.date.year, month_abbreviated_name)
        else:
            return self.directory + '/lahore_weather_' + str(self.date.year) +\
             '*.txt'

    def read_data(self):

        if self.date_string.count('/') == 1:
            return self.data_for_given_month()
        else:
            return self.data_for_given_year()

    def data_for_given_year(self):

        year_data = []
        for filename in glob.glob(self.file_name()):
            month_data = self.data_for_given_month(filename)
            year_data.extend(month_data)
        return year_data

    def data_for_given_month(self, filename=''):

        if filename == '':
            filename = self.file_name()

        return pandas.read_csv(
            filename, header=0).to_dict(orient='records')


def main():

    date_type = Validation()
    parser = argparse.ArgumentParser(description='WeatherMan data analysis.')

    parser.add_argument(
        '-e', '--year',
        dest='given_year',
        type=date_type.verify_date,
        metavar='',
        help='(usage: -e yyyy) to see maximum temperature,'
        ' minimum temperature and humidity')

    parser.add_argument(
        '-a', '--month',
        dest='given_month_for_analysis',
        type=date_type.verify_date,
        metavar='',
        help='(usage: -a yyyy/mm) to see average maximum, average minimum'
        ' temperature and mean humidity of the month')

    parser.add_argument(
        '-c', '--bars',
        type=date_type.verify_date,
        dest='simple_chart',
        metavar='',
        help='(usage: -c yyyy/mm) to see horizontal bar chart'
        ' of highest and lowest temperature on each day')

    parser.add_argument(
        '-s', '--charts',
        type=date_type.verify_date,
        dest='stacked_chart',
        metavar='',
        help='(usage: -c yyyy/mm) to see horizontal bar chart'
        ' of highest and lowest temperature on each day')

    parser.add_argument('path_to_files',
                        help='path to the files having weather data')

    args = parser.parse_args()

    if not os.path.isdir(args.path_to_files):
        print('path to directory does not exist')
        exit(1)

    date = args.given_year or args.given_month_for_analysis or \
        args.simple_chart or args.stacked_chart

    data_reader = ExtractData(date, args.path_to_files)
    total_data = data_reader.read_data()

    if args.given_year:
        weather_data = WeatherData(total_data)
        weather_data.analyze_data(
            'Max TemperatureC',
            'Min TemperatureC',
            'Max Humidity'
        )

    else:
        weather_data = WeatherData(total_data)

        if args.given_month_for_analysis:
            weather_data.analyze_data(
                'Mean TemperatureC',
                'Mean TemperatureC',
                ' Mean Humidity',
                True
            )

        if args.simple_chart:
            weather_data.display_temperature_chart_of_given_month()

        if args.stacked_chart:
            weather_data.display_temperature_chart_of_given_month(True)


if __name__ == '__main__':
    main()
