#!/usr/bin/python3.6
import argparse
import os
import glob
import datetime

import constants
from weather_data_analysis import WeatherDataAnalysis
from weather_readings import WeatherReadings
from weather_reporting import WeatherReporting
from read_weather import ReadWeather


def read_weather_records(path_to_files):
    files_path = glob.glob(path_to_files+'/*_weather_*_*.txt')
    weather_records = WeatherReadings()

    for file_path in files_path:
        month = ReadWeather()
        month.read_file(file_path)
        weather_records.add_month(month)
    
    return weather_records


def year_validator(date_value):
    try:
        return datetime.datetime.strptime(date_value, '%Y')
    except ValueError:
        raise argparse.ArgumentTypeError(constants.YEAR_ARGUMENT_ERROR_MESSAGE)


def year_and_month_validator(date_value):
    try:
        return datetime.datetime.strptime(date_value, '%Y/%m')
    except ValueError:
        raise argparse.ArgumentTypeError(constants.MONTH_ARGUMENT_ERROR_MESSAGE)


def path_validator(path_value):
    if os.access(path_value, os.R_OK):
        return path_value
    else:
        raise argparse.ArgumentTypeError(constants.DIRECTORY_ERROR_MESSAGE)


def main():
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

    weather_records = read_weather_records(args.path)
    analyse_weather = WeatherDataAnalysis()
    report_weather = WeatherReporting()

    for date in args.e or []:
        year_report = analyse_weather.calculate_yearly_report(weather_records, date)
        report_weather.yearly_report(year_report)
    
    for date in args.a or []:
        month_report = analyse_weather.calculate_monthly_report(weather_records, date)
        report_weather.monthly_report(month_report)
    
    for date in args.c or []:
        report_weather.monthly_bar_chart(weather_records, date)


if __name__ == '__main__':
    main()
