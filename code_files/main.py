#!/usr/bin/python3.6

import csv
import sys
import re
import argparse

import calculations
import constants

from year_data_holder import YearsDataHolder
from result_generation import display_results
from csv_file_data_holder import CsvFileDataHolder


def parse_e(values, years_holder, files_path):
    if values is None:
        return
    for value in values:
        current_year = value
        current_operation = 'e' + value
        if re.match(r'e\d{4}$', current_operation):
            add_current_year(current_year, years_holder, files_path)
            result = calculations.calculate_yearly_record(
                years_holder, current_year)
            result.append(current_year)
            display_results(result, 'e')
        else:
            print(constants.ARGUMENT_ERROR_MESSAGE, current_operation)


def parse_a(values, years_holder, files_path):
    if values is None:
        return
    for value in values:
        current_operation = 'a' + value
        if re.match(r'a\d{4}/0?[1-9]|[1-9][0-2]$', current_operation):
            current_year = value.split('/')[0]
            month_number = int(value.split('/')[1])-1
            add_current_year(current_year, years_holder, files_path)
            result = calculations.calculate_month_record(
                years_holder, current_year, month_number
            )
            result.append(
                constants.MONTHS_NAME[month_number]
                + ', ' + current_year
            )
            display_results(result, 'a')
        else:
            print(constants.ARGUMENT_ERROR_MESSAGE, current_operation)


def parse_c(values, years_holder, files_path):
    if values is None:
        return
    for value in values:
        current_operation = 'c' + value
        if re.match(r'c\d{4}/0?[1-9]|[1-9][0-2]$', current_operation):
            current_year = value.split('/')[0]
            month_number = int(value.split('/')[1])-1
            add_current_year(current_year, years_holder, files_path)
            result = calculations.calculate_month_record_for_bar_charts(
                years_holder, current_year, month_number
            )
            result['year'] = (
                constants.MONTHS_NAME[month_number]
                + ', ' + current_year
            )
            display_results(result, 'c')
        else:
            print(constants.ARGUMENT_ERROR_MESSAGE, current_operation)


def add_current_year(current_year, years_holder, files_path):
    month_list = years_holder.get_months_list_by_year(current_year)
    if month_list is None:
        month_list = []
        for name in constants.MONTHS_NAME:
            file_path = files_path + 'Murree_weather_' + \
                current_year + '_' + name[:3] + '.txt'
            my_month = CsvFileDataHolder()
            my_month.read_csv_file(file_path)
            if my_month.csv_file is None:
                my_month = None
            month_list.append(my_month)
        years_holder.add_new_year(current_year, month_list)


# main function
parser = argparse.ArgumentParser(description='practice')

parser.add_argument('path')
parser.add_argument('-e', nargs='*')
parser.add_argument('-a', nargs='*')
parser.add_argument('-c', nargs='*')

args = parser.parse_args()

if args.e is not None or args.a is not None or args.c is not None:
    years_holder = YearsDataHolder()
    files_path = args.path
    if files_path[-1] != '/':
        files_path = files_path + '/'
    parse_e(args.e, years_holder, files_path)
    parse_a(args.a, years_holder, files_path)
    parse_c(args.c, years_holder, files_path)
