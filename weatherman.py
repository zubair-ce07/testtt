"""
This Module is used to calculate weather reports from data provided
in text files
"""

import csv
import argparse
from pathlib import Path
from functools import reduce
from datetime import datetime
from re import compile as re_compile
from os import path as os_path, listdir as os_listdir
from sys import argv as sys_argv, exit as sys_exit


class TerminalColors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ReadCSVFile:
    def __init__(self, file_name, file_dir='', field_names=None, skip_first_line=True):
        self.file_path = os_path.join(file_dir, file_name)
        self.file_data = []
        self.field_names = field_names
        self.skip_first_line = skip_first_line
        if not Path(self.file_path).is_file():
            raise FileNotFoundError('No such file: {}'.format(self.file_path))

    def read_file(self):
        f = open(self.file_path, 'r')
        reader = csv.DictReader(f, fieldnames=self.field_names)

        if self.skip_first_line:
            next(reader)

        for line in reader:
            self.file_data.append(line)
        f.close()

        return self.file_data


def compare_numbers(a, b):
    return a - b


def print_yearly_report(results, months):
    value = results['max_temp_value']
    date = results['max_temp_date']
    print('Highest: {:.2f}C on {}'.format(value, get_day_name(date, months)))

    value = results['min_temp_value']
    date = results['min_temp_date']
    print('Lowest: {:.2f}C on {}'.format(value, get_day_name(date, months)))

    value = results['max_humidity_value']
    date = results['max_humidity_date']
    print('Humidity: {:.2f}% on {}'.format(value, get_day_name(date, months)))


def yearly_computation(result, row):
    date = row['date']
    max_temperature = row['max_temperature']
    min_temperature = row['min_temperature']
    max_humidity = row['max_humidity']

    if max_temperature:
        max_temperature = int(max_temperature)
        if result['max_temp_value'] is None or \
                compare_numbers(max_temperature, result['max_temp_value']) > 0:
            result['max_temp_value'] = max_temperature
            result['max_temp_date'] = date
    if min_temperature:
        min_temperature = int(min_temperature)
        if result['min_temp_value'] is None or \
                compare_numbers(result['min_temp_value'], min_temperature) > 0:
            result['min_temp_value'] = min_temperature
            result['min_temp_date'] = date
    if max_humidity:
        max_humidity = int(max_humidity)
        if result['max_humidity_value'] is None or \
                compare_numbers(max_humidity, result['max_humidity_value']) > 0:
            result['max_humidity_value'] = max_humidity
            result['max_humidity_date'] = date

    return result


def calculate_yearly_report(files_data):
    results = {
        'max_temp_value': None,
        'max_temp_date': None,
        'min_temp_value': None,
        'min_temp_date': None,
        'max_humidity_value': None,
        'max_humidity_date': None
    }

    for data in files_data:
        results = reduce(yearly_computation, data, results)

    return results


def categorise_location_files_of_year(year):
    def categorise_location_files(result, file_name):
        location = file_name.split(year)[0]
        if location not in result:
            result[location] = []

        result[location].append(file_name)
        return result

    return categorise_location_files


def generate_yearly_report(dir_path, year, static_values):
    file_columns = static_values['file_columns']
    months = static_values['months']
    file_names = select_file_names(year, static_values)
    categorise_location_files = categorise_location_files_of_year(year)
    location_files = reduce(categorise_location_files, file_names, {})

    for location in location_files:
        print(location.rstrip('_'))
        files_data = []
        file_list = location_files[location]
        for file_name in file_list:
            try:
                csv_file = ReadCSVFile(file_name, dir_path, file_columns)
                file_data = csv_file.read_file()
            except (FileNotFoundError, IOError):
                continue

            files_data.append(file_data)

        results = calculate_yearly_report(files_data)
        print_yearly_report(results, months)


