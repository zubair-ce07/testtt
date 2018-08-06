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

    def __init__(self, dir_path, required_year_arg, required_years_and_months):
        self.year_data = {}
        self.required_files = []
        self.dir_path = dir_path

        if required_year_arg:
            files_required = os.path.join(dir_path, 'Murree_weather_' + required_year_arg + '_???.txt')
            files_required = glob.glob(files_required)
            files_required = [os.path.basename(file) for file in files_required]
            self.required_files.extend(files_required)

        for required_year_and_month in required_years_and_months:
            if not required_year_and_month:
                continue

            required_year_and_month = required_year_and_month.split('/')
            required_year = required_year_and_month[0]
            required_month = calendar.month_name[int(required_year_and_month[1])]

            files_required = os.path.join(dir_path, 'Murree_weather_' + required_year + '_' +
                                          required_month[:3] + '.txt')

            files_required = glob.glob(files_required)
            files_required = [os.path.basename(file) for file in files_required]
            if files_required:
                self.required_files.extend(files_required)

    def parse_file_row(self, file_data):
        for row in file_data:
            yield {
                'Max TemperatureC': 0 if row['Max TemperatureC'] == '' else row['Max TemperatureC'],
                'Min TemperatureC': 0 if row['Min TemperatureC'] == '' else row['Min TemperatureC'],
                'Max Humidity': 0 if row['Max Humidity'] == '' else row['Max Humidity'],
                'PKT': row['PKT']
            }

    def parse_file_data(self):
        month_data = {}
        for file_name in self.required_files:
            with open(os.path.join(self.dir_path, file_name), 'r') as file:
                year, month = get_year_and_month(file_name)
                file_data = csv.DictReader(file, skipinitialspace=True, delimiter=',')

                for index, parsed_row in enumerate(self.parse_file_row(file_data)):
                    index_string = str(index + 1)
                    month_data[index_string] = parsed_row

                if year not in self.year_data.keys():
                    self.year_data[year] = {}

                self.year_data[year][month] = copy.deepcopy(month_data)
                month_data.clear()


class ResultComputer:

    def compute_average_results(self, month_data):
        sum_highest = sum(int(day['Max TemperatureC']) for day in month_data.values())
        sum_lowest = sum(int(day['Min TemperatureC']) for day in month_data.values())
        sum_humidity = sum(int(day['Max Humidity']) for day in month_data.values())
        count = len(month_data)
        return {
            'Highest Average': sum_highest / count,
            'Lowest Average': sum_lowest / count,
            'Average Humidity': sum_humidity / count
        }

    def compute_extreme_results(self, year_data):
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

    def compute_high_low_day_results(self, month_data):
        result_list = []
        for day in month_data.values():
            result_list.append((int(day['Max TemperatureC']), int(day['Min TemperatureC'])))

        return result_list


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

    def generate_high_low_day_double_results(self, data):
        for index, record in enumerate(data):
            print('{:0>2d} {} {}C\n{:0>2d} {} {}C'.format(index + 1, COLOR_RED + '+' * record[0],
                                                          COLOR_PURPLE + str(record[0]), index + 1,
                                                          COLOR_BLUE + '+' * record[1], COLOR_PURPLE + str(record[1])))

        print(COLOR_DEFAULT)

    def generate_high_low_day_single_results(self, data):
        for index, record in enumerate(data):
            print('{:0>2d} {}{} {}C - {}C'.format(index + 1, COLOR_BLUE + '+' * record[1],
                                                  COLOR_RED + '+' * record[0],
                                                  COLOR_PURPLE + str(record[1]), str(record[0])))

        print(COLOR_DEFAULT)


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

    file_parser = FileParser(args.dir_path, args.extreme_report,
                             [args.average_report, args.chart_report, args.bonus])

    result_computer = ResultComputer()
    result_generator = ResultGenerator()

    file_parser.parse_file_data()

    if args.extreme_report:
        if file_parser.year_data.get(args.extreme_report):
            year_data = file_parser.year_data[args.extreme_report]
            year_result = result_computer.compute_extreme_results(year_data)
            result_generator.generate_extreme_results(year_result)
        else:
            print('Sorry! data is not available of required year')

    if args.average_report:
        year_and_month = args.average_report.split('/')

        year = year_and_month[0]
        month = year_and_month[1]

        if file_parser.year_data.get(year, {}).get(month):
            month_data = file_parser.year_data[year][month]
            month_result = result_computer.compute_average_results(month_data)
            result_generator.generate_average_results(month_result)
        else:
            print('Sorry! data is not available of required year and month')

    if args.chart_report:
        year_and_month = args.chart_report.split('/')

        year = year_and_month[0]
        month = year_and_month[1]

        if file_parser.year_data.get(year, {}).get(month):
            month_data = file_parser.year_data[year][month]
            month_result = result_computer.compute_high_low_day_results(month_data)
            result_generator.generate_high_low_day_double_results(month_result)
        else:
            print('Sorry! data is not available of required year and month')

    if args.bonus:
        year_and_month = args.bonus.split('/')

        year = year_and_month[0]
        month = year_and_month[1]

        if file_parser.year_data.get(year, {}).get(month):
            month_data = file_parser.year_data[year][month]
            month_result = result_computer.compute_high_low_day_results(month_data)
            result_generator.generate_high_low_day_single_results(month_result)
        else:
            print('Sorry! data is not available of required year and month')


if __name__ == '__main__':
    main()
