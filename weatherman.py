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


class WeatherReadings:
    def __init__(self):
        self.all_weather_readings = {}

    @staticmethod
    def generate_file_key(file_name):
        return os.path.splitext(file_name)[0]

    def read_file(self, file_name, file_dir='', field_names=None, skip_first_line=True):
        month_readings_key = self.generate_file_key(file_name)
        if month_readings_key in self.all_weather_readings:
            return self.all_weather_readings[month_readings_key]

        file_path = os.path.join(file_dir, file_name)
        if not Path(file_path).is_file():
            raise FileNotFoundError('No such file: {}'.format(file_path))

        month_readings = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f, fieldnames=field_names)
            if skip_first_line:
                next(reader)
            for day_readings in reader:
                month_readings.append(day_readings)

        self.all_weather_readings[month_readings_key] = month_readings
        return month_readings

    def get_month_readings(self, file_name):
        month_readings_key = self.generate_file_key(file_name)
        if month_readings_key in self.all_weather_readings:
            return self.all_weather_readings[month_readings_key]
        return None


def apply_func(func, key_column, readings):
    return func([row for row in readings if row[key_column]], key=lambda row: int(row[key_column]))


def calculate_average(key_column, readings):
    map_iter = map(lambda row: int(row[key_column]), [row for row in readings if row[key_column]])
    reading_points = list(map_iter)
    return sum(reading_points) / len(reading_points)


def yearly_report(file_names, weather_readings):
    from_format, to_format = '%Y-%m-%d', '%B %d'
    months_readings = map(lambda file_name: weather_readings.get_month_readings(file_name), file_names)
    full_year_readings = list(chain(*months_readings))

    max_temp_row = apply_func(max, 'max_temperature', full_year_readings)
    min_temp_row = apply_func(min, 'min_temperature', full_year_readings)
    max_humid_row = apply_func(max, 'max_humidity', full_year_readings)
    map_iter = map(lambda date: create_date_str(
        date, from_format, to_format), [max_temp_row['date'], min_temp_row['date'], max_humid_row['date']])

    print('Highest: {:.2f}C on {}'.format(int(max_temp_row['max_temperature']), next(map_iter)))
    print('Lowest: {:.2f}C on {}'.format(int(min_temp_row['min_temperature']), next(map_iter)))
    print('Humidity: {:.2f}% on {}'.format(int(max_humid_row['max_humidity']), next(map_iter)))


def monthly_report(file_name, weather_readings):
    avg_highest = calculate_average('max_temperature', weather_readings.get_month_readings(file_name))
    avg_lowest = calculate_average('min_temperature', weather_readings.get_month_readings(file_name))
    avg_mean_humidity = calculate_average('mean_humidity', weather_readings.get_month_readings(file_name))

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

    if max_t:
        helper(int(max_t), TerminalColors.RED)
    if min_t:
        helper(int(min_t), TerminalColors.BLUE)


def one_row_chart(day_no, max_t, min_t):
    if max_t and min_t:
        max_t, min_t = int(max_t), int(min_t)
        print(day_no, end=' ')
        print_symbol('+', min_t, TerminalColors.BLUE)
        print_symbol('+', max_t, TerminalColors.RED)
        print(' {}C - {}C'.format(min_t, max_t))


def monthly_bar_chart(file_name, weather_readings, chart_type):
    month_readings = weather_readings.get_month_readings(file_name)
    for day_reading in month_readings:
        max_temperature, min_temperature = day_reading['max_temperature'], day_reading['min_temperature']
        day_no = create_date_str(day_reading['date'], '%Y-%m-%d', '%d')
        day_no = '{0:02d}'.format(int(day_no))

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


def create_date_str(date_str, current_format, target_format):
    try:
        date = datetime.strptime(date_str, current_format)
    except TypeError:
        return None
    else:
        return date.strftime(target_format)


def read_files(switch_wise_file_names, files_dir, field_names):
    weather_readings = WeatherReadings()
    for switch in switch_wise_file_names:
        map_iter = map(lambda file_name: weather_readings.read_file(
            file_name, files_dir, field_names), switch_wise_file_names[switch])
        list(map_iter)
    return weather_readings


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
    usage_msg = 'PROG directory_path [-e yyyy] [-a yyyy/mm] [-c yyyy/mm] [-c1 yyyy/mm]'

    parser = argparse.ArgumentParser(usage=usage_msg)
    parser.add_argument('directory_path', type=str, help='data files directory path')
    parser.add_argument('-e', type=valid_year, help='usage: -e yyyy')
    parser.add_argument('-a', type=valid_year_month, help='usage: -a yyyy/mm')
    parser.add_argument('-c', type=valid_year_month, help='usage: -c yyyy/mm')
    parser.add_argument('-c1', type=valid_year_month, help='usage: -c1 yyyy/mm')
    args = vars(parser.parse_args())

    if len([x for x in args.values() if x]) < 2:
        sys.exit('usage: ' + usage_msg)
    return args


def main():
    file_columns = [
        'date', 'max_temperature', 'mean_temperature', 'min_temperature',
        'dew_point', 'mean_dew_point', 'min_dew_point', 'max_humidity',
        'mean_humidity', 'min_humidity', 'max_sea_level_pressure',
        'mean_sea_level_pressure', 'min_sea_level_pressure', 'max_visibility',
        'mean_visibility', 'min_visibility', 'max_wind_speed', 'mean_wind_speed',
        'max_guest_speed', 'precipitation', 'cloud_cover', 'events', 'wind_dir'
    ]
    args = parse_arguments()
    dir_path = args['directory_path']
    file_names_in_dir = get_file_names_in_dir(dir_path)
    switch_order = list(map(lambda x: x.lstrip('-'), sys.argv[2::2]))
    switch_wise_file_names = get_file_names_to_read(switch_order, args, file_names_in_dir)
    weather_readings = read_files(switch_wise_file_names, dir_path, file_columns)
    generate_reports(switch_order, switch_wise_file_names, weather_readings)


if __name__ == '__main__':
    main()
