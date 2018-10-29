#!/usr/bin/python3.6
import argparse
import os
import glob
import datetime

import constants
from weather_data_analysis import WeatherDataAnalysis
from weather_readings import WeatherReadings
from weather_reporting import WeatherReporting
from csv_file_data_holder import CsvFileDataHolder


def parse_records(operation, dates, weather_records, path_to_files):
    if not dates:
        return

    for date in dates:
        analyse_weather = WeatherDataAnalysis()
        report_weather = WeatherReporting()
        add_current_year_weather_readings(
            date, weather_records, path_to_files)
        report = analyse_weather.analyse(operation, weather_records, date)
        report_weather.display_report(report, operation, date)


def add_current_year_weather_readings(date, weather_records, path_to_files):
    months_in_year = weather_records.get_months_data_of_year(date.year)
    if months_in_year is None:
        months_in_year = {}
        month_files_path = glob.glob(path_to_files+'/*'+str(date.year)+'*.txt')
        for month_file_path in month_files_path:
            month = CsvFileDataHolder()
            month.read_csv_file(month_file_path)
            months_in_year[month.months_name()] = month
        weather_records.add_new_year(date.year, months_in_year)


def year_validator(date_value):
    try:
        date_value = datetime.datetime.strptime(date_value, '%Y')
        return date_value
    except ValueError:
        raise argparse.ArgumentTypeError(constants.YEAR_ARGUMENT_ERROR_MESSAGE)


def year_and_month_validator(date_value):
    try:
        date_value = datetime.datetime.strptime(date_value, '%Y/%m')
        return date_value
    except ValueError:
        raise argparse.ArgumentTypeError(
            constants.MONTH_ARGUMENT_ERROR_MESSAGE)


def path_validator(path_value):
    if os.access(path_value, os.R_OK):
        return path_value
    else:
        raise argparse.ArgumentTypeError(constants.DIRECTORY_ERROR_MESSAGE)


def driver():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=path_validator,
                        help=constants.PATH_ARGUMENT_DISCRIPTION)
    parser.add_argument('-e', type=year_validator, nargs='+',
                        help=constants.YEAR_ARGUMENT_DISCRIPTION)
    parser.add_argument('-a', type=year_and_month_validator,
                        nargs='+', help=constants.MONTH_ARGUMENT_DISCRIPTION)
    parser.add_argument('-c', type=year_and_month_validator, nargs='+',
                        help=constants.MONTH_BARCHART_ARGUMENT_DISCRIPTION)
    args = parser.parse_args()
    weather_records = WeatherReadings()
    parse_records('e', args.e, weather_records, args.path)
    parse_records('a', args.a, weather_records, args.path)
    parse_records('c', args.c, weather_records, args.path)


if __name__ == '__main__':
    driver()
