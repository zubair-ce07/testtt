import argparse
import fnmatch
import os
import csv
from datetime import datetime
import calendar


def year_files(path, year):
    file_names = []
    for file in os.listdir(path):
        if fnmatch.fnmatch(file, f'*_{year}_*'):
            file_names.append(path + '/' + file)
    return file_names


def month_files(path, year, month):
    files_names = []
    for file in os.listdir(path):
        if fnmatch.fnmatch(file, f'*_{year}_{month}.txt'):
            full_path = path + '/' + file
            files_names.append(full_path)
    return files_names


def read_files(files):
    max_temperature = []
    min_temperature = []
    max_humidity = []
    mean_humidity = []
    max_temp_date = []
    min_temp_date = []
    max_humidity_date = []
    data = {}
    try:
        for file in list(files):
            with open(file) as data_file:
                for row in csv.DictReader(data_file):
                    if row['Max TemperatureC'] != '':
                        max_temperature.append(int(row['Max TemperatureC']))
                        max_temp_date.append(row['PKT'])
                    if row['Min TemperatureC'] != '':
                        min_temperature.append(int(row['Min TemperatureC']))
                        min_temp_date.append(row['PKT'])
                    if row['Max Humidity'] != '':
                        max_humidity.append(int(row['Max Humidity']))
                        max_humidity_date.append(row['PKT'])
                    if row[' Mean Humidity'] != '':
                        mean_humidity.append(int(row[' Mean Humidity']))
        data['max_temperature'] = max_temperature
        data['min_temperature'] = min_temperature
        data['max_humidity'] = max_humidity
        data['mean_humidity'] = mean_humidity
        data['max_temp_date'] = max_temp_date
        data['min_temp_date'] = min_temp_date
        data['max_humidity_date'] = max_humidity_date
        return data
    except FileNotFoundError as fnfError:
        print(fnfError)


def extreme_values(data):
    extremes = {
        'max_temperature': max(data['max_temperature']),
        'max_temp_date': data['max_temp_date'][data['max_temperature'].index(
            max(data['max_temperature']))],
        'min_temp_date': data['min_temp_date'][data['min_temperature'].index(
            min(data['min_temperature']))],
        'max_humidity_date': data['max_humidity_date'][data['max_humidity'].index(
            max(data['max_humidity']))],
        'min_temperature': min(data['min_temperature']),
        'max_humidity': max(data['max_humidity'])
    }

    return extremes


def average_values(data):
    averages = {
        'avg_max_temperature': round(
            sum(data['max_temperature']) / len(data['max_temperature'])),
        'avg_min_temperature': round(
            sum(data['min_temperature']) / len(data['min_temperature'])),
        'avg_mean_humidity': round(
            sum(data['mean_humidity']) / len(data['mean_humidity']))
    }

    return averages


def display_chart(data):
    for (max_temp, min_temp, max_day, min_day) in zip(data['max_temperature'],
                                                      data['min_temperature'],
                                                      data['max_temp_date'],
                                                      data['min_temp_date']):
        max_day = max_day.split('-')[2]
        print(max_day + ' ', end='')
        for value in range(max_temp):
            print("\033[1;31m+\033[1;m", end='')
        print(f' {max_temp}C')

        min_day = min_day.split('-')[2]
        print(min_day + ' ', end='')
        for value in range(min_temp):
            print("\033[1;34m+\033[1;m", end='')
        print(f' {min_temp}C')


def bonus_chart(data):
    for (max_temp, min_temp, max_day) in zip(data['max_temperature'],
                                             data['min_temperature'],
                                             data['max_temp_date']):
        max_day = max_day.split('-')[2]
        print(max_day + ' ', end='')
        for i in range(min_temp):
            print("\033[1;34m+\033[1;m", end='')
        for j in range(max_temp):
            print("\033[1;31m+\033[1;m", end='')
        print(f' {min_temp}C-{max_temp}C')


def display_extrems(extremes):
    max_temp_day = datetime.strptime(extremes['max_temp_date'],
                                     '%Y-%m-%d').strftime('%B %d')
    min_temp_day = datetime.strptime(extremes['min_temp_date'],
                                     '%Y-%m-%d').strftime('%B %d')
    max_humid_day = datetime.strptime(extremes['max_humidity_date'],
                                      '%Y-%m-%d').strftime('%B %d')
    print(f'Highest: {extremes["max_temperature"]}C on {max_temp_day}')
    print(f'Lowest: {extremes["min_temperature"]}C on {min_temp_day}')
    print(f'Humidity: {extremes["max_humidity"]}% on {max_humid_day}')


def display_averages(avg_values):
    print(f'Highest Average: {avg_values["avg_max_temperature"]}C')
    print(f'Lowest Average: {avg_values["avg_min_temperature"]}C')
    print(f'Average Mean Humidity: {avg_values["avg_mean_humidity"]}%')


def main():
    parser = argparse.ArgumentParser(description='Weatherman app')
    parser.add_argument('path', help='Directory path to the data files')
    parser.add_argument('-e',
                        help='For a given year it displays the highest '
                             'temperature and day, '
                             ' lowest temperature '
                             'and day, most humid day and humidity')
    parser.add_argument('-a',
                        help='For a given month it displays the average '
                             'highest temperature, average lowest '
                             'temperature, average mean humidity.')
    parser.add_argument('-c',
                        help='For a given month it draws horizontal bar '
                             'charts for the highest and lowest temperature '
                             'on each day.')
    parser.add_argument('-b', help='Bonus Task')
    args = parser.parse_args()

    if args.e:
        file_names_e = year_files(args.path, args.e)
        if file_names_e:
            data = read_files(file_names_e)
            extremes = extreme_values(data)
            display_extrems(extremes)
        else:
            print('No file found for given year')

    elif args.a:
        date = args.a.split('/')
        year, month = date[0], date[1]
        file_names_a = month_files(args.path, year,
                                   calendar.month_abbr[int(month)])
        if file_names_a:
            data = read_files(file_names_a)
            avg_values = average_values(data)
            display_averages(avg_values)
        else:
            print('No file found for given year and month')

    elif args.c:
        date = args.c.split('/')
        year, month = date[0], date[1]
        file_names_c = month_files(args.path, year,
                                   calendar.month_abbr[int(month)])
        if file_names_c:
            data = read_files(file_names_c)
            display_chart(data)
        else:
            print('No file found for given year and month')
    elif args.b:
        date = args.b.split('/')
        year, month = date[0], date[1]
        file_names_b = month_files(args.path, year,
                                   calendar.month_abbr[int(month)])
        if file_names_b:
            data = read_files(file_names_b)
            bonus_chart(data)
        else:
            print('No file found for given year and month')


if __name__ == '__main__':
    main()