def print_monthly_report(results):
    avg_highest = results['max_temp_sum'] / results['max_temp_count']
    avg_lowest = results['min_temp_sum'] / results['min_temp_count']
    avg_mean_humidity = results['mean_humidity_sum'] / results['mean_humidity_count']

    print('Highest Average: {:.2f}C'.format(avg_highest))
    print('Lowest Average: {:.2f}C'.format(avg_lowest))
    print('Average Mean Humidity: {:.2f}%'.format(avg_mean_humidity))


def monthly_computation(result, row):
    max_temperature = row['max_temperature']
    min_temperature = row['min_temperature']
    mean_humidity = row['mean_humidity']

    if max_temperature:
        result['max_temp_sum'] += int(max_temperature)
        result['max_temp_count'] += 1
    if min_temperature:
        result['min_temp_sum'] += int(min_temperature)
        result['min_temp_count'] += 1
    if mean_humidity:
        result['mean_humidity_sum'] += int(mean_humidity)
        result['mean_humidity_count'] += 1

    return result


def calculate_monthly_report(data_rows):
    initial_values = {
        'max_temp_sum': 0,
        'max_temp_count': 0,
        'min_temp_sum': 0,
        'min_temp_count': 0,
        'mean_humidity_sum': 0,
        'mean_humidity_count': 0
    }

    return reduce(monthly_computation, data_rows, initial_values)


def generate_monthly_report(dir_path, query_str, static_values):
    file_columns = static_values['file_columns']
    file_names = select_file_names(query_str, static_values)
    if not file_names:
        sys_exit('Data files not available for: %s' % query_str)

    for file_name in file_names:
        print(os_path.splitext(file_name)[0])
        try:
            csv_file = ReadCSVFile(file_name, dir_path, file_columns)
            file_data = csv_file.read_file()
        except (FileNotFoundError, IOError) as e:
            print(str(e))
            return

        results = calculate_monthly_report(file_data)
        print_monthly_report(results)


def select_file_names(query_str, static_values):
    months = static_values['months']
    file_names = static_values['file_names']

    lst = query_str.split('/')
    size = len(lst)
    regex = r'\w+'

    year = lst[0]
    regex += year

    if size == 2:
        month = int(lst[1])
        regex += '_' + months[month-1][:3]

    r = re_compile(regex)
    return list(filter(r.match, file_names))


def get_day_name(date, months):
    if not date:
        return ''

    lst = date.split('-')
    month = int(lst[1]) - 1
    day = lst[2]
    return '{} {}'.format(months[month], day)


def draw_chart(value, color):
    if color == 'red':
        use_color = TerminalColors.RED
    elif color == 'blue':
        use_color = TerminalColors.BLUE
    else:
        use_color = TerminalColors.RESET

    text = '{}'.format('+' * value)
    print(use_color + text + TerminalColors.RESET, end='')


def two_row_chart(day_no, max_t, min_t):
    if max_t:
        print(day_no, end=' ')
        draw_chart(int(max_t), 'red')
        print(' {}C'.format(int(max_t)))

    if min_t:
        print(day_no, end=' ')
        draw_chart(int(min_t), 'blue')
        print(' {}C'.format(int(min_t)))


def one_row_chart(day_no, max_t, min_t):
    if max_t and min_t:
        print(day_no, end=' ')
        draw_chart(int(min_t), 'blue')
        draw_chart(int(max_t), 'red')
        print(' {}C - {}C'.format(int(min_t), int(max_t)))


def print_monthly_bar_chart(data_rows, chart_type):
    for row in data_rows:
        date = row['date']
        max_temperature = row['max_temperature']
        min_temperature = row['min_temperature']

        day_no = '{0:02d}'.format(int(date.split('-')[2]))

        if chart_type == 'double':
            two_row_chart(day_no, max_temperature, min_temperature)
        elif chart_type == 'single':
            one_row_chart(day_no, max_temperature, min_temperature)


