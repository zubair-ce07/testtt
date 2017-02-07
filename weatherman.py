"""
This Module is used to calculate weather reports from data provided
in text files
"""

import csv
import argparse
from functools import reduce
from datetime import datetime
from os import path as os_path
from sys import argv as sys_argv, exit as sys_exit


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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


def calculate_yearly_report(files_data):
    results = {
        'max_temp_value': None,
        'max_temp_date': None,
        'min_temp_value': None,
        'min_temp_date': None,
        'max_humidity_value': None,
        'max_humidity_date': None
    }

    def computation(result, row):
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

    for data in files_data:
        results = reduce(computation, data, results)

    return results


def generate_yearly_report(dir_path, query_str, static_values):
    file_columns = static_values['file_columns']
    months = static_values['months']
    file_list = generate_file_names(query_str, static_values)

    files_data = []
    for file_name in file_list:
        file_path = os_path.join(dir_path, file_name)

        try:
            f = open(file_path, 'r')
        except FileNotFoundError:
            continue

        reader = csv.DictReader(f, fieldnames=file_columns)
        next(reader)

        file_data_rows = []
        for line in reader:
            file_data_rows.append(line)

        f.close()
        files_data.append(file_data_rows)

    results = calculate_yearly_report(files_data)
    print_yearly_report(results, months)


def print_monthly_report(results):
    avg_highest = results['max_temp_sum'] / results['max_temp_count']
    avg_lowest = results['min_temp_sum'] / results['min_temp_count']
    avg_mean_humidity = results['mean_humidity_sum'] / results['mean_humidity_count']

    print('Highest Average: {:.2f}C'.format(avg_highest))
    print('Lowest Average: {:.2f}C'.format(avg_lowest))
    print('Average Mean Humidity: {:.2f}%'.format(avg_mean_humidity))


def calculate_monthly_report(data_rows):
    initial_values = {
        'max_temp_sum': 0,
        'max_temp_count': 0,
        'min_temp_sum': 0,
        'min_temp_count': 0,
        'mean_humidity_sum': 0,
        'mean_humidity_count': 0
    }

    def computation(result, row):
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

    return reduce(computation, data_rows, initial_values)


def generate_monthly_report(dir_path, query_str, static_values):
    file_columns = static_values['file_columns']

    file_name = generate_file_names(query_str, static_values)[0]
    file_path = os_path.join(dir_path, file_name)

    try:
        f = open(file_path, 'r')
    except FileNotFoundError:
        error_msg = 'file not available: {}'.format(file_path)
        print(error_msg)
        return

    file_data_rows = []
    reader = csv.DictReader(f, fieldnames=file_columns)
    next(reader)
    for line in reader:
        file_data_rows.append(line)
    f.close()

    results = calculate_monthly_report(file_data_rows)
    print_monthly_report(results)


def generate_file_names(query_str, static_values):
    months = static_values['months']
    file_prefix = static_values['file_prefix']
    file_ext = static_values['data_file_ext']

    lst = query_str.split('/')
    size = len(lst)
    file_list = []

    if size == 1:
        year = lst[0]
        for m in months:
            file_list.append(
                file_prefix + year + '_' + m[:3] + file_ext)
    elif size == 2:
        year = lst[0]
        month = int(lst[1])
        file_list.append(
            file_prefix + year + '_' + months[month-1][:3] + file_ext)

    return file_list


def get_day_name(date, months):
    if not date:
        return ''

    lst = date.split('-')
    month = int(lst[1]) - 1
    day = lst[2]
    return '{} {}'.format(months[month], day)


def draw_chart(value, color):
    if color == 'red':
        use_color = Bcolors.FAIL
    elif color == 'blue':
        use_color = Bcolors.OKBLUE
    else:
        use_color = Bcolors.ENDC

    text = '{}'.format('+' * value)
    print(use_color + text + Bcolors.ENDC, end='')


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
    months = static_values['months']

    file_name = generate_file_names(query_str, static_values)[0]
    file_path = os_path.join(dir_path, file_name)

    try:
        f = open(file_path, 'r')
    except FileNotFoundError:
        error_msg = 'file not available: {}'.format(file_path)
        print(error_msg)
        return

    reader = csv.DictReader(f, fieldnames=file_columns)
    next(reader)

    lst = query_str.split('/')
    m = int(lst[1])-1
    print('{} {}'.format(months[m], lst[0]))

    file_data_rows = []
    for line in reader:
        file_data_rows.append(line)

    f.close()
    print_monthly_bar_chart(file_data_rows, chart_type)


def generate_report(dir_path, key, value, static_values):
    if key == 'e':
        generate_yearly_report(dir_path, value, static_values)
    elif key == 'a':
        generate_monthly_report(dir_path, value, static_values)
    elif key == 'c':
        monthly_bar_chart(dir_path, value, 'double', static_values)
    elif key == 'c1':
        monthly_bar_chart(dir_path, value, 'single', static_values)


def check_valid_year(year):
    try:
        datetime.strptime(year, '%Y')
    except ValueError:
        sys_exit('Invalid or out of range year(usage: yyyy): %s' % year)


def valid_year_month(text):
    try:
        datetime.strptime(text, '%Y/%m')
    except ValueError:
        sys_exit('Invalid of out of range year/month(usage: yyyy/mm): %s' % text)


def argument_order(args):
    iterator = iter(args)
    lst = []
    for item in iterator:
        lst.append(item.lstrip('-'))
        next(iterator)

    return lst


def validate_arguments(args):
    if args.e:
        check_valid_year(args.e)
    if args.a:
        valid_year_month(args.a)
    if args.c:
        valid_year_month(args.c)
    if args.c1:
        valid_year_month(args.c1)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_path', type=str, help='data files directory path')
    parser.add_argument('-e', type=str, help='usage: -e yyyy')
    parser.add_argument('-a', type=str, help='usage: -a yyyy/mm')
    parser.add_argument('-c', type=str, help='usage: -c yyyy/mm')
    parser.add_argument('-c1', type=str, help='usage: -c1 yyyy/mm')
    return parser.parse_args()


def main():
    static_values = {
        'usage_error': 'usage: path_to_files [-e yyyy] [-a yyyy/mm] [-c yyyy/mm]',
        'file_prefix': 'Murree_weather_',
        'data_file_ext': '.txt',
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

    if len(sys_argv) < 4:
        sys_exit(static_values.usage_error)

    args = parse_arguments()
    validate_arguments(args)
    args = vars(args)
    arg_order = argument_order(sys_argv[2:])
    for arg in arg_order:
        generate_report(sys_argv[1], arg, args[arg], static_values)


if __name__ == '__main__':
    main()
