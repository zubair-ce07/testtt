#!~/Documents/myenv/bin/python3
'''generate weather reports from CSV files'''
import csv
import sys
from datetime import datetime
import calendar
import os
from termcolor import colored

__author__ = 'fakhar'


def check_args(args):
    '''Checks the kind of report to be generated'''

    file_path = args[1]

    for i in range(2, len(args), 2):
        year = args[i + 1][0:4]

        if args[i] == '-e':
            extreme_weather(file_path, year)
        elif args[i] == '-a' or '-c':
            if int(args[i + 1][5]) == 0:
                month = int(args[i + 1][6])
            else:
                month = int(args[i + 1][5:])

            month = calendar.month_abbr[month]
            prereq(month, year, file_path, args[i])


def extreme_weather(file_path, year):
    '''generate report for extreme weathers for a year'''
    file_names = os.listdir(file_path)
    year_list, max_temperature, min_temperature, max_humidity = [], [], [], []

    for file in file_names:
        if year in file:
            year_list.append(file)

    for file in year_list:
        with open(file_path + '/' + file) as csvfile:
            filereader = csv.DictReader(csvfile)
            for row in filereader:
                if row['Max TemperatureC'] != '':
                    max_temperature.append(
                        (int(row['Max TemperatureC']), row['PKT']))
                if row['Min TemperatureC'] != '':
                    min_temperature.append(
                        (int(row['Min TemperatureC']), row['PKT']))
                if row['Max Humidity'] != '':
                    max_humidity.append(
                        (int(row['Max Humidity']), row['PKT']))

    max_temperature, min_temperature, max_humidity = max(
        max_temperature), min(min_temperature), max(max_humidity)
    max_temp_date = datetime.strptime(max_temperature[1], '%Y-%m-%d')
    min_temp_date = datetime.strptime(min_temperature[1], '%Y-%m-%d')
    max_humid_date = datetime.strptime(max_humidity[1], '%Y-%m-%d')

    print('Highest: ' + str(max_temperature[0]).zfill(2) + 'C on ' +
          calendar.month_name[max_temp_date.month] + ' ' + str(max_temp_date.day).zfill(2))
    print('Lowest: ' + str(min_temperature[0]).zfill(2) + 'C on ' +
          calendar.month_name[min_temp_date.month] + ' ' + str(min_temp_date.day).zfill(2))
    print('Humidity: ' + str(max_humidity[0]).zfill(2) + '% on ' +
          calendar.month_name[max_humid_date.month] + ' ' + str(min_temp_date.day).zfill(2))
    print()


def prereq(month, year, path, arg):
    '''prerequisites for -a and -c'''
    file_name = os.listdir(path)
    for file in file_name:
        if year in file:
            if month in file:
                req_file = file

    high_temp_list, low_temp_list, mean_humid_list = [], [], []

    with open(path + '/' + req_file) as csvfile:
        filereader = csv.DictReader(csvfile)
        for row in filereader:
            if row['Max TemperatureC'] != '':
                high_temp_list.append(int(row['Max TemperatureC']))
            else:
                high_temp_list.append('-')
            if row['Min TemperatureC'] != '':
                low_temp_list.append(int(row['Min TemperatureC']))
            else:
                low_temp_list.append('-')
            if row[' Mean Humidity'] != '':
                mean_humid_list.append(int(row[' Mean Humidity']))
            else:
                mean_humid_list.append('-')

        if arg == '-a':
            average_weather(high_temp_list, low_temp_list, mean_humid_list)
        else:
            print(month, year)
            weather_graph(high_temp_list, low_temp_list)


def average_weather(high_temp_list, low_temp_list, mean_humid_list):
    '''generates report for average weather for a month'''
    avg_high, avg_low, avg_hum = 0, 0, 0

    for i in high_temp_list:
        if i != '-':
            avg_high += i
    avg_high = avg_high // len(
        [n for n in high_temp_list if str(n).isdigit()])

    for i in low_temp_list:
        if i != '-':
            avg_low += i
    avg_low = avg_low // len(
        [n for n in low_temp_list if str(n).isdigit()])

    for i in mean_humid_list:
        if i != '-':
            avg_hum += i
    avg_hum = avg_hum // len(
        [n for n in mean_humid_list if str(n).isdigit()])

    print('Highest Average: ' + str(avg_high) + 'C')
    print('Lowest Average: ' + str(avg_low) + 'C')
    print('Average Mean Humidity: ' + str(avg_hum) + '%')
    print()


def weather_graph(high_temp_list, low_temp_list):
    '''generates a bar graph for daily high/low temps of a month'''
    text = ''
    for day in range(0, len(high_temp_list)):
        if high_temp_list[day] == '-':
            continue
        print(str(day + 1).zfill(2), end=' ')
        for _ in range(0, high_temp_list[day]):
            text += colored('+', 'red')
        print(text + ' ' + str(high_temp_list[day]) + 'C')
        text = ''
        print(str(day + 1).zfill(2), end=' ')
        for _ in range(0, low_temp_list[day]):
            text += colored('+', 'blue')
        print(text + ' ' + str(low_temp_list[day]) + 'C')
        text = ''
    print()
    #print(month, year)
    for day in range(0, len(high_temp_list)):
        if high_temp_list[day] == '-':
            continue
        print(str(day + 1).zfill(2), end=' ')
        for _ in range(0, low_temp_list[day]):
            text += colored('+', 'blue')
        #print(text, end='')
        #text = ''

        for _ in range(0, high_temp_list[day]):
            text += colored('+', 'red')
        print(text + ' ' + str(low_temp_list[day]) +
              'C - ' + str(high_temp_list[day]) + 'C')
        text = ''
    print()


def main():
    '''generate weather reports'''
    check_args(sys.argv)


if __name__ == "__main__":
    main()
