import os
import argparse
import datetime
import calendar
import copy
import sys
import csv
from time import strptime
from collections import defaultdict

EMPTY = ''
COLOR_RED = '\033[91m'
COLOR_BLUE = '\033[94m'
COLOR_PURPLE = '\033[35m'
COLOR_DEFAULT = '\033[0m'


class FileParser:

    def __init__(self):
        self.year_data = defaultdict(dict)
        self.month_data = {}

    @staticmethod
    def is_dir(dirname):
        if not os.path.isdir(dirname):
            print('Sorry! The directory path is not valid')
            sys.exit(3)
        else:
            return dirname

    @staticmethod
    def get_year_and_month(file_name):

        temp = file_name.split('_')
        year = temp[2]
        month = temp[3][:-4]

        return year, str(strptime(month, '%b').tm_mon)

    def parse_file(self, dir_path):

        file_names = os.listdir(self.is_dir(dir_path))
        os.chdir(dir_path)

        for file_name in file_names:
            with open(file_name, 'r') as file:
                year, month = self.get_year_and_month(file_name)
                read_csv = csv.DictReader(file, delimiter=',')
                for i, row in enumerate(read_csv):
                    row = {k.strip(): v.strip() for k, v in row.items()}
                    self.month_data[str(i + 1)] = row

                self.year_data[year][month] = copy.deepcopy(self.month_data)
                self.month_data.clear()


class ResultComputer:

    def compute_avg_results(self, month_data):
        sum_highest = sum_lowest = sum_humidity = 0
        count_highest_temp = count_lowest_temp = count_humidity = 0

        for day in month_data.values():
            if day['Max TemperatureC'] is not EMPTY:
                sum_highest += int(day['Max TemperatureC'])
                count_highest_temp += 1

            if day['Min TemperatureC'] is not EMPTY:
                sum_lowest += int(day['Min TemperatureC'])
                count_lowest_temp += 1

            if day['Max Humidity'] is not EMPTY:
                sum_humidity += int(day['Max Humidity'])
                count_humidity += 1

        return (
            sum_highest / count_highest_temp, sum_lowest / count_lowest_temp,
            sum_humidity / count_humidity
        )

    def compute_extreme_results(self, year_data):
        highest_temp = -273
        lowest_temp = +273
        highest_humidity = -100

        for month in year_data.values():
            for day in month.values():

                if day['Max TemperatureC'] is not EMPTY:
                    val = int(day['Max TemperatureC'])
                    if val > highest_temp:
                        highest_temp = val
                        highest_temp_date = day['PKT']

                if day['Min TemperatureC'] is not EMPTY:
                    val = int(day['Min TemperatureC'])
                    if val < lowest_temp:
                        lowest_temp = val
                        lowest_temp_date = day['PKT']

                if day['Max Humidity'] is not EMPTY:
                    val = int(day['Max Humidity'])
                    if val > highest_humidity:
                        highest_humidity = val
                        highest_humidity_date = day['PKT']

        return (
            highest_temp, highest_temp_date,
            lowest_temp, lowest_temp_date,
            highest_humidity, highest_humidity_date
        )

    def compute_high_low_day_results(self, month_data):

        temp_list = []

        for day in month_data.values():
            if day['Max TemperatureC'] is not EMPTY and day['Min TemperatureC'] is not EMPTY:
                temp_list.append((int(day['Max TemperatureC']), int(day['Min TemperatureC'])))

        return temp_list


class ResultGenerator:
    def gen_ext_results(self, data):
        date = datetime.datetime.strptime(data[1], '%Y-%m-%d')
        print('Highest: {}C on {} {}'.format(data[0], calendar.month_name[date.month], date.day))
        date = datetime.datetime.strptime(data[3], '%Y-%m-%d')
        print('Lowest: {}C on {} {}'.format(data[2], calendar.month_name[date.month], date.day))
        date = datetime.datetime.strptime(data[5], '%Y-%m-%d')
        print('Humidity: {}% on {} {}\n'.format(data[4], calendar.month_name[date.month], date.day))

    def gen_avg_results(self, data):
        print('Highest Average: {}'.format(round(data[0], 2)))
        print('Lowest Average: {}'.format(round(data[1], 2)))
        print('Average Mean Humidity: {}\n'.format(round(data[2], 2)))

    def gen_high_low_day_double_results(self, data):

        for i, val in enumerate(data):
            print(COLOR_PURPLE + str(i + 1).zfill(2) + ' ' + COLOR_RED + '+' * data[i][0] + ' ' + COLOR_PURPLE + str(
                data[i][0]) + 'C\n'
                  + COLOR_PURPLE + str(i + 1).zfill(2) + ' ' + COLOR_BLUE + '+' * data[i][1] + ' ' + COLOR_PURPLE + str(
                data[i][1]) + 'C')

        print(COLOR_DEFAULT)

    def gen_high_low_day_single_results(self, data):

        for i, val in enumerate(data):
            print(COLOR_PURPLE + str(i + 1).zfill(2) + ' ' + COLOR_BLUE + '+' * data[i][1] + COLOR_RED +
                  '+' * data[i][0] + ' ' + COLOR_PURPLE + str(data[i][1]) + 'C - ' + str(data[i][0]) + 'C')

        print(COLOR_DEFAULT)


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

    my_result_gen = ResultGenerator()

    if args.extreme_report:
        if args.extreme_report in my_parser.year_data:
            my_result_gen.gen_ext_results(
                my_computer.compute_extreme_results(my_parser.year_data[args.extreme_report]))
        else:
            print('Sorry! Data is not available for report')
            sys.exit(1)

    if args.average_report:
        tokens = args.average_report.split('/')
        year = tokens[0]
        month = tokens[1]

        my_result_gen.gen_avg_results(
            my_computer.compute_avg_results(my_parser.year_data[year][month]))

    if args.chart_report:
        tokens = args.chart_report.split('/')
        year = tokens[0]
        month = tokens[1]

        my_result_gen.gen_high_low_day_double_results(
            my_computer.compute_high_low_day_results(my_parser.year_data[year][month]))

    if args.bonus:
        tokens = args.bonus.split('/')
        year = tokens[0]
        month = tokens[1]

        my_result_gen.gen_high_low_day_single_results(
            my_computer.compute_high_low_day_results(my_parser.year_data[year][month]))


if __name__ == '__main__':
    try:
        main()
    except IndexError:
        print('Sorry! The input provided is not valid')
        sys.exit(2)
    except KeyboardInterrupt:
        print('Killed by user')
        sys.exit(4)
