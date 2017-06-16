#!~/Documents/myenv/bin/python3
'''generate weather reports from CSV files'''
import csv
import sys
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
        year_list = []
        self.record_list = []
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
                        year_list.append(file_name)
                else:
                    year_list.append(file_name)
        if not year_list:
            raise ValueError('Data not available')
        for file_name in year_list:
            with open(file_path + '/' + file_name) as csvfile:
                filereader = csv.DictReader(csvfile)
                for row in filereader:
                    new_record = Record(
                        row['PKT'], row['Max TemperatureC'],
                        row['Min TemperatureC'], row['Max Humidity'], row[' Mean Humidity'])
                    self.record_list.append(new_record)


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
            extreme_weather(CSV(args.file_path, year))
    if args.a:
        for year_month in args.a:
            month_average(CSV(args.file_path, year_month.split(
                '/')[0], year_month.split('/')[1]))
    if args.c:
        for year_month in args.c:
            weather_graph(
                CSV(args.file_path, year_month.split(
                    '/')[0], year_month.split('/')[1]))


def extreme_weather(csvfile):
    '''generate report for extreme weathers for a year'''

    max_temp = max(csvfile.record_list, key=lambda x: x.max_temp)
    min_temp = min(csvfile.record_list, key=lambda x: x.min_temp)
    max_humid = max(csvfile.record_list, key=lambda x: x.max_humidity)

    print('Highest: {:02d}C on {} {:02d}'.format(
        max_temp.max_temp, calendar.month_name[max_temp.date.month], max_temp.date.day))

    print('Lowest: {:02d}C on {} {:02d}'.format(
        min_temp.min_temp, calendar.month_name[min_temp.date.month], min_temp.date.day))

    print('Humidity: {:02d}% on {} {:02d}'.format(
        max_humid.max_humidity, calendar.month_name[max_humid.date.month],
        max_humid.date.day), end='\n\n')


def month_average(csvfile):
    '''generate monthly averages'''
    avg_high_temp = [n.max_temp for n in csvfile.record_list]
    avg_high_temp = [n for n in avg_high_temp if n != -273]
    print('Highest Average: {:02d}C'.format(
        sum(avg_high_temp) // len(avg_high_temp)))

    avg_low_temp = [n.min_temp for n in csvfile.record_list]
    avg_low_temp = [n for n in avg_low_temp if n != 273]
    print('Lowest Average: {:02d}C'.format(
        sum(avg_low_temp) // len(avg_low_temp)))

    avg_mean_humid = [n.mean_humidity for n in csvfile.record_list]
    avg_mean_humid = [n for n in avg_mean_humid if n != -1]
    print('Average Mean Humidity: {:02d}%'.format(
        sum(avg_mean_humid) // len(avg_mean_humid)), end='\n\n')


def weather_graph(csvfile):
    '''create monthly graphs'''
    print(calendar.month_name[csvfile.record_list[0].date.month],
          csvfile.record_list[0].date.year)
    for i in csvfile.record_list:
        if i.max_temp != -273:
            print('{:02d} '.format(i.date.day) + colored('+', 'red') * i.max_temp 
                  + ' {:02d}C\n{:02d} '.format(i.max_temp, i.date.day) +
                  colored('+', 'blue') * i.min_temp
                  + ' {:02d}C'.format(i.min_temp))
    print()
    print(calendar.month_name[csvfile.record_list[0].date.month],
          csvfile.record_list[0].date.year)
    for i in csvfile.record_list:
        if i.max_temp != -273:
            print('{:02d} '.format(i.date.day) + colored('+', 'blue') * i.min_temp
                  + colored('+', 'red') * i.max_temp
                  + ' {:02d}C - {:02d}C'.format(i.min_temp, i.max_temp))
    print()


def main():
    '''generate weather reports'''
    check_args()


if __name__ == '__main__':
    main()
