#!/usr/bin/python3.6

import csv
import sys
import re
import argparse
import os

import calculations
import constants

from weather_readings import WeatherReadings
from result_generation import display_results
from csv_file_data_holder import CsvFileDataHolder


def parse_yearly_records(values, weather_readings, files_path):
    if values is None:
        return
    for value in values:
        current_year = value
        add_current_year(current_year, weather_readings, files_path)
        result = calculations.calculate_yearly_record(
            weather_readings, current_year)
        result.append(current_year)
        display_results(result, 'e')


def parse_monthly_records(values, weather_readings, files_path):
    if values is None:
        return
    for value in values:
        current_year = value.split('/')[0]
        month_number = int(value.split('/')[1])-1
        add_current_year(current_year, weather_readings, files_path)
        result = calculations.calculate_month_record(
            weather_readings, current_year, month_number
        )
        result.append(
            constants.MONTHS_NAME[month_number]
            + ', ' + current_year
        )
        display_results(result, 'a')


def parse_monthly_records_for_barchart(values, weather_readings, files_path):
    if values is None:
        return
    for value in values:
        current_year = value.split('/')[0]
        month_number = int(value.split('/')[1])-1
        add_current_year(current_year, weather_readings, files_path)
        result = calculations.calculate_month_record_for_bar_charts(
            weather_readings, current_year, month_number
        )
        result['year'] = (
            constants.MONTHS_NAME[month_number]
            + ', ' + current_year
        )
        display_results(result, 'c')


def add_current_year(current_year, weather_readings, files_path):
    month_list = weather_readings.get_months_list_by_year(current_year)
    if month_list is None:
        month_list = []
        for name in constants.MONTHS_NAME:
            file_path = files_path + '/Murree_weather_' + \
                current_year + '_' + name[:3] + '.txt'
            my_month = CsvFileDataHolder()
            my_month.read_csv_file(file_path)
            if my_month.csv_file is None:
                my_month = None
            month_list.append(my_month)
        weather_readings.add_new_year(current_year, month_list)


def my_year_validator(value, year_validator=re.compile(r"[0-9]{4}$")):
    if not year_validator.match(value):
        raise argparse.ArgumentTypeError
    return value


def my_year_and_month_validator(value, year_validator=re.compile(r"\d{4}/0?[1-9]|[1-9][0-2]$")):
    if not year_validator.match(value):
        raise argparse.ArgumentTypeError
    return value


def driver():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    try:
        parser.add_argument('-e', type=my_year_validator, nargs='*')
        parser.add_argument('-a', type=my_year_and_month_validator, nargs='*')
        parser.add_argument('-c', type=my_year_and_month_validator, nargs='*')
        args = parser.parse_args()
        if os.access(args.path, os.R_OK):
            weather_readings = WeatherReadings()
            parse_yearly_records(args.e, weather_readings, args.path)
            parse_monthly_records(args.a, weather_readings, args.path)
            parse_monthly_records_for_barchart(
                args.c, weather_readings, args.path)
    except:
        print(constants.ARGUMENT_ERROR_MESSAGE)


if __name__ == '__main__':
    driver()
