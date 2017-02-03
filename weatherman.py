"""
This Module is used to calculate weather reports from data provided
in text files
"""

import csv
import argparse
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


def max_value():
    value = None
    date_str = None

    def update_value(t, date):
        nonlocal value, date_str
        if value is None or t > value:
            value = t
            date_str = date

    def get_value():
        return value, date_str

    return update_value, get_value


def min_value():
    value = None
    date_str = None

    def update_value(t, date):
        nonlocal value, date_str
        if value is None or t < value:
            value = t
            date_str = date

    def get_value():
        return value, date_str

    return update_value, get_value


def mean_value():
    value = 0
    count = 0

    def update_value(t):
        nonlocal value, count
        value += t
        count += 1

    def get_value():
        return value / count

    return update_value, get_value


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


def yearly_report(dir_path, query_str, static_values):
    file_columns = static_values['file_columns']
    months = static_values['months']

    file_list = generate_file_names(query_str, static_values)

    update_max_temp, get_max_temp = max_value()
    update_min_temp, get_min_temp = min_value()
    update_max_humidity, get_max_humidity = max_value()

    date_index = file_columns.index('date')
    max_temp_index = file_columns.index('max_temperature')
    min_temp_index = file_columns.index('min_temperature')
    max_humidity_index = file_columns.index('max_humidity')

    for file_name in file_list:
        file_path = os_path.join(dir_path, file_name)
        try:
            f = open(file_path, 'r')
        except FileNotFoundError:
            continue

        reader = csv.reader(f)
        next(reader)

        for line in reader:
            d = line[date_index]
            max_t = line[max_temp_index]
            min_t = line[min_temp_index]
            max_h = line[max_humidity_index]

            if max_t:
                update_max_temp(int(max_t), d)
            if min_t:
                update_min_temp(int(min_t), d)
            if max_h:
                update_max_humidity(int(max_h), d)

        f.close()

    value, date = get_max_temp()
    print('Highest: {:.2f}C on {}'.format(value, get_day_name(date, months)))

    value, date = get_min_temp()
    print('Lowest: {:.2f}C on {}'.format(value, get_day_name(date, months)))

    value, date = get_max_humidity()
    print('Humidity: {:.2f}% on {}'.format(value, get_day_name(date, months)))


def monthly_report(dir_path, query_str, static_values):
    file_columns = static_values['file_columns']

    file_name = generate_file_names(query_str, static_values)[0]
    file_path = os_path.join(dir_path, file_name)

    try:
        f = open(file_path, 'r')
    except FileNotFoundError:
        print('file not available: %s' % file_path)
        return

    reader = csv.reader(f)
    next(reader)

    update_avg_max_temp, get_avg_max_temp = mean_value()
    update_avg_min_temp, get_avg_min_temp = mean_value()
    update_avg_mean_humidity, get_avg_mean_humidity = mean_value()

    # date_index = file_columns.index('date')
    max_temp_index = file_columns.index('max_temperature')
    min_temp_index = file_columns.index('min_temperature')
    mean_humidity_index = file_columns.index('mean_humidity')

    for line in reader:
        # d = line[date_index]
        max_t = line[max_temp_index]
        min_t = line[min_temp_index]
        mean_h = line[mean_humidity_index]

        if max_t:
            update_avg_max_temp(int(max_t))
        if min_t:
            update_avg_min_temp(int(min_t))
        if mean_h:
            update_avg_mean_humidity(int(mean_h))

    f.close()

    print('Highest Average: {:.2f}C'.format(get_avg_max_temp()))
    print('Lowest Average: {:.2f}C'.format(get_avg_min_temp()))
    print('Average Mean Humidity: {:.2f}%'.format(get_avg_mean_humidity()))


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


def monthly_bar_chart(dir_path, query_str, chart_type, static_values):
    file_columns = static_values['file_columns']
    months = static_values['months']

    file_name = generate_file_names(query_str, static_values)[0]
    file_path = os_path.join(dir_path, file_name)

    try:
        f = open(file_path, 'r')
    except FileNotFoundError:
        print('file not available: %s' % file_path)
        return

    reader = csv.reader(f)
    next(reader)

    date_index = file_columns.index('date')
    max_temp_index = file_columns.index('max_temperature')
    min_temp_index = file_columns.index('min_temperature')

    lst = query_str.split('/')
    m = int(lst[1])-1
    print('{} {}'.format(months[m], lst[0]))

    for line in reader:
        d = line[date_index]
        max_t = line[max_temp_index]
        min_t = line[min_temp_index]

        day_no = '{0:02d}'.format(int(d.split('-')[2]))

        if chart_type == 'double':
            two_row_chart(day_no, max_t, min_t)
        elif chart_type == 'single':
            one_row_chart(day_no, max_t, min_t)

    f.close()


def generate_report(dir_path, key, value, static_values):
    if key == 'e':
        yearly_report(dir_path, value, static_values)
    elif key == 'a':
        monthly_report(dir_path, value, static_values)
    elif key == 'c':
        monthly_bar_chart(dir_path, value, 'double', static_values)
    elif key == 'c1':
        monthly_bar_chart(dir_path, value, 'single', static_values)


def check_valid_year(year):
    try:
        year = int(year)
    except ValueError:
        sys_exit('invalid year: %s' % year)
    else:
        if year > datetime.now().year or year < 1970:
            sys_exit('out of range year: %s' % year)


def check_valid_month(month):
    try:
        month = int(month)
    except ValueError:
        sys_exit('invalid month: %s' % month)
    else:
        if month < 1 or month > 12:
            sys_exit('out of range month: %s' % month)


def valid_year_month(text):
    lst = text.split('/')
    if len(lst) < 2:
        sys_exit('invalid switch value: %s' % str(text))
    check_valid_year(lst[0])
    check_valid_month(lst[1])


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
