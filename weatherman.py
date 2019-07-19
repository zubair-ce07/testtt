import sys
import os
import glob
import argparse

from parser import WeatherParser
from analyzer import WeatherAnalyzer
from reporter import WeatherReporter

arg_parser = argparse.ArgumentParser(description="Program to parse, analyze and report weather readings")
arg_parser.add_argument('readings_dir', help="Path to weather readings directory")
arg_parser.add_argument('-e', help="Display the highest temperature and day, lowest temperature and day, most humid day and humidity for a given year (e.g. 2002)")
arg_parser.add_argument("-a", help="Display the average highest temperature, average lowest temperature, average mean humidity for a given month (e.g. 2005/6)")
arg_parser.add_argument("-c", help="Draw two horizontal bar charts on the console for the highest and lowest temperature on each day. Highest in red and lowest in blue for a given month")
arg_parser.add_argument("-o", help="Draw one horizontal bar chart on the console for the highest and lowest temperature on each day. Highest in red and lowest in blue for a given month")


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
    hottest_day = analyzer.get_day_with_max_temperature_from_year(readings, year)
    coldest_day = analyzer.get_day_with_min_temperature_from_year(readings, year)
    most_humid_day = analyzer.get_day_with_max_humidity_from_year(readings, year)
    reporter.report_year_extremes(hottest_day, coldest_day, most_humid_day)


def get_monthly_reports(readings, year, month):
    """Report the average highest temperature, average lowest temperature and average mean humidity for a month"""
    avg_hottest_temperature = analyzer.get_avg_max_temperature_from_month(readings, year, month)
    avg_coldest_temperature = analyzer.get_avg_min_temperature_from_month(readings, year, month)
    avg_humidity = analyzer.get_avg_mean_humidity_from_month(readings, year, month)
    reporter.report_month_averages(avg_hottest_temperature, avg_coldest_temperature, avg_humidity)


def get_monthly_bar_charts(readings, year, month):
    """Print bar charts for the highest and lowest temperatures in a month"""
    max_temperatures = analyzer.get_list_of_max_temperatures_from_month(
        readings, year, month)
    min_temperatures = analyzer.get_list_of_min_temperatures_from_month(
        readings, year, month)
    reporter.report_month_temperatures(max_temperatures, min_temperatures)


def get_monthly_single_bar_chart(readings, year, month):
    """Print single lined bar charts for the highest and lowest temperatures in a month"""
    max_temperatures = analyzer.get_list_of_max_temperatures_from_month(
        readings, year, month)
    min_temperatures = analyzer.get_list_of_min_temperatures_from_month(
        readings, year, month)
    reporter.report_month_temperatures(
        max_temperatures, min_temperatures, True)


if __name__ == "__main__":
    """Parse the arguments passed to the program"""

    if arguments.e:
        try:
            year = arguments.e
            year = int(year)
        except ValueError:
            print("-e argument only accepts year e.g. 2002")
            exit(1)
        get_yearly_reports(readings, year)

    if arguments.a:
        try:
            year, month = arguments.a.split("/")
        except ValueError:
            print("Please pass month with year with argument -e .g. 2005/6")
            exit(1)
        get_monthly_reports(readings, int(year), int(month))

    if arguments.c:
        try:
            year, month = arguments.c.split("/")
        except ValueError:
            print("Please pass month with year with argument -c e.g. 2005/6")
            exit(1)
        get_monthly_bar_charts(readings, int(year), int(month))

    if arguments.o:
        try:
            year, month = arguments.o.split("/")
        except IndexError:
            print("Please pass year and month with argument -o e.g. 2005/6")
            exit(1)
        except ValueError:
            print("Please pass month with year with argument -o e.g. 2005/6")
            exit(1)
        get_monthly_single_bar_chart(readings, int(year), int(month))
