import argparse
import os
import datetime


import constants
from weather_data_analysis import WeatherDataAnalysis
from weather_readings import WeatherReadings
from weather_reporting import WeatherReporting


def validate_year(date_value):
    try:
        return datetime.datetime.strptime(date_value, '%Y')
    except ValueError:
        raise argparse.ArgumentTypeError(constants.YEAR_ARGUMENT_ERROR_MESSAGE)


def validate_year_and_month(date_value):
    try:
        return datetime.datetime.strptime(date_value, '%Y/%m')
    except ValueError:
        raise argparse.ArgumentTypeError(
            constants.MONTH_ARGUMENT_ERROR_MESSAGE)


def validate_path(path_value):
    if os.access(path_value, os.R_OK):
        return path_value
    else:
        raise argparse.ArgumentTypeError(constants.DIRECTORY_ERROR_MESSAGE)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=validate_path,
                        help=constants.PATH_ARGUMENT_DISCRIPTION)
    parser.add_argument('-e', type=validate_year, nargs='+', default=[],
                        help=constants.YEAR_ARGUMENT_DISCRIPTION)
    parser.add_argument('-a', type=validate_year_and_month, nargs='+',
                        default=[], help=constants.MONTH_ARGUMENT_DISCRIPTION)
    parser.add_argument('-c', type=validate_year_and_month, nargs='+',
                        default=[], help=constants.MONTH_BARCHART_ARGUMENT_DISCRIPTION)
    args = parser.parse_args()

    weather_records = WeatherReadings()
    analyse_weather = WeatherDataAnalysis()
    report_weather = WeatherReporting()
    weather_records.read_weather_records(args.path)

    for date in args.e:
        year_records = weather_records.extract_year_readings(date)

        if not year_records:
            print(constants.FILE_ERROR_MESSAGE, '\n\n')
            continue

        year_report = analyse_weather.calculate_yearly_report(year_records)
        report_weather.display_year_report(year_report)

    for date in args.a:
        month_records = weather_records.extract_month_readings(date)
        if not month_records:
            print(constants.FILE_ERROR_MESSAGE, '\n\n')
            continue

        month_report = analyse_weather.calculate_monthly_report(month_records)
        report_weather.display_month_report(month_report)

    for date in args.c:
        month_records = weather_records.extract_month_readings(date)
        if not month_records:
            print(constants.FILE_ERROR_MESSAGE, '\n\n')
            continue

        report_weather.display_month_bar_chart(month_records)


if __name__ == '__main__':
    main()
