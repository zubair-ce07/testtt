#!~/Documents/myenv/bin/python3
'''generate weather reports from CSV files'''
import csv
import sys
import datetime
import calendar
import os
from termcolor import colored
#from weather import CSV

__author__ = 'fakhar'

from record import Record


class CSV:
    '''creates a single CSV for all the required files'''
    #record_list = []

    def __init__(self, file_path, year, month):
        file_names = os.listdir(file_path)
        year_list = []
        self.record_list = []

        for file in file_names:
            if year in file:
                if month != 0:
                    if month in file:
                        year_list.append(file)
                else:
                    year_list.append(file)
        # print(year_list)
        for file in year_list:
            with open(file_path + '/' + file) as csvfile:
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

    print('Highest: ' + str(max_temp.max_temp).zfill(2) +
          'C on ' + calendar.month_name[max_temp.date.month]
          + ' ' + str(max_temp.date.day).zfill(2))

    print('Lowest: ' + str(min_temp.min_temp).zfill(2) +
          'C on ' + calendar.month_name[min_temp.date.month]
          + ' ' + str(min_temp.date.day).zfill(2))

    print('Humidity: ' + str(max_humid.max_humidity).zfill(2) +
          '% on ' + calendar.month_name[max_humid.date.month]
          + ' ' + str(max_humid.date.day).zfill(2))
    print()


def month_average(csvfile):
    '''generate monthly averages'''

    avg_high_temp = [n.max_temp for n in csvfile.record_list]
    avg_high_temp = [n for n in avg_high_temp if n != -273]

    print('Highest Average: ' + str(sum(avg_high_temp) // len(avg_high_temp)) + 'C')

    avg_low_temp = [n.min_temp for n in csvfile.record_list]
    avg_low_temp = [n for n in avg_low_temp if n != 273]
    print('Lowest Average: ' + str(sum(avg_low_temp) // len(avg_low_temp)) + 'C')

    avg_mean_humid = [n.mean_humidity for n in csvfile.record_list]
    avg_mean_humid = [n for n in avg_mean_humid if n != -1]
    print('Average Mean Humidity: ' + str(sum(avg_mean_humid) // len(avg_mean_humid)) + '%')
    print()


def weather_graph(csvfile):
    '''create monthly graphs'''
    print(calendar.month_name[csvfile.record_list[0].date.month], csvfile.record_list[0].date.year)
    #print(len(csvfile.record_list))
    for i in csvfile.record_list:
        if i.max_temp != -273:
            #print(end='')
            print(str(i.date.day).zfill(2), end=' ')
            print(colored('+', 'red') * i.max_temp + str(i.max_temp) + 'C')
            print(str(i.date.day).zfill(2), end=' ')
            print(colored('+', 'blue') * i.min_temp + str(i.min_temp) + 'C')
    print()
    print(calendar.month_name[csvfile.record_list[0].date.month], csvfile.record_list[0].date.year)
    for i in csvfile.record_list:
        if i.max_temp != -273:
            print(end='')
            print(str(i.date.day).zfill(2), end=' ')
            print(colored('+', 'blue') * i.min_temp + colored('+', 'red')
                  * i.max_temp + ' ' + str(i.min_temp) + 'C - ' + str(i.max_temp) + 'C')
    print()


def main():
    '''generate weather reports'''
    check_arg(sys.argv)


if __name__ == '__main__':
    main()
