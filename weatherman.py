import argparse
import calendar
from dateutil import parser
from termcolor import colored
import csv
import re
import os


class WeatherMan:

    def __init__(self):
        self.months = calendar.month_name

        self.field_date = 'PKT'
        self.field_temp_max = 'Max TemperatureC'
        self.field_temp_min = 'Min TemperatureC'
        self.field_humid_max = 'Max Humidity'
        self.field_temp_mean = 'Mean TemperatureC'
        self.field_humid_mean = 'Mean Humidity'

    @staticmethod
    def read_file(file_path, year, month, data_fields):
        filename_pattern = '(?=.*{year})(?=.*{month}).*\.txt$'.format(year=year, month=month[:3])

        for filename in os.listdir(file_path):
            if re.search(filename_pattern, filename, flags=re.IGNORECASE):
                with open('{path}/{filename}'.format(filename=filename, path=file_path), ) as csvFile:
                    dict_reader = csv.DictReader(csvFile, fieldnames=data_fields)
                    next(dict_reader)  # Skip header
                    return list(dict_reader)

    @staticmethod
    def compare(value1, value2, compare_func):
        return value1 and (not value2 or compare_func(int(value1), int(value2)))

    def display_highest_lowest_temperature(self, file_path, year):
        if not file_path or not year:
            print('Please pass correct arguments.')
            return

        highest_data = {'highest_temp': None, 'highest_day': None, 'highest_month': None}
        lowest_data = {'lowest_temp': None, 'lowest_day': None, 'lowest_month': None}
        humidity_data = {'highest_humid': None, 'humid_day': None, 'humid_month': None}

        for month in self.months[1:]:
            weather_records = self.read_file(file_path, year, month,
                                             [self.field_date, self.field_temp_max,
                                              self.field_temp_min, self.field_humid_max])
            if not weather_records:
                print('{month},{year} file not found.'.format(year=year, month=month))
                continue

            for weather_record in weather_records:
                if self.compare(weather_record[self.field_temp_max], highest_data['highest_temp'],
                                lambda op1, op2: (op2 < op1)):
                    cur_date = parser.parse(weather_record[self.field_date])
                    highest_data['highest_temp'] = int(weather_record[self.field_temp_max])
                    highest_data['highest_day'] = cur_date.day
                    highest_data['highest_month'] = month

                if self.compare(weather_record[self.field_temp_min], lowest_data['lowest_temp'],
                                lambda op1, op2: (op2 > op1)):
                    cur_date = parser.parse(weather_record[self.field_date])
                    lowest_data['lowest_temp'] = int(weather_record[self.field_temp_min])
                    lowest_data['lowest_day'] = cur_date.day
                    lowest_data['lowest_month'] = month

                if self.compare(weather_record[self.field_humid_max], humidity_data['highest_humid'],
                                lambda op1, op2: (op2 < op1)):
                    cur_date = parser.parse(weather_record[self.field_date])
                    humidity_data['highest_humid'] = int(weather_record[self.field_humid_max])
                    humidity_data['humid_day'] = cur_date.day
                    humidity_data['humid_month'] = month

        print('Highest: {}C on {} {} \nLowest: {}C on {} {} \nHumid: {}C on {} {}'.format(
            highest_data['highest_temp'], highest_data['highest_month'], highest_data['highest_day'],
            lowest_data['lowest_temp'], lowest_data['lowest_month'], lowest_data['lowest_day'],
            humidity_data['highest_humid'], humidity_data['humid_month'], humidity_data['humid_day']))

    def display_average(self, file_path, year, month):
        if not file_path or not year or not month:
            print('Please pass correct arguments.')
            return

        highest_temp = None
        lowest_temp = None
        highest_humid = None

        weather_records = self.read_file(file_path, year, self.months[month],
                                         [self.field_date, self.field_temp_mean, self.field_humid_mean])
        if not weather_records:
            print('{month},{year} file not found.'.format(year=year, month=month))
            return

        for weather_record in weather_records:
            if self.compare(weather_record[self.field_temp_mean], highest_temp, lambda op1, op2: (op2 < op1)):
                highest_temp = int(weather_record[self.field_temp_mean])

            if self.compare(weather_record[self.field_temp_mean], lowest_temp, lambda op1, op2: (op2 > op1)):
                lowest_temp = int(weather_record[self.field_temp_mean])

            if self.compare(weather_record[self.field_humid_mean], highest_humid, lambda op1, op2: (op2 < op1)):
                highest_humid = int(weather_record[self.field_humid_mean])

        print('Highest Average: {}C \nLowest Average: {}C \nAverage Humidity: {}%'.format(
            highest_temp, lowest_temp, highest_humid))

    def print_two_bar_charts_record(self, day, temp, symbol, color):
        print('{} '.format(day), end='')
        self.colored_print(temp, symbol, color)
        print(' {}C'.format(temp))

    @staticmethod
    def colored_print(count, symbol, color):
        for index in range(int(count)):
            print(colored(symbol, color), end='')

    def display_two_bar_charts(self, file_path, year, month):
        if not file_path or not year or not month:
            print('Please pass correct arguments.')
            return

        print('{} {}'.format(self.months[month], year))

        weather_records = self.read_file(file_path, year, self.months[month],
                                         [self.field_date, self.field_temp_max, self.field_temp_min])
        if not weather_records:
            print('{month},{year} file not found.'.format(year=year, month=month))
            return

        for weather_record in weather_records:
            try:
                day = parser.parse(weather_record[self.field_date]).day
            except ValueError:
                continue

            if weather_record[self.field_temp_max]:
                self.print_two_bar_charts_record(day, weather_record[self.field_temp_max], '+', 'red')

            if weather_record[self.field_temp_min]:
                self.print_two_bar_charts_record(day, weather_record[self.field_temp_min], '+', 'blue')

    def display_one_bar_chart(self, file_path, year, month):
        if not file_path or not year or not month:
            print('Please pass correct arguments.')
            return

        print('{} {}'.format(self.months[month], year))

        weather_records = self.read_file(file_path, year, self.months[month],
                                         [self.field_date, self.field_temp_max, self.field_temp_min])
        if not weather_records:
            print('{month},{year} file not found.'.format(year=year, month=month))
            return

        for weather_record in weather_records:
            highest_temp = weather_record[self.field_temp_max]
            lowest_temp = weather_record[self.field_temp_min]

            if lowest_temp or highest_temp:
                print('{} '.format(parser.parse(weather_record[self.field_date]).day), end='')

                if weather_record[self.field_temp_min]:
                    self.colored_print(lowest_temp, '+', 'blue')

                if weather_record[self.field_temp_max]:
                    self.colored_print(highest_temp, '+', 'red')

                print(' {}C-{}C'.format(lowest_temp, highest_temp))


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-e', nargs=2, dest='highest_lowest_temp')
    arg_parser.add_argument('-a', nargs=2, dest='average')
    arg_parser.add_argument('-c', nargs=2, dest='bar_chart')
    args = arg_parser.parse_args()

    weatherman = WeatherMan()

    if args.highest_lowest_temp:
        try:
            date = parser.parse(args.highest_lowest_temp[0])
            weatherman.display_highest_lowest_temperature(args.highest_lowest_temp[1], date.year)
        except ValueError:
            print('Please pass date in correct format.')
    if args.average:
        try:
            date = parser.parse(args.average[0])
            weatherman.display_average(args.average[1], date.year, date.month)
        except ValueError:
            print('Please pass date in correct format.')
    if args.bar_chart:
        try:
            date = parser.parse(args.bar_chart[0])
            weatherman.display_two_bar_charts(args.bar_chart[1], date.year, date.month)
            weatherman.display_one_bar_chart(args.bar_chart[1], date.year, date.month)
        except ValueError:
            print('Please pass date in correct format.')


if __name__ == "__main__":
    main()

