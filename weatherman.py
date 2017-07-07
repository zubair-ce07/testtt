#!~/Documents/myenv/bin/python3
'''generate weather reports from CSV files'''
import csv
import calendar
import os
import argparse
from termcolor import colored

from record import Record

__author__ = 'fakhar'


class CSV:
    '''creates a single CSV for all the required files'''

    def __init__(self, file_path, year, month=None):

        try:
            file_names = os.listdir(file_path)
        except:
            raise FileNotFoundError('The directory doesn\'t exist')
        years = []
        self.records = []
        try:
            type(int(year))
        except:
            raise ValueError('Enter year in YYYY format')
        if month:
            try:
                month = int(month)
            except:
                raise ValueError('Enter month in MM format')
            if month in range(1, len(calendar.month_name)):
                month = calendar.month_abbr[month]
            else:
                raise ValueError('Month number not valid')
        for file_name in file_names:
            if year in file_name:
                if month:
                    if month in file_name:
                        years.append(file_name)
                else:
                    years.append(file_name)
        if not years:
            raise ValueError('Data not available')
        for file_name in years:
            with open(file_path + os.path.sep + file_name) as csvfile:
                filereader = csv.DictReader(csvfile)
                for row in filereader:
                    new_record = Record(
                        row['PKT'], row['Max TemperatureC'],
                        row['Min TemperatureC'], row['Max Humidity'], row[' Mean Humidity'])
                    self.records.append(new_record)


def check_args():
    '''check if arguments are in valid format'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', nargs='*',
                        help='Extreme Weather Report, use -e YYYY YYYY....')
    parser.add_argument('-a', nargs='*',
                        help='Average Monthly Weather Report, use -a YYYY/MM YYYY/MM....')
    parser.add_argument('-c', nargs='*',
                        help='Average Monthly Weather Report, use -a YYYY/MM YYYY/MM....')
    parser.add_argument('file_path',
                        help='Directory to data, use relative path like dir/to/files')
    args = parser.parse_args()
    if args.e:
        for year in args.e:
            get_extreme_weather(CSV(args.file_path, year))
    if args.a:
        for year_month in args.a:
            get_month_average(CSV(args.file_path, year_month.split(
                '/')[0], year_month.split('/')[1]))
    if args.c:
        for year_month in args.c:
            print_weather_graph(
                CSV(args.file_path, year_month.split(
                    '/')[0], year_month.split('/')[1]))


def get_extreme_weather(csvfile):
    '''generate report for extreme weathers for a year'''

    max_temp = max([n for n in csvfile.records if isinstance(
        n.max_temp, int)], key=lambda x: x.max_temp)
    min_temp = min([n for n in csvfile.records if isinstance(
        n.min_temp, int)], key=lambda x: x.min_temp)
    max_humid = max([n for n in csvfile.records if isinstance(
        n.max_humidity, int)], key=lambda x: x.max_humidity)

    print_extreme_weather({'max_temp_record': max_temp,
                           'min_temp_record': min_temp, 'max_humid_record': max_humid})


def print_extreme_weather(extreme_weathers):

    print('Highest: {:02d}C on {} {:02d}'.format(
        extreme_weathers['max_temp_record'].max_temp,
        calendar.month_name[extreme_weathers['max_temp_record'].date.month],
        extreme_weathers['max_temp_record'].date.day))

    print('Lowest: {:02d}C on {} {:02d}'.format(
        extreme_weathers['min_temp_record'].min_temp,
        calendar.month_name[extreme_weathers['min_temp_record'].date.month],
        extreme_weathers['min_temp_record'].date.day))

    print('Humidity: {:02d}% on {} {:02d}'.format(
        extreme_weathers['max_humid_record'].max_humidity,
        calendar.month_name[extreme_weathers['max_humid_record'].date.month],
        extreme_weathers['max_humid_record'].date.day), end='\n\n')


def get_month_average(csvfile):
    '''generate monthly averages'''

    avg_high_temp = [
        n.max_temp for n in csvfile.records if isinstance(n.max_temp, int)]

    avg_low_temp = [
        n.min_temp for n in csvfile.records if isinstance(n.min_temp, int)]

    avg_mean_humid = [
        n.mean_humidity for n in csvfile.records if isinstance(n.mean_humidity, int)]

    print_month_average({'avg_high_temp': avg_high_temp,
                         'avg_low_temp': avg_low_temp, 'avg_mean_humid': avg_mean_humid})


def print_month_average(month_averages):
    print('Highest Average: {:02d}C'.format(
        sum(month_averages['avg_high_temp']) // len(month_averages['avg_high_temp'])))

    print('Lowest Average: {:02d}C'.format(
        sum(month_averages['avg_low_temp']) // len(month_averages['avg_low_temp'])))

    print('Average Mean Humidity: {:02d}%'.format(
        sum(month_averages['avg_mean_humid']) // len(month_averages['avg_mean_humid'])), end='\n\n')


def print_weather_graph(csvfile):
    '''create monthly graphs'''
    print(calendar.month_name[csvfile.records[0].date.month],
          csvfile.records[0].date.year)
    for i in csvfile.records:
        if isinstance(i.max_temp, int):
            print('{:02d} '.format(i.date.day) + colored('+', 'red') * i.max_temp
                  + ' {:02d}C\n{:02d} '.format(i.max_temp, i.date.day) +
                  colored('+', 'blue') * i.min_temp
                  + ' {:02d}C'.format(i.min_temp))
    print()
    print(calendar.month_name[csvfile.records[0].date.month],
          csvfile.records[0].date.year)
    for i in csvfile.records:
        if isinstance(i.max_temp, int):
            print('{:02d} '.format(i.date.day) + colored('+', 'blue') * i.min_temp
                  + colored('+', 'red') * i.max_temp
                  + ' {:02d}C - {:02d}C'.format(i.min_temp, i.max_temp))
    print()


def main():
    '''generate weather reports'''
    check_args()


if __name__ == '__main__':
    main()
