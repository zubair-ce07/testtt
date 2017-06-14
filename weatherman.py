#!~/Documents/myenv/bin/python3
'''generate weather reports from CSV files'''
import csv
import sys
import calendar
import os
from termcolor import colored
# from weather import CSV

__author__ = 'fakhar'

from record import Record


class CSV:
    '''creates a single CSV for all the required files'''
    # record_list = []

    def __init__(self, file_path, year, month):
        file_names = os.listdir(file_path)
        year_list = []
        self.record_list = []

        for file_name in file_names:
            if year in file_name:
                if month:
                    if month in file_name:
                        year_list.append(file_name)
                else:
                    year_list.append(file_name)
        # print(year_list)
        for file_name in year_list:
            with open(file_path + '/' + file_name) as csvfile:
                filereader = csv.DictReader(csvfile)
                for row in filereader:
                    new_record = Record(
                        row['PKT'], row['Max TemperatureC'],
                        row['Min TemperatureC'], row['Max Humidity'], row[' Mean Humidity'])
                    self.record_list.append(new_record)


def check_arg(args):
    '''check if arguments are in valid format'''
    if len(args) < 4:
        print('Minium Required arguments not provided\n'
              + 'usage: script-name.py path/to/files-dir flag date\n'
              + 'flag: -e for Yearly extreme Weather Report, -a for Average Monthly report'
              + 'or -c for Monthly Bar Graph'
              + 'date: Enter in either YYYY or YYYY/MM format')
        sys.exit()
    elif not os.path.exists(args[1]):
        print('The provided directory doesn\'t exist')
        sys.exit()
    else:
        file_path = args[1]
        for i in range(2, len(args), 2):
            if args[i] not in ['-a', '-c', '-e']:
                print('Please select a label from [-a, -c, -e]')
                sys.exit()
            else:
                if int(args[i + 1][:4]) not in range(2004, 2017):
                    print('Please enter correct year')
                    sys.exit()
                if args[i] == '-e':
                    if len(args[i + 1]) > 4 or len(args[i + 1]) < 2:
                        print('Please input year in the YYYY / YYY / YY format')
                        sys.exit()
                elif len(args[i + 1]) > 5:
                    if int(args[i + 1][5:]) not in range(1, 12):
                        print('Please enter a valid month')
                        sys.exit()
                else:
                    print('Please enter date in YYYY/MM format')
                    sys.exit()

            generate_report(args[i:i + 2], file_path)


def generate_report(args, file_path):
    '''Checks the kind of report to be generated'''
    year = args[1][0:4]

    if args[0] == '-e':
        extreme_weather(CSV(file_path, year, 0))

    elif args[0] == '-a' or '-c':
        if int(args[1][5]) == 0:
            month = int(args[1][6])
        else:
            month = int(args[1][5:])

        month = calendar.month_abbr[month]
        if args[0] == '-a':
            month_average(CSV(file_path, year, month))
        else:
            weather_graph(CSV(file_path, year, month))


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
    # print(len(csvfile.record_list))
    for i in csvfile.record_list:
        if i.max_temp != -273:
            print('{:02d} '.format(i.date.day) + colored('+', 'red') * i.max_temp
                  + '{:02d}C\n{:02d} '.format(i.max_temp, i.date.day) +
                  colored('+', 'blue') * i.min_temp
                  + '{:02d}C'.format(i.min_temp))
    print()
    print(calendar.month_name[csvfile.record_list[0].date.month],
          csvfile.record_list[0].date.year)
    for i in csvfile.record_list:
        if i.max_temp != -273:
            # print(end='')
            print('{:02d} '.format(i.date.day) + colored('+', 'blue') * i.min_temp
                  + colored('+', 'red') * i.max_temp
                  + '{:02d}C - {:02d}C'.format(i.min_temp, i.max_temp))
    print()


def main():
    '''generate weather reports'''
    check_arg(sys.argv)


if __name__ == '__main__':
    main()
