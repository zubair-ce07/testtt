"""
This Module is used to calculate weather reports from data provided
in text files
"""

import re
import os
import sys
import csv
import argparse
from pathlib import Path
from itertools import chain
from datetime import datetime


class TerminalColors:
    BLUE = '\033[94m'
    RED = '\033[91m'
    RESET = '\033[0m'


class WeatherReading:
    def __init__(self, kwargs):
        self.reading_date = kwargs.get('reading_date')
        self.max_temperature = kwargs.get('max_temperature')
        self.min_temperature = kwargs.get('min_temperature')
        self.max_humidity = kwargs.get('max_humidity')
        self.mean_humidity = kwargs.get('mean_humidity')


class WeatherReader:
    file_columns = [
        'date', 'max_temperature', 'mean_temperature', 'min_temperature',
        'dew_point', 'mean_dew_point', 'min_dew_point', 'max_humidity',
        'mean_humidity', 'min_humidity', 'max_sea_level_pressure',
        'mean_sea_level_pressure', 'min_sea_level_pressure', 'max_visibility',
        'mean_visibility', 'min_visibility', 'max_wind_speed', 'mean_wind_speed',
        'max_guest_speed', 'precipitation', 'cloud_cover', 'events', 'wind_dir'
    ]

    @staticmethod
    def create_reading(row):
        kwargs = {
            'reading_date': datetime.strptime(row.get('date'), '%Y-%m-%d')
        }
        integer_columns = [
            'max_temperature', 'min_temperature', 'max_humidity', 'mean_humidity'
        ]
        for column in integer_columns:
            value = row.get(column)
            kwargs[column] = int(value) if value else None

        return WeatherReading(kwargs)

    def read_file(self, file_name, file_dir='', skip_first_line=True):
        month_readings = []
        file_path = os.path.join(file_dir, file_name)
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f, fieldnames=WeatherReader.file_columns)
            if skip_first_line:
                next(reader)
            for row in reader:
                month_readings.append(self.create_reading(row))

        return month_readings


def remove_file_extension(file_name):
    return os.path.splitext(file_name)[0]


def apply_func(func, key_column, readings):
    return func([row for row in readings if row.__getattribute__(key_column) is not None],
                key=lambda obj: obj.__getattribute__(key_column))


def calculate_average(key_column, readings):
    reading_points = [row.__getattribute__(key_column)
                      for row in readings if row.__getattribute__(key_column) is not None]
    return sum(reading_points) / len(reading_points)


def yearly_report(file_names, weather_readings):
    to_format = '%B %d'
    months_readings = [weather_readings[remove_file_extension(file_name)] for file_name in file_names]
    full_year_readings = list(chain(*months_readings))

    max_temp_row = apply_func(max, 'max_temperature', full_year_readings)
    min_temp_row = apply_func(min, 'min_temperature', full_year_readings)
    max_humid_row = apply_func(max, 'max_humidity', full_year_readings)

    date_strs = [date.strftime(to_format) for date in [
        max_temp_row.reading_date, min_temp_row.reading_date, max_humid_row.reading_date]]
    date_iter = iter(date_strs)

    print('Highest: {:.2f}C on {}'.format(int(max_temp_row.max_temperature), next(date_iter)))
    print('Lowest: {:.2f}C on {}'.format(int(min_temp_row.min_temperature), next(date_iter)))
    print('Humidity: {:.2f}% on {}'.format(int(max_humid_row.max_humidity), next(date_iter)))


def monthly_report(file_name, weather_readings):
    avg_highest = calculate_average('max_temperature', weather_readings[remove_file_extension(file_name)])
    avg_lowest = calculate_average('min_temperature', weather_readings[remove_file_extension(file_name)])
    avg_mean_humidity = calculate_average('mean_humidity', weather_readings[remove_file_extension(file_name)])

    print('Highest Average: {:.2f}C'.format(avg_highest))
    print('Lowest Average: {:.2f}C'.format(avg_lowest))
    print('Average Mean Humidity: {:.2f}%'.format(avg_mean_humidity))


def print_symbol(symbol, value, color):
    text = '{}'.format(symbol * value)
    print(color + text + TerminalColors.RESET, end='')


def two_row_chart(day_no, max_t, min_t):
    def helper(value, color):
        print(day_no, end=' ')
        print_symbol('+', value, color)
        print(' {}C'.format(value))

    if max_t is not None:
        helper(max_t, TerminalColors.RED)
    if min_t is not None:
        helper(min_t, TerminalColors.BLUE)


