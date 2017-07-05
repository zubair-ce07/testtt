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


class WeatherReport:

    def display_month_report(self, analyzed_data):
        print('Highest Average: {}C'.format(
            analyzed_data['average_max_temperature']))
        print('Lowest Average: {}C'.format(
            analyzed_data['average_min_temperature']))
        print('Average Humidity: {}%'.format(
              analyzed_data['average_humidity']))

    def display_year_report(self, analyzed_data):
        print('Highest: {0[value]}C on {0[month]} {0[day]}'.format(
                  analyzed_data['max']))
        print('Lowest: {0[value]}C on {0[month]} {0[day]}'.format(
                  analyzed_data['min']))
        print('Humid: {0[value]}% on {0[month]} {0[day]}'.format(
                  analyzed_data['humid']))


class Charts:
    def display_temperature_chart_of_given_month(
                                                self,
                                                month_data,
                                                is_stacked_chart=False):
        for day_data in month_data:
            if not math.isnan(day_data['Max TemperatureC']) and not math.isnan(
                    day_data['Min TemperatureC']):
                if is_stacked_chart:
                    self.display_stacked_horizontal_chart(day_data)
                else:
                    self.display_simple_horizontal_chart(day_data)

    def display_stacked_horizontal_chart(self, one_day_data):
        date = (one_day_data['PKT'] or one_day_data['PKST'])
        date = datetime.datetime.strptime(date, "%Y-%m-%d")

        text = str(date.day) + ' '
        text += colored('+' * int(one_day_data['Min TemperatureC']), 'blue')
        text += colored('+' * int(one_day_data['Max TemperatureC']), 'red')

        text += ' {}C - {}C'.format(
            str(int(one_day_data['Min TemperatureC'])),
            str(int(one_day_data['Max TemperatureC'])))

        print(text)

    def display_simple_horizontal_chart(self, one_day_data):
        date = (one_day_data['PKT'] or one_day_data['PKST'])
        date = datetime.datetime.strptime(date, "%Y-%m-%d")

        start_of_line = str(date.day) + ' '
        cold_value = int(one_day_data['Min TemperatureC'])
        hot_value = int(one_day_data['Max TemperatureC'])

        coldness = colored(
            '+' * int(one_day_data['Min TemperatureC']),
            'blue') + ' ' + str(cold_value) + 'C'

        hotness = colored('+' * int(one_day_data['Max TemperatureC']), 'red')
        hotness += ' ' + str(hot_value) + 'C'
        print(start_of_line + coldness)
        print(start_of_line + hotness)


class WeatherMan:

    def __init__(self, weather_data):
        self.weather_data = weather_data
        self.reporter = WeatherReport()
        self.chart_report = Charts()

    def _data_analysis(self, column_key, is_max_required=True):
        if is_max_required:
            method, infinity = max, float('-inf')
        else:
            method, infinity = min, float('inf')
        day_data = method(
            self.weather_data,
            key=lambda x: infinity if math.isnan(x[column_key]) else
            x[column_key]
            )
        value = int(day_data[column_key])
        date = datetime.datetime.strptime(day_data['PKT'] or day_data['PKST'],
                                          '%Y-%m-%d')
        day = date.day
        month = calendar.month_name[date.month]
        return {
            'value': value,
            'month': month,
            'day': day
        }

    def analyze_yearly_data(self):

        max_temperature = self._data_analysis('Max TemperatureC')

        min_temperature = self._data_analysis('Min TemperatureC', False)

        humidity = self._data_analysis('Max Humidity')

        processed_data = {'max': max_temperature,
                          'min': min_temperature,
                          'humid': humidity}

        self.reporter.display_year_report(processed_data)

    def analyze_monthly_average_data(self):
        humidity_data_of_month = pandas.DataFrame(self.weather_data)

        average_max_temperature = humidity_data_of_month[
                                                    'Max TemperatureC'].mean()
        average_min_temperature = humidity_data_of_month[
                                                    'Min TemperatureC'].mean()
        average_humidity = humidity_data_of_month[' Mean Humidity'].mean()

        processed_data = {'average_max_temperature': int(
                                                    average_max_temperature),
                          'average_min_temperature': int(
                                                    average_min_temperature),
                          'average_humidity': int(average_humidity)}

        self.reporter.display_month_report(processed_data)

    def monthly_chart_report(self, is_stacked=False):
        self.chart_report.display_temperature_chart_of_given_month(
                                                self.weather_data, is_stacked)


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
            date = datetime.datetime.strptime(date, "%Y/%m")
            month_abbreviated_name = calendar.month_abbr[int(date.month)]
            self.file_name_pattern = os.path.join(
                directory, 'lahore_weather_' + str(date.year) + '_' +
                           month_abbreviated_name + '.txt')
        else:
            date = datetime.datetime.strptime(str(date), "%Y")
            self.file_name_pattern = os.path.join(
                directory, 'lahore_weather_' + str(date.year) + '_*.txt')

    def read_data(self):
        data = []
        for filename in glob.glob(self.file_name_pattern):
            data.extend(
                pandas.read_csv(filename, header=0).to_dict(orient='records'))
        return data


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
        weather_data = WeatherMan(total_data)
        weather_data.analyze_yearly_data()

    else:
        weather_data = WeatherMan(total_data)

        if args.given_month_for_analysis:
            weather_data.analyze_monthly_average_data()

        if args.simple_chart:
            weather_data.monthly_chart_report()

        if args.stacked_chart:
            weather_data.monthly_chart_report(True)


if __name__ == '__main__':
    main()
