import argparse
import csv
import os


def parsing_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path of the weatherfiles")
    parser.add_argument("-e", "--extremes", action="store")
    parser.add_argument("-a", "--average", action="store")
    parser.add_argument("-c", "--charts", action="store")
    return parser.parse_args()


def format_text(text, color_flag):
    if not text:
        return ''
    colors = {'red': '0;31;20', 'blue': '0;34;20'}
    stringformat = '\x1b[{}m{}\x1b[0m'
    if color_flag:
        return stringformat.format(colors['red'], text)
    else:
        return stringformat.format(colors['blue'], text)


def print_daily_temperature(high, low, date):
    input_text_high = ''
    input_text_low = ''
    for i in range(0, high, 1):
        input_text_high += '+'
    for i in range(0, low, 1):
        input_text_low += '+'
    print ('{0} {1} {2}C'.format(date, format_text(input_text_high, True), str(high)))
    print ('{0} {1} {2}C'.format(date, format_text(input_text_low, False), str(low)))


def print_daily_temperature_bonus(high, low, date):
    input_text_high = ''
    input_text_low = ''
    for i in range(0, high, 1):
        input_text_high += '+'
    for i in range(0, low, 1):
        input_text_low += '+'
    print ('{0} {1}{2} {3}C - {4}C'.format(date, format_text(input_text_low, False),
                                           format_text(input_text_high, True), str(low), str(high)))


def parsing_monthly_input(path, input_year_month):
    months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',
              6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
              11: 'Nov', 12: 'Dec'}
    if '/' in input_year_month:
        year_month = input_year_month.split('/')
        if len(year_month[0]) == 4:
            for file_name in os.listdir(path):
                if months[int(year_month[1])] in file_name and year_month[0] in file_name:
                    return file_name


def parsing_yearly_input(path, year):
    if len(year) == 4:
        file_names = []
        for file_name in os.listdir(path):
            if year in file_name:
                file_names.append(file_name)
        return file_names


def parse_date(date):
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
              6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October',
              11: 'November', 12: 'December'}
    date_elements = date.split('-')
    return months[int(date_elements[1])] + " " + date_elements[2]


def display_average(args):
    filename = parsing_monthly_input(args.path, args.average)
    if not filename:
        print ('Invalid -a input')
        return
    data_sum = [0, 0, 0, 0, 0, 0]
    with open(args.path + '/' + filename, 'rt') as sourcefile:
        reader = csv.DictReader(sourcefile)
        for row in reader:
            if row.get('Max TemperatureC'):
                data_sum[0] += int(row.get('Max TemperatureC'))
                data_sum[1] += 1
            if row.get('Min TemperatureC'):
                data_sum[2] += int(row.get('Min TemperatureC'))
                data_sum[3] += 1
            if row.get(' Mean Humidity'):
                data_sum[4] += int(row.get(' Mean Humidity'))
                data_sum[5] += 1
    print ('Highest Average: {0}C'.format(str(round(data_sum[0] / data_sum[1]))))
    print ('Lowest Average: {0}C'.format(str(round(data_sum[2] / data_sum[3]))))
    print ('Average Mean Humidity: {0}%'.format(str(round(data_sum[4] / data_sum[5]))))


def display_extremes(args):
    files = parsing_yearly_input(args.path, args.extremes)
    if not files:
        print ('Invalid -e input')
        return
    max_temp = {'date': None, 'temperature': None}
    min_temp = {'date': None, 'temperature': None}
    max_humid = {'date': None, 'percentage': None}
    for filename in files:
        with open(args.path + '/' + filename, 'rt') as sourcefile:
            reader = csv.DictReader(sourcefile)
            for row in reader:
                if not max_temp['date']:
                    max_temp['date'] = row.get('PKT') or row.get('PKST')
                    min_temp['date'] = row.get('PKT') or row.get('PKST')
                    max_humid['date'] = row.get('PKT') or row.get('PKST')
                    max_temp['temperature'] = row.get('Max TemperatureC')
                    min_temp['temperature'] = row.get('Min TemperatureC')
                    max_humid['percentage'] = row.get('Max Humidity')
                else:
                    if row.get('Max TemperatureC'):
                        if int(max_temp['temperature']) < int(row.get('Max TemperatureC')):
                            max_temp['temperature'] = row.get('Max TemperatureC')
                            max_temp['date'] = row.get('PKT') or row.get('PKST')
                    if row.get('Min TemperatureC'):
                        if int(min_temp['temperature']) > int(row.get('Min TemperatureC')):
                            min_temp['temperature'] = row.get('Min TemperatureC')
                            min_temp['date'] = row.get('PKT') or row.get('PKST')
                    if row.get('Max Humidity'):
                        if int(max_humid['percentage']) < int(row.get('Max Humidity')):
                            max_humid['percentage'] = row.get('Max Humidity')
                            max_humid['date'] = row.get('PKT') or row.get('PKST')

    print ('Highest: {0}C on {1}'.format(max_temp['temperature'], parse_date(max_temp['date'])))
    print ('Lowest: {0}C on {1}'.format(min_temp['temperature'], parse_date(min_temp['date'])))
    print ('Humidity: {0}% on {1}'.format(max_humid['percentage'], parse_date(max_humid['date'])))


def display_charts(args):
    filename = parsing_monthly_input(args.path, args.charts)
    if not filename:
        print ('Invalid -c input')
        return
    with open(args.path + '/' + filename, 'rt') as sourcefile:
        reader = csv.DictReader(sourcefile)
        for row in reader:
            if row.get('Max TemperatureC') and row.get('Min TemperatureC'):
                print_daily_temperature(int(row.get('Max TemperatureC')), int(row.get('Min TemperatureC')),
                                        (row.get('PKT') or row.get('PKST')).split('-')[2])
                print_daily_temperature_bonus(int(row.get('Max TemperatureC')), int(row.get('Min TemperatureC')),
                                              (row.get('PKT') or row.get('PKST')).split('-')[2])


if __name__ == '__main__':
    arguments = parsing_arguments()
    if arguments.extremes:
        display_extremes(arguments)
    if arguments.average:
        display_average(arguments)
    if arguments.charts:
        display_charts(arguments)