def one_row_chart(day_no, max_t, min_t):
    if max_t is not None and min_t is not None:
        print(day_no, end=' ')
        print_symbol('+', min_t, TerminalColors.BLUE)
        print_symbol('+', max_t, TerminalColors.RED)
        print(' {}C - {}C'.format(min_t, max_t))


def monthly_bar_chart(file_name, weather_readings, chart_type):
    month_readings = weather_readings[remove_file_extension(file_name)]
    for day_reading in month_readings:
        max_temperature, min_temperature = day_reading.max_temperature, day_reading.min_temperature
        day_no = '{0:02d}'.format(int(day_reading.reading_date.strftime('%d')))

        if chart_type == 'double':
            two_row_chart(day_no, max_temperature, min_temperature)
        elif chart_type == 'single':
            one_row_chart(day_no, max_temperature, min_temperature)


def generate_reports(switch_order, switch_wise_file_names, weather_readings):
    for switch in switch_order:
        file_names = switch_wise_file_names[switch]
        if not file_names:
            print('Files not available for option -%s' % switch)
            continue

        if switch == 'e':
            yearly_report(file_names, weather_readings)
        elif switch == 'a':
            monthly_report(file_names[0], weather_readings)
        elif switch == 'c':
            monthly_bar_chart(file_names[0], weather_readings, 'double')
        elif switch == 'c1':
            monthly_bar_chart(file_names[0], weather_readings, 'single')


def read_files(switch_wise_file_names, files_dir):
    file_names = set()
    all_weather_readings = {}
    weather_reader = WeatherReader()
    for switch in switch_wise_file_names:
        file_names.update(switch_wise_file_names[switch])

    file_names = list(file_names)
    for file_name in file_names:
        all_weather_readings[remove_file_extension(file_name)] = weather_reader.read_file(file_name, files_dir)

    return all_weather_readings


def get_file_names_to_read(switches, args, available_files):
    switch_wise_file_names = {}
    for s in switches:
        if s == 'e':
            regex = r'\w+' + args[s].strftime('%Y')
        elif s in ['a', 'c', 'c1']:
            regex = r'\w+' + args[s].strftime('%Y_%b')
        else:
            continue

        r = re.compile(regex)
        switch_wise_file_names[s] =\
            [file_name for file_name in available_files if r.match(file_name)]
    return switch_wise_file_names


def get_file_names_in_dir(dir_path):
    def check_is_file(file_name):
        return os.path.isfile(os.path.join(dir_path, file_name))

    try:
        files = os.listdir(dir_path)
    except FileNotFoundError:
        sys.exit('No such directory: %s' % dir_path)
    else:
        return [file_name for file_name in files if check_is_file(file_name)]


def valid_date(text, pattern, error_msg):
    try:
        date = datetime.strptime(text, pattern)
    except ValueError:
        raise argparse.ArgumentTypeError(error_msg)
    else:
        return date


def valid_year(text):
    msg = 'Invalid or out of range year(usage: yyyy): %s' % text
    return valid_date(text, '%Y', msg)


def valid_year_month(text):
    msg = 'Invalid of out of range year/month(usage: yyyy/mm): %s' % text
    return valid_date(text, '%Y/%m', msg)


def parse_arguments():
    usage_msg = 'PROG files_directory [-e yyyy] [-a yyyy/mm] [-c yyyy/mm] [-c1 yyyy/mm]'

    parser = argparse.ArgumentParser(usage=usage_msg)
    parser.add_argument('files_directory', type=str, help='data files directory path')
    parser.add_argument('-e', type=valid_year, help='usage: -e yyyy')
    parser.add_argument('-a', type=valid_year_month, help='usage: -a yyyy/mm')
    parser.add_argument('-c', type=valid_year_month, help='usage: -c yyyy/mm')
    parser.add_argument('-c1', type=valid_year_month, help='usage: -c1 yyyy/mm')
    args = vars(parser.parse_args())

    if len([x for x in args.values() if x]) < 2:
        sys.exit('usage: ' + usage_msg)
    return args


def main():
    args = parse_arguments()
    files_dir = args['files_directory']
    file_names_in_dir = get_file_names_in_dir(files_dir)
    switch_order = [arg.lstrip('-') for arg in sys.argv[2::2]]
    switch_wise_file_names = get_file_names_to_read(switch_order, args, file_names_in_dir)
    weather_readings = read_files(switch_wise_file_names, files_dir)
    generate_reports(switch_order, switch_wise_file_names, weather_readings)


if __name__ == '__main__':
    main()
