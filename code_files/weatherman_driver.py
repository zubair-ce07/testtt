#!/usr/bin/python3.6

import csv
import sys
import re
import argparse
import os

from weather_data_analysis import WeatherDataAnalysis
from weather_readings import WeatherReadings
from weather_reporting import WeatherReporting
from csv_file_data_holder import CsvFileDataHolder
from constants import MONTHS_NAME
from constants import ARGUMENT_ERROR_MESSAGE


def parse_records(operation, values, weather_readings, files_path):
    if values is None:
        return
    for value in values:
        weather_analysis = WeatherDataAnalysis()
        weather_reporting = WeatherReporting()
        current_year = value
        record_info = current_year
        month_number = 0
        if operation is not 'e':
            current_year = value.split('/')[0]
            month_number = int(value.split('/')[1])-1
            record_info = (MONTHS_NAME[month_number] + ', ' + current_year)
        add_current_year(current_year, weather_readings, files_path)
        report = weather_analysis.analyse(
            operation, weather_readings, current_year, month_number)
        weather_reporting.display_report(report, operation, record_info)


def add_current_year(current_year, weather_readings, files_path):
    month_list = weather_readings.get_months_list_by_year(current_year)
    if month_list is None:
        month_list = []
        for name in MONTHS_NAME:
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


def my_year_and_month_validator(value, year_validator=re.compile(r"\d{4}/(0?[1-9]|[1-9][0-2])$")):
    if not year_validator.match(value):
        raise argparse.ArgumentTypeError
    return value


def driver():
    parser = argparse.ArgumentParser()
    try:
        parser.add_argument('path')
        parser.add_argument('-e', type=my_year_validator, nargs='*')
        parser.add_argument(
            '-a', type=my_year_and_month_validator, nargs='*')
        parser.add_argument(
            '-c', type=my_year_and_month_validator, nargs='*')
        args = parser.parse_args()
        if os.access(args.path, os.R_OK):
            weather_readings = WeatherReadings()
            parse_records('e', args.e, weather_readings, args.path)
            parse_records('a', args.a, weather_readings, args.path)
            parse_records('c', args.c, weather_readings, args.path)
    except argparse.ArgumentTypeError:
        print(ARGUMENT_ERROR_MESSAGE)


if __name__ == '__main__':
    driver()