def monthly_bar_chart(dir_path, query_str, chart_type, static_values):
    file_columns = static_values['file_columns']
    file_names = select_file_names(query_str, static_values)
    if not file_names:
        sys_exit('Data files not available for: %s' % query_str)

    for file_name in file_names:
        print(os_path.splitext(file_name)[0])
        try:
            csv_file = ReadCSVFile(file_name, dir_path, file_columns)
            file_data = csv_file.read_file()
        except (FileNotFoundError, IOError) as e:
            print(str(e))
            continue

        print_monthly_bar_chart(file_data, chart_type)


def get_files_in_dir(dir_path):
    def check_is_file(file_name):
        return os_path.isfile(os_path.join(dir_path, file_name))

    try:
        files = os_listdir(dir_path)
    except FileNotFoundError:
        print('No such directory: %s' % dir_path)
    else:
        return list(filter(check_is_file, files))


def generate_report(dir_path, key, value, static_values):
    if key == 'e':
        generate_yearly_report(dir_path, value, static_values)
    elif key == 'a':
        generate_monthly_report(dir_path, value, static_values)
    elif key == 'c':
        monthly_bar_chart(dir_path, value, 'double', static_values)
    elif key == 'c1':
        monthly_bar_chart(dir_path, value, 'single', static_values)


def valid_text(text, pattern, error_msg):
    try:
        datetime.strptime(text, pattern)
    except ValueError:
        raise argparse.ArgumentTypeError(error_msg)
    else:
        return text


def valid_year(year):
    msg = 'Invalid or out of range year(usage: yyyy): %s' % year
    return valid_text(year, '%Y', msg)


def valid_year_month(text):
    msg = 'Invalid of out of range year/month(usage: yyyy/mm): %s' % text
    return valid_text(text, '%Y/%m', msg)


def argument_order(args):
    iterator = iter(args)
    lst = []
    for item in iterator:
        lst.append(item.lstrip('-'))
        next(iterator)

    return lst


def parse_arguments(usage_msg):
    parser = argparse.ArgumentParser(usage=usage_msg)
    parser.add_argument('directory_path', type=str, help='data files directory path')
    parser.add_argument('-e', type=valid_year, help='usage: -e yyyy')
    parser.add_argument('-a', type=valid_year_month, help='usage: -a yyyy/mm')
    parser.add_argument('-c', type=valid_year_month, help='usage: -c yyyy/mm')
    parser.add_argument('-c1', type=valid_year_month, help='usage: -c1 yyyy/mm')
    return parser.parse_args()


def main():
    static_values = {
        'usage_msg': 'directory_path [-e yyyy] [-a yyyy/mm] [-c yyyy/mm]',
        'switches': [
            '-e', '-a', '-c', '-c1'
        ],
        'file_columns': [
            'date', 'max_temperature', 'mean_temperature', 'min_temperature',
            'dew_point', 'mean_dew_point', 'min_dew_point', 'max_humidity',
            'mean_humidity', 'min_humidity', 'max_sea_level_pressure',
            'mean_sea_level_pressure', 'min_sea_level_pressure', 'max_visibility',
            'mean_visibility', 'min_visibility', 'max_wind_speed', 'mean_wind_speed',
            'max_guest_speed', 'precipitation', 'cloud_cover', 'events', 'wind_dir'
        ],
        'months': [
            'January', 'February', 'March',
            'April', 'May', 'June',
            'July', 'August', 'September',
            'October', 'November', 'December'
        ]

    }

    args = parse_arguments(static_values['usage_msg'])
    args = vars(args)
    if len(list(filter(lambda x: x, args.values()))) < 2:
        sys_exit('usage: ' + static_values['usage_msg'])

    files_directory = args['directory_path']
    file_names = get_files_in_dir(files_directory)
    if not file_names:
        sys_exit('No files found in directory %s' % files_directory)
    else:
        static_values['file_names'] = file_names

    arg_order = argument_order(sys_argv[2:])
    for arg in arg_order:
        generate_report(files_directory, arg, args[arg], static_values)


if __name__ == '__main__':
    main()
