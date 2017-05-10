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


def print_daily_temperature(high, low, date):
    colors = {'red': '0;31;20', 'blue': '0;34;20'}
    input_text_high = ''
    input_text_low = ''
    for i in range(0, high, 1):
        input_text_high += '+'
    for i in range(0, low, 1):
        input_text_low += '+'
    input_text_high = '\x1b[%sm %s \x1b[0m' % (colors['red'], input_text_high)
    input_text_low = '\x1b[%sm %s \x1b[0m' % (colors['blue'], input_text_low)
    print(date + input_text_high + str(high) + 'C')
    print(date + input_text_low + str(low) + 'C')


def print_daily_temperature_bonus(high, low, date):
    colors = {'red': '0;31;20', 'blue': '0;34;20'}
    input_text_high = ''
    input_text_low = ''
    for i in range(0, high, 1):
        input_text_high += '+'
    for i in range(0, low, 1):
        input_text_low += '+'
    input_text_high = '\x1b[%sm%s\x1b[0m' % (colors['red'], input_text_high)
    input_text_low = '\x1b[%sm%s\x1b[0m' % (colors['blue'], input_text_low)
    print(date + ' ' + input_text_low + input_text_high + ' ' + str(low) + 'C - ' + str(high) + 'C')


def parsing_monthly_input(path, input_year_month):
    months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',
              6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
              11: 'Nov', 12: 'Dec'}
    if '/' in input_year_month:
        year_month = input_year_month.split('/')
        if year_month[0].__len__() == 4:
            for file_name in os.listdir(path):
                if months[int(year_month[1])] in file_name and year_month[0] in file_name:
                    return file_name
    return None


def parsing_yearly_input(path, year):
    if year.__len__() == 4:
        file_names = []
        for file_name in os.listdir(path):
            if year in file_name:
                file_names.append(file_name)
        if file_names.__len__() > 0:
            return file_names
    return None


def parse_date(date):
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
              6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October',
              11: 'November', 12: 'December'}
    date_elements = date.split('-')
    return months[int(date_elements[1])] + " " + date_elements[2]


def display_average(args):
    filename = parsing_monthly_input(args.path, args.average)
    if filename:
        data_sum = [0, 0, 0, 0, 0, 0]
        with open(args.path + '/' + filename, 'rt') as sourcefile:
            reader = csv.DictReader(sourcefile)
            fieldnames = reader.fieldnames
            for row in reader:
                if row[fieldnames[1]]:
                    data_sum[0] += int(row[fieldnames[1]])
                    data_sum[1] += 1
                if row[fieldnames[3]]:
                    data_sum[2] += int(row[fieldnames[3]])
                    data_sum[3] += 1
                if row[fieldnames[8]]:
                    data_sum[4] += int(row[fieldnames[8]])
                    data_sum[5] += 1
        print ("Highest Average: " + str(round(data_sum[0] / data_sum[1])) + 'C')
        print ("Lowest Average: " + str(round(data_sum[2] / data_sum[3])) + 'C')
        print ("Average Mean Humidity: " + str(round(data_sum[4] / data_sum[5])) + '%')
    else:
        print ('Invalid -a input')


def display_extremes(args):
    files = parsing_yearly_input(args.path, args.extremes)
    if files:
        max_temp = {'date': None, 'temperature': None}
        min_temp = {'date': None, 'temperature': None}
        max_humid = {'date': None, 'percentage': None}
        for filename in files:
            with open(args.path + '/' + filename, 'rt') as sourcefile:
                reader = csv.DictReader(sourcefile)
                fieldnames = reader.fieldnames
                for row in reader:
                    if not max_temp['date']:
                        max_temp['date'] = row[fieldnames[0]]
                        min_temp['date'] = row[fieldnames[0]]
                        max_humid['date'] = row[fieldnames[0]]
                        max_temp['temperature'] = row[fieldnames[1]]
                        min_temp['temperature'] = row[fieldnames[3]]
                        max_humid['percentage'] = row[fieldnames[7]]
                    else:
                        if row[fieldnames[1]]:
                            if int(max_temp['temperature']) < int(row[fieldnames[1]]):
                                max_temp['temperature'] = row[fieldnames[1]]
                                max_temp['date'] = row[fieldnames[0]]
                        if row[fieldnames[3]]:
                            if int(min_temp['temperature']) > int(row[fieldnames[3]]):
                                min_temp['temperature'] = row[fieldnames[3]]
                                min_temp['date'] = row[fieldnames[0]]
                        if row[fieldnames[7]]:
                            if int(max_humid['percentage']) < int(row[fieldnames[7]]):
                                max_humid['percentage'] = row[fieldnames[7]]
                                max_humid['date'] = row[fieldnames[0]]
        print ("Highest: " + max_temp['temperature'] + 'C on ' + parse_date(max_temp['date']))
        print ("Lowest: " + min_temp['temperature'] + 'C on ' + parse_date(min_temp['date']))
        print ("Humidity: " + max_humid['percentage'] + '% on ' + parse_date(max_humid['date']))
    else:
        print ('Invalid -e input')


def display_charts(args):
    filename = parsing_monthly_input(args.path, args.charts)
    if filename:
        with open(args.path + '/' + filename, 'rt') as sourcefile:
            reader = csv.DictReader(sourcefile)
            fieldnames = reader.fieldnames
            for row in reader:
                if row[fieldnames[1]] and row[fieldnames[3]]:
                    print_daily_temperature(int(row[fieldnames[1]]), int(row[fieldnames[3]]),
                                            row[fieldnames[0]].split('-')[2])
                    print_daily_temperature_bonus(int(row[fieldnames[1]]), int(row[fieldnames[3]]),
                                                  row[fieldnames[0]].split('-')[2])
    else:
        print ('Invalid -c input')


if __name__ == '__main__':
    arguments = parsing_arguments()
    if arguments.extremes:
        display_extremes(arguments)
    if arguments.average:
        display_average(arguments)
    if arguments.charts:
        display_charts(arguments)
