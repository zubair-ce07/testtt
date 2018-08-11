import argparse
import calendar
import copy
import csv
import datetime
import glob
import os
import re
from time import strptime

COLOR_RED = '\033[91m'
COLOR_BLUE = '\033[94m'
COLOR_PURPLE = '\033[35m'
COLOR_DEFAULT = '\033[0m'


def is_valid_directory(dir_name):
    if os.path.isdir(dir_name):
        return dir_name


def is_valid_year_and_month(year_and_month):
    match = re.search('^(20\d{2}|19\d{2}|0(?!0)\d|[1-9]\d)/(1[0-2]|0[1-9]|\d)', year_and_month)
    if match:
        return year_and_month


def get_year_and_month(file_name):
    year = file_name[15:19]
    month = file_name[20:23]
    return year, str(strptime(month, '%b').tm_mon)


class FileParser:

    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.year_data = {}
        self.required_files = []

    def populate_file_list(self, required_year, required_month=None):
        if self.year_data.get(required_year, {}).get(required_month):
            return

        if required_year:
            if required_month:
                required_month = calendar.month_name[int(required_month)]
                files_required = os.path.join(self.dir_path, '*' + required_year + '_' + required_month[:3] + '.txt')
            else:
                files_required = os.path.join(self.dir_path, '*' + required_year + '_???.txt')

            files_required = glob.glob(files_required)
            self.required_files.extend([os.path.basename(file) for file in files_required])

    def parse_month_data(self, file_data):
        month_data = {}
        index = 1
        for row in file_data:
            month_data[str(index)] = {
                'Max TemperatureC': 0 if row['Max TemperatureC'] == '' else row['Max TemperatureC'],
                'Min TemperatureC': 0 if row['Min TemperatureC'] == '' else row['Min TemperatureC'],
                'Max Humidity': 0 if row['Max Humidity'] == '' else row['Max Humidity'],
                'PKT': row['PKT']
            }
            index += 1
        return month_data

    def parse_files(self):
        for file_name in self.required_files:
            with open(os.path.join(self.dir_path, file_name), 'r') as file:
                year, month = get_year_and_month(file_name)
                file_data = csv.DictReader(file, skipinitialspace=True, delimiter=',')
                month_data = self.parse_month_data(file_data)

                if not self.year_data.get(year):
                    self.year_data[year] = {}

            self.year_data[year][month] = copy.deepcopy(month_data)


class ResultCalculator:

    def calculate_average_results(self, month_data):
        sum_highest = sum(int(day['Max TemperatureC']) for day in month_data.values())
        sum_lowest = sum(int(day['Min TemperatureC']) for day in month_data.values())
        sum_humidity = sum(int(day['Max Humidity']) for day in month_data.values())
        count = len(month_data)
        return {
            'Highest Average': sum_highest / count,
            'Lowest Average': sum_lowest / count,
            'Average Humidity': sum_humidity / count
        }

    def calculate_extreme_results(self, year_data):
        min_temp_list = []
        max_temp_list = []
        max_humidity_list = []

        for month in year_data.values():
            value = max(month.items(), key=lambda x: int(x[1]['Max TemperatureC']))
            max_temp_list.append((value[1]['Max TemperatureC'], value[1]['PKT']))
            value = min(month.items(), key=lambda x: int(x[1]['Min TemperatureC']))
            min_temp_list.append((value[1]['Min TemperatureC'], value[1]['PKT']))
            value = max(month.items(), key=lambda x: int(x[1]['Max Humidity']))
            max_humidity_list.append((value[1]['Max Humidity'], value[1]['PKT']))

        highest_temp_and_date = max(max_temp_list, key=lambda x: x[0])
        lowest_temp_and_date = min(min_temp_list, key=lambda x: x[0])
        highest_humidity_and_date = max(max_humidity_list, key=lambda x: x[0])

        return {
            'Highest Temp': highest_temp_and_date[0],
            'Highest Temp Date': highest_temp_and_date[1],
            'Lowest Temp': lowest_temp_and_date[0],
            'Lowest Temp Date': lowest_temp_and_date[1],
            'Highest Humidity': highest_humidity_and_date[0],
            'Highest Humidity Date': highest_humidity_and_date[1]
        }


