import argparse
import calendar
import copy
import csv
import datetime
import os
import re
from time import strptime

COLOR_RED = '\033[91m'
COLOR_BLUE = '\033[94m'
COLOR_PURPLE = '\033[35m'
COLOR_DEFAULT = '\033[0m'


def validate_path(dirname):
    if os.path.isdir(dirname):
        return dirname
    else:
        return None


def get_year_and_month(file_name):
    year = file_name[15:19]
    month = file_name[20:23]
    return year, str(strptime(month, '%b').tm_mon)


class FileParser:

    def __init__(self):
        self.year_data = {}
        self.month_data = {}

    def parse_file(self, dir_path):
        if validate_path(dir_path) is None:
            print('Sorry! The directory path is not valid')
            return None

        file_names = os.listdir(dir_path)

        for file_name in file_names:
            with open(os.path.join(dir_path, file_name), 'r') as file:
                year, month = get_year_and_month(file_name)
                file_data = csv.DictReader(file, skipinitialspace=True, delimiter=',')
                for index, row in enumerate(file_data):
                    self.month_data[str(index + 1)] = row

                if year not in self.year_data.keys():
                    self.year_data[year] = {}

                self.year_data[year][month] = copy.deepcopy(self.month_data)
                self.month_data.clear()


class ResultComputer:

    def compute_avg_results(self, month_data):
        sum_highest = sum_lowest = sum_humidity = 0
        highest_temp_count = lowest_temp_count = humidity_count = 0
        result = {}

        for day in month_data.values():
            if day['Max TemperatureC'] is not '':
                sum_highest += int(day['Max TemperatureC'])
                highest_temp_count += 1

            if day['Min TemperatureC'] is not '':
                sum_lowest += int(day['Min TemperatureC'])
                lowest_temp_count += 1

            if day['Max Humidity'] is not '':
                sum_humidity += int(day['Max Humidity'])
                humidity_count += 1

        result['Highest Average'] = sum_highest / highest_temp_count
        result['Lowest Average'] = sum_lowest / lowest_temp_count
        result['Average Humidity'] = sum_humidity / humidity_count

        return result

    def compute_extreme_results(self, year_data):
        min_temp_list = []
        max_temp_list = []
        max_humidity_list = []
        result = {}

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

        result['Highest Temp'] = highest_temp_and_date[0]
        result['Highest Temp Date'] = highest_temp_and_date[1]
        result['Lowest Temp'] = lowest_temp_and_date[0]
        result['Lowest Temp Date'] = lowest_temp_and_date[1]
        result['Highest Humidity'] = highest_humidity_and_date[0]
        result['Highest Humidity Date'] = highest_humidity_and_date[1]

        return result

    def compute_high_low_day_results(self, month_data):
        result_list = []

        for day in month_data.values():
            if day['Max TemperatureC'] is not '' and day['Min TemperatureC'] is not '':
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


def print_data_not_present_message():
    print('Sorry! data is not available of required year')


def print_invalid_input_message():
    print('Invalid input format')


def validate_year_and_month(year_and_month):
    match = re.search('^(20\d{2}|19\d{2}|0(?!0)\d|[1-9]\d)/(1[0-2]|0[1-9]|\d)', year_and_month)
    year_and_month = {}
    if match:
        year_and_month['year'] = match.group(1)
        year_and_month['month'] = match.group(2)
        return year_and_month
    else:
        return None


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('dir_path',
                        help='Directory path of weather files')
    parser.add_argument('-e', '--extreme-report',
                        help='Generates extreme weather report, taking year as input')
    parser.add_argument('-a', '--average-report',
                        help='Generates average weather report, taking year and month as input')
    parser.add_argument('-c', '--chart-report',
                        help='Generates two line reports, taking year and month as input')
    parser.add_argument('-b', '--bonus',
                        help='Generates single line reports, taking year and month as input')

    args = parser.parse_args()

    my_parser = FileParser()
    my_parser.parse_file(args.dir_path)

    my_computer = ResultComputer()

    my_result_generator = ResultGenerator()

    if args.extreme_report:
        if args.extreme_report in my_parser.year_data.keys():
            year_data = my_parser.year_data[args.extreme_report]
            year_result = my_computer.compute_extreme_results(year_data)
            my_result_generator.generate_extreme_results(year_result)
        else:
            print_data_not_present_message()

    if args.average_report:
        year_and_month = validate_year_and_month(args.average_report)
        if year_and_month:
            year = year_and_month['year']
            month = year_and_month['month']
        else:
            print_invalid_input_message()

        if year in my_parser.year_data.keys():
            if month in my_parser.year_data[year].keys():
                month_data = my_parser.year_data[year][month]
                month_result = my_computer.compute_avg_results(month_data)
                my_result_generator.generate_average_results(month_result)
            else:
                print_data_not_present_message()
        else:
            print_data_not_present_message()

    if args.chart_report:
        year_and_month = validate_year_and_month(args.chart_report)
        if year_and_month:
            year = year_and_month['year']
            month = year_and_month['month']
        else:
            print_invalid_input_message()

        if year in my_parser.year_data.keys():
            if month in my_parser.year_data[year].keys():
                month_data = my_parser.year_data[year][month]
                month_result = my_computer.compute_high_low_day_results(month_data)
                my_result_generator.generate_high_low_day_double_results(month_result)
            else:
                print_data_not_present_message()
        else:
            print_data_not_present_message()

    if args.bonus:
        year_and_month = validate_year_and_month(args.bonus)
        if year_and_month:
            year = year_and_month['year']
            month = year_and_month['month']
        else:
            print_invalid_input_message()

        if year in my_parser.year_data.keys():
            if month in my_parser.year_data[year].keys():
                month_data = my_parser.year_data[year][month]
                month_result = my_computer.compute_high_low_day_results(month_data)
                my_result_generator.generate_high_low_day_single_results(month_result)
            else:
                print_data_not_present_message()
        else:
            print_data_not_present_message()


if __name__ == '__main__':
    main()
