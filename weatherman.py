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

analyzer = WeatherAnalyzer()
reporter = WeatherReporter()


def get_yearly_reports(readings_dir, year):
    """Report the hottest, coldest and the most humid day in a year"""
    readings = WeatherParser.parse_weather_files(readings_dir, year)
    hottest_day = analyzer.get_maximum_temperature_day(readings)
    coldest_day = analyzer.get_minimum_temperature_day(readings)
    most_humid_day = analyzer.get_most_humidity_day(readings)
    reporter.report_year_extremes(hottest_day, coldest_day, most_humid_day)


def get_monthly_reports(readings_dir, year, month):
    """Report the average highest temperature, average lowest temperature and average mean humidity for a month"""
    readings = WeatherParser.parse_weather_files(readings_dir, year, month)
    avg_hottest_temperature = analyzer.get_avg_maximum_temperature(readings)
    avg_coldest_temperature = analyzer.get_avg_minimum_temperature(readings)
    avg_humidity = analyzer.get_avg_mean_humidity(readings)
    reporter.report_month_averages(
        avg_hottest_temperature, avg_coldest_temperature, avg_humidity)


def get_monthly_bar_charts(readings_dir, year, month):
    """Print bar charts for the highest and lowest temperatures in a month"""
    readings = WeatherParser.parse_weather_files(readings_dir, year, month)
    max_temperatures = analyzer.get_maximum_temperatures(readings)
    min_temperatures = analyzer.get_minimum_temperatures(readings)
    reporter.report_month_temperatures(max_temperatures, min_temperatures)


def get_monthly_single_bar_chart(readings_dir, year, month):
    """Print single lined bar charts for the highest and lowest temperatures in a month"""
    readings = WeatherParser.parse_weather_files(readings_dir, year, month)
    max_temperatures = analyzer.get_maximum_temperatures(readings)
    min_temperatures = analyzer.get_minimum_temperatures(readings)
    reporter.report_month_temperatures(
        max_temperatures, min_temperatures, True)


if __name__ == "__main__":
    """Parse the arguments passed to the program"""

    if arguments.e:
        get_yearly_reports(arguments.readings_dir, arguments.e)

    if arguments.a:
        get_monthly_reports(arguments.readings_dir,
                            arguments.a[0], arguments.a[1])

    if arguments.c:
        get_monthly_bar_charts(arguments.readings_dir,
                               arguments.c[0], arguments.c[1])

    if arguments.o:
        get_monthly_single_bar_chart(
            arguments.readings_dir, arguments.o[0], arguments.o[1])