class ResultGenerator:

    def generate_extreme_results(self, data):
        date = datetime.datetime.strptime(data['Highest Temp Date'], '%Y-%m-%d')
        print('Highest: {}C on {} {}'.format(data['Highest Temp'],
                                             calendar.month_name[date.month], date.day))
        date = datetime.datetime.strptime(data['Lowest Temp Date'], '%Y-%m-%d')
        print('Lowest: {}C on {} {}'.format(data['Lowest Temp'],
                                            calendar.month_name[date.month], date.day))
        date = datetime.datetime.strptime(data['Highest Humidity Date'], '%Y-%m-%d')
        print('Humidity: {}% on {} {}\n'.format(data['Highest Humidity'],
                                                calendar.month_name[date.month], date.day))

    def generate_average_results(self, data):
        print('Highest Average: {}'.format(round(data['Highest Average'], 2)))
        print('Lowest Average: {}'.format(round(data['Lowest Average'], 2)))
        print('Average Mean Humidity: {}\n'.format(round(data['Average Humidity'], 2)))

    def generate_high_low_day_double_results(self, month_data):
        for index, day in enumerate(month_data.values()):
            print('{:0>2d} {} {}C\n{:0>2d} {} {}C'.format(index + 1, COLOR_RED + '+' * int(day['Max TemperatureC']),
                                                          COLOR_PURPLE + day['Max TemperatureC'], index + 1,
                                                          COLOR_BLUE + '+' * int(day['Min TemperatureC']),
                                                          COLOR_PURPLE + day['Min TemperatureC']))

        print(COLOR_DEFAULT)

    def generate_high_low_day_single_results(self, month_data):
        for index, day in enumerate(month_data.values()):
            print('{:0>2d} {}{} {}C - {}C'.format(index + 1, COLOR_BLUE + '+' * int(day['Min TemperatureC']),
                                                  COLOR_RED + '+' * int(day['Max TemperatureC']),
                                                  COLOR_PURPLE + day['Min TemperatureC'],
                                                  day['Max TemperatureC']))

        print(COLOR_DEFAULT)


def split_year_and_month(year_and_month):
    year_and_month = year_and_month.split('/')
    year = year_and_month[0]
    month = year_and_month[1]
    return year, month


def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('dir_path',
                                 type=is_valid_directory,
                                 help='Directory path of weather files')
    argument_parser.add_argument('-e', '--extreme-report',
                                 help='Generates extreme weather report, taking year as input')
    argument_parser.add_argument('-a', '--average-report',
                                 type=is_valid_year_and_month,
                                 help='Generates average weather report, taking year and month as input')
    argument_parser.add_argument('-c', '--chart-report',
                                 type=is_valid_year_and_month,
                                 help='Generates two line reports, taking year and month as input')
    argument_parser.add_argument('-b', '--bonus',
                                 type=is_valid_year_and_month,
                                 help='Generates single line reports, taking year and month as input')

    args = argument_parser.parse_args()

    if not args.dir_path:
        print('Invalid directory path')
        return

    file_parser = FileParser(args.dir_path)
    result_calculator = ResultCalculator()
    result_generator = ResultGenerator()

    if args.extreme_report:
        file_parser.populate_file_list(args.extreme_report)

    if args.average_report:
        year, month = split_year_and_month(args.average_report)
        file_parser.populate_file_list(year, month)

    if args.chart_report:
        year, month = split_year_and_month(args.chart_report)
        file_parser.populate_file_list(year, month)

    if args.bonus:
        year, month = split_year_and_month(args.bonus)
        file_parser.populate_file_list(year, month)

    file_parser.parse_files()

    if args.extreme_report:
        if file_parser.year_data.get(args.extreme_report):
            year_data = file_parser.year_data[args.extreme_report]
            year_result = result_calculator.calculate_extreme_results(year_data)
            result_generator.generate_extreme_results(year_result)
        else:
            print('Sorry! data is not available of required year')

    if args.average_report:
        year, month = split_year_and_month(args.average_report)

        if file_parser.year_data.get(year, {}).get(month):
            month_data = file_parser.year_data[year][month]
            month_result = result_calculator.calculate_average_results(month_data)
            result_generator.generate_average_results(month_result)
        else:
            print('Sorry! data is not available of required year and month')

    if args.chart_report:
        year, month = split_year_and_month(args.chart_report)

        if file_parser.year_data.get(year, {}).get(month):
            month_data = file_parser.year_data[year][month]
            result_generator.generate_high_low_day_double_results(month_data)
        else:
            print('Sorry! data is not available of required year and month')

    if args.bonus:
        year, month = split_year_and_month(args.bonus)

        if file_parser.year_data.get(year, {}).get(month):
            month_data = file_parser.year_data[year][month]
            result_generator.generate_high_low_day_single_results(month_data)
        else:
            print('Sorry! data is not available of required year and month')


if __name__ == '__main__':
    main()
