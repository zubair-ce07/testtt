"""
File for all helper functions of weatherman
Pylint Score: 10.00
"""

import os
import csv
import calendar
from colored import fg, attr
from weather import Weather


def get_files(args):
    """Function to find the required files"""
    files = []
    if args.year:
        for file in os.listdir(args.directory):
            if file.find(args.year) != -1:
                files.append(file)
    else:
        month_no = None
        year = None
        if args.year_month and args.year_month.find('/') == 4:
            year, month_no = args.year_month.split('/')
        elif args.year_month_graph and args.year_month_graph.find('/') == 4:
            year, month_no = args.year_month_graph.split('/')
        if 0 < int(month_no) <= 12:
            month = calendar.month_name[int(month_no)]
            mon = '{:.3}'.format(month)
            for file in os.listdir(args.directory):
                if file.find('{}_{}'.format(year, mon)) != -1:
                    files.append(file)
    return files


def read_data(directory, files):
    """Method to read the required data from files"""
    weather_rows = []

    for file in files:
        path = '{}/{}'.format(directory, file)

        with open(path, 'r') as read_file:
            reader = csv.DictReader(read_file)
            if not reader.fieldnames:
                reader = csv.DictReader(read_file)

            for i, header in enumerate(reader.fieldnames):
                if header.find('PKT') != -1 or header.find('PKST') != -1:
                    reader.fieldnames[i] = 'PKT'
                if header.find('Max TemperatureC') != -1:
                    reader.fieldnames[i] = 'Max TemperatureC'
                if header.find('Min TemperatureC') != -1:
                    reader.fieldnames[i] = 'Min TemperatureC'
                if header.find('Mean Humidity') != -1:
                    reader.fieldnames[i] = 'Mean Humidity'
                if header.find('Max Humidity') != -1:
                    reader.fieldnames[i] = 'Max Humidity'

            for row in reader:
                weather = Weather()
                if row['Max TemperatureC']:
                    weather.get_row(row)
                    weather_rows.append(weather)

    return weather_rows


def peak_days(weather_rows):
    """Function to find the peak days of year"""
    max_temp = float('-inf')
    min_temp = float('inf')
    max_humid = float('-inf')
    max_temp_dates = []
    min_temp_dates = []
    max_humid_dates = []

    for row in weather_rows:
        if row.max_temp >= max_temp:
            if row.max_temp > max_temp:
                max_temp_dates.clear()      # Clear the previous dates, if new max value occurs
            max_temp = row.max_temp
            max_temp_dates.append('{} {}'.format(row.month, row.day))
        if row.min_temp <= min_temp:
            if row.min_temp < min_temp:
                min_temp_dates.clear()
            min_temp = row.min_temp
            min_temp_dates.append('{} {}'.format(row.month, row.day))
        if row.max_humid >= max_humid:
            if row.max_humid > max_humid:
                max_humid_dates.clear()
            max_humid = row.max_humid
            max_humid_dates.append('{} {}'.format(row.month, row.day))

    return max_temp, min_temp, max_humid, max_temp_dates, min_temp_dates, max_humid_dates


def show_peak_days(year, weather_rows):
    """Function to display peak days of year"""
    max_temp, min_temp, max_humid, max_temp_dates, min_temp_dates, max_humid_dates = \
        peak_days(weather_rows)

    print('Year {}'.format(year))
    print('Highest: {}C on {}'.format(max_temp, ', '.join(date for date in max_temp_dates)))
    print('Lowest: {}C on {}'.format(min_temp, ', '.join(date for date in min_temp_dates)))
    print('Humid: {}% on {}'.format(max_humid, ', '.join(date for date in max_humid_dates)))


def calculate_averages(weather_rows):
    """Function to calculate averages"""
    sum_max_temp = 0
    sum_min_temp = 0
    sum_mean_humid = 0

    for row in weather_rows:
        sum_max_temp += row.max_temp
        sum_min_temp += row.min_temp
        sum_mean_humid += row.mean_humid

    avg_max_temp = round(sum_max_temp / len(weather_rows))
    avg_min_temp = round(sum_min_temp / len(weather_rows))
    avg_mean_humid = round(sum_mean_humid / len(weather_rows))

    return avg_max_temp, avg_min_temp, avg_mean_humid


def show_averages(year_month, weather_rows):
    """Function to display averages of month"""
    avg_max_temp, avg_min_temp, avg_mean_humid = calculate_averages(weather_rows)

    year, month_no = year_month.split('/')
    month = calendar.month_name[int(month_no)]

    print(month, year)
    print('Highest Average: {}C'.format(avg_max_temp))
    print('Lowest Average: {}C'.format(avg_min_temp))
    print('Average Humidity: {}%'.format(avg_mean_humid))


def make_graph(year_month, weather_rows):
    """Function to display daily weather graph"""
    year, month_no = year_month.split('/')
    month = calendar.month_name[int(month_no)]
    print(month, year)

    for row in weather_rows:
        day = row.day
        min_temp = row.min_temp
        max_temp = row.max_temp
        min_temp_bar = '{}{}{}'.format(fg('light_blue'), '+' * int(min_temp), attr('reset'))
        max_temp_bar = '{}{}{}'.format(fg('red'), '+' * int(max_temp), attr('reset'))

        print('{} {}{} {}C - {}C'.format(day, min_temp_bar, max_temp_bar, min_temp, max_temp))
