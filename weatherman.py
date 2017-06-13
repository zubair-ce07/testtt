import argparse
import csv
import fnmatch
import os
import calendar
import datetime


def get_pattern(year, month = None):
    pattern = ''
    if month is not None:
        pattern = calendar.month_abbr[month]
    return '*' + str(year) + '_' + pattern + '*'

def mean(l):
    return sum(map(int, l)) / len(l)


def print_year(high_temp, low_temp, humid):
    print 'Highest: ' + high_temp[1] + 'C' + ' on ' + datetime.datetime(int(high_temp[0].split('-')[0]), int(high_temp[0].split('-')[1]),
                                                                        int(high_temp[0].split('-')[2])).strftime('%B %m')
    print 'Lowest: ' + low_temp[1] + 'C' + ' on ' + datetime.datetime(int(low_temp[0].split('-')[0]), int(low_temp[0].split('-')[1]),
                                                                        int(low_temp[0].split('-')[2])).strftime('%B %m')
    print 'Humid: ' + humid[1] + '%' + ' on ' + datetime.datetime(int(humid[0].split('-')[0]), int(humid[0].split('-')[1]),
                                                                        int(humid[0].split('-')[2])).strftime('%B %m')

def print_month(high, low, humid):
    print 'Highest Average: ' + str(high)
    print 'Lowest Average: ' + str(low)
    print 'Average Mean Humidity: ' + str(humid)


def print_chart(result_set):
    W = '\033[0m'  # white (normal)
    R = '\033[31m'  # red
    G = '\033[32m'  # green

    print(datetime.datetime(int(result_set[0][0].split('-')[0]),
                      int(result_set[0][0].split('-')[1]),
                      int(result_set[0][0].split('-')[2])).strftime('%B %Y'))
    for record in result_set:
        print (record[0].split('-')[2] + ' ' + R + int(record[1])*'+' + W + ' ' + record[1] + 'C')
        print (record[0].split('-')[2] + ' ' + G + int(record[2])*'+' + W + ' ' + record[2] + 'C')


def print_bonus(result_set):
    W = '\033[0m'  # white (normal)
    R = '\033[31m'  # red
    G = '\033[32m'  # green

    print(datetime.datetime(int(result_set[0][0].split('-')[0]),
                            int(result_set[0][0].split('-')[1]),
                            int(result_set[0][0].split('-')[2])).strftime('%B %Y'))
    for record in result_set:
        print (record[0].split('-')[2] + ' ' + G + int(record[2]) * '+' + R +
               int(record[1])*'+' + W + ' ' + record[2] + 'C - ' + record[1])
        #print (record[0].split('-')[2] + ' ' + R + int(record[1]) * '+' + W + ' ' + record[2] + 'C')
def get_columns(dir, file, columns):
    result_set = []
    with open(os.path.join(dir, file)) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result_set.append([row[column] for column in columns])
    return result_set


def filter_data(result_set):
    return [row for row in result_set if '' not in row]


def process_year(dir, year):
    result_set = []
    pattern = get_pattern(year)
    for file in os.listdir(dir):
        if fnmatch.fnmatch(file, pattern):
            result_set.extend(get_columns(dir, file, ['PKT', 'Max TemperatureC', 'Min TemperatureC', 'Max Humidity']))

    result_set = filter_data(result_set)
    return max(result_set, key=lambda item: int(item[1])), min(result_set, key=lambda item: int(item[2])), \
           max(result_set, key=lambda item: int(item[3]))


def process_month(dir, year, month):
    result_set = []
    pattern = get_pattern(year, month)
    for file in os.listdir(dir):
        if fnmatch.fnmatch(file, pattern):
            result_set = get_columns(dir, file, ['Max TemperatureC', 'Min TemperatureC', 'Max Humidity'])

    result_set = filter_data(result_set)
    return map(mean, zip(*result_set))

def process_chart(dir, year, month):
    result_set = []
    pattern = get_pattern(year, month)
    for file in os.listdir(dir):
        if fnmatch.fnmatch(file, pattern):
            result_set = get_columns(dir, file, ['PKT', 'Max TemperatureC', 'Min TemperatureC'])
    result_set = filter_data(result_set)
    return result_set


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="Path of the data directory")
    parser.add_argument("-e", help="Processing Year",
                        type=int)
    parser.add_argument("-a", help="Processing Year/MonthNumber")
    parser.add_argument("-c", help="Processing Chart Year/MonthNumber")
    parser.add_argument("-b", help="Processing Sinle-line Chart Year/MonthNumber")
    args = parser.parse_args()

    if args.e:
        result_set = process_year(args.dir, args.e)
        print_year(result_set[0], result_set[1], result_set[2])
    if args.a:
        result_set = process_month(args.dir, int(args.a.split('/')[0]), int(args.a.split('/')[1]))
        print_month(result_set[0], result_set[1], result_set[2])
    if args.c:
        result_set = process_chart(args.dir, int(args.c.split('/')[0]), int(args.c.split('/')[1]))
        print_chart(result_set)
    if args.b:
        result_set = process_chart(args.dir, int(args.b.split('/')[0]), int(args.b.split('/')[1]))
        print_bonus(result_set)
