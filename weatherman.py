import sys
import os
import glob
import argparse

from parser import WeatherParser
from analyzer import WeatherAnalyzer
from reporter import WeatherReporter


def is_year(year):
    try:
        year = int(year)
    except ValueError:
        message = "{} is not a valid year.".format(year)
        raise argparse.ArgumentTypeError(message)
    return year


def is_month(month):
    try:
        year, month = month.split("/")
    except ValueError:
        message = "Please pass month with year in the format YYYY/MM e.g. 2005/6"
        raise argparse.ArgumentTypeError(message)
    year = is_year(year)
    try:
        month = int(month)
        if month < 1 or month > 12:
            raise ValueError
    except ValueError:
        message = "{} is not a valid month.".format(month)
        raise argparse.ArgumentTypeError(message)
    return [year, month]


arg_parser = argparse.ArgumentParser(
    description="Program to parse, analyze and report weather readings")
arg_parser.add_argument(
    'readings_dir', help="Path to weather readings directory")
arg_parser.add_argument(
    '-e', type=is_year, help="Display the highest temperature and day, lowest temperature and day, most humid day and humidity for a given year (e.g. 2002)")
arg_parser.add_argument(
    "-a", type=is_month, help="Display the average highest temperature, average lowest temperature, average mean humidity for a given month (e.g. 2005/6)")
arg_parser.add_argument(
    "-c", type=is_month, help="Draw two horizontal bar charts on the console for the highest and lowest temperature on each day. Highest in red and lowest in blue for a given month")
arg_parser.add_argument(
    "-o", type=is_month, help="Draw one horizontal bar chart on the console for the highest and lowest temperature on each day. Highest in red and lowest in blue for a given month")


arguments = arg_parser.parse_args()

parser = WeatherParser()

readings = []
file_paths = glob.glob(arguments.readings_dir + "/*")

for file_path in file_paths:
    readings = readings + parser.parse_weather_file(file_path)

analyzer = WeatherAnalyzer()
reporter = WeatherReporter()


def get_yearly_reports(readings, year):
    """Report the hottest, coldest and the most humid day in a year"""
    hottest_day = analyzer.get_maximum_temperature_day(readings, year)
    coldest_day = analyzer.get_minimum_temperature_day(readings, year)
    most_humid_day = analyzer.get_most_humidity_day(readings, year)
    reporter.report_year_extremes(hottest_day, coldest_day, most_humid_day)


def get_monthly_reports(readings, year, month):
    """Report the average highest temperature, average lowest temperature and average mean humidity for a month"""
    avg_hottest_temperature = analyzer.get_avg_maximum_temperature(
        readings, year, month)
    avg_coldest_temperature = analyzer.get_avg_minimum_temperature(
        readings, year, month)
    avg_humidity = analyzer.get_avg_mean_humidity(readings, year, month)
    reporter.report_month_averages(
        avg_hottest_temperature, avg_coldest_temperature, avg_humidity)


def get_monthly_bar_charts(readings, year, month):
    """Print bar charts for the highest and lowest temperatures in a month"""
    max_temperatures = analyzer.get_maximum_temperatures(
        readings, year, month)
    min_temperatures = analyzer.get_minimum_temperatures(
        readings, year, month)
    reporter.report_month_temperatures(max_temperatures, min_temperatures)


def get_monthly_single_bar_chart(readings, year, month):
    """Print single lined bar charts for the highest and lowest temperatures in a month"""
    max_temperatures = analyzer.get_maximum_temperatures(
        readings, year, month)
    min_temperatures = analyzer.get_minimum_temperatures(
        readings, year, month)
    reporter.report_month_temperatures(
        max_temperatures, min_temperatures, True)


if __name__ == "__main__":
    """Parse the arguments passed to the program"""

    if arguments.e:
        get_yearly_reports(readings, arguments.e)

    if arguments.a:
        get_monthly_reports(readings, arguments.a[0], arguments.a[1])

    if arguments.c:
        get_monthly_bar_charts(readings, arguments.c[0], arguments.c[1])

    if arguments.o:
        get_monthly_single_bar_chart(readings, arguments.o[0], arguments.o[1])
