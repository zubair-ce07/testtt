import argparse
import csv
import re
from os import path
from glob import glob
from datetime import datetime
from weatherman_ds import WeatherReading
from weatherman_calculation import WeatherReport


def main():

    parser = argparse.ArgumentParser(description='A program that calculates '
                                                 'weather information and'
                                                 ' visualizes it.')

    parser.add_argument('directory', help='directory of the weather readings.', type=directory_validate)
    parser.add_argument('-e', '--extreme', default='', help='option for extreme '
                        'weather report format:yyyy', type=year_validate)
    parser.add_argument('-a', '--average', default='', help='option for average'
                        ' weather report format:yyyy/mm', type=month_validate)
    parser.add_argument('-c', '--chart', default='', help='option for weather '
                        ' chart format:yyyy/mm', type=month_validate)

    args = parser.parse_args()

    weather_readings = load_weather_data(args.directory)
    if args.extreme:
        extreme_weather_handler(weather_readings, args.extreme)
    if args.average:
        average_weather_handler(weather_readings, args.average)
    if args.chart:
        chart_weather_handler(weather_readings, args.chart)


def load_weather_data(directory):
    reading_file_paths = glob(directory + '/*.txt')
    weather_readings = []
    for file_path in reading_file_paths:
        with open(file_path, 'r') as opened_reading_file:
            weather_reading_csv = csv.DictReader(opened_reading_file)
            for row in weather_reading_csv:
                weather_readings.append(WeatherReading(row))
    return weather_readings


def extreme_weather_handler(weather_readings, input_date_extreme):
    weather_readings_extreme = readings_filter_year(weather_readings, input_date_extreme)
    if weather_readings_extreme:
        extreme_weather_results = WeatherReport.yearly_results(weather_readings_extreme)
        weather_report_extreme(extreme_weather_results)
    else:
        print("Readings not available for " + input_date_extreme)


def average_weather_handler(weather_readings, input_date_average):
    weather_readings_average = readings_filter_month(weather_readings, input_date_average)
    if weather_readings_average:
        average_weather_results = WeatherReport.monthly_results(weather_readings_average)
        weather_report_average(average_weather_results)
    else:
        print("Readings not available for " + input_date_average)


def chart_weather_handler(weather_readings, input_date_chart):
    weather_readings_chart = readings_filter_month(weather_readings, input_date_chart)
    if weather_readings_chart:
        weather_report_chart(weather_readings_chart, input_date_chart)
    else:
        print("Readings not available for " + input_date_chart)


def readings_filter_month(weather_readings, month):
    readings_date = datetime.strptime(month, '%Y/%m').strftime('%Y-%-m-')
    filtered_weather_readings = list(filter(lambda day: day.pkt.startswith(readings_date), weather_readings))
    return filtered_weather_readings


def readings_filter_year(weather_readings, year):
    filtered_weather_readings = list(filter(lambda day: day.pkt.startswith(year), weather_readings))
    return filtered_weather_readings


def weather_report_extreme(result):
    """"Displays the highest lowest temperature and highest humidity report"""
    high_day = datetime.strptime(result.highest_day, "%Y-%m-%d")
    low_day = datetime.strptime(result.lowest_day, "%Y-%m-%d")
    humid_day = datetime.strptime(result.humidity_day, "%Y-%m-%d")

    print(f"Highest: {result.highest_reading}C on {high_day:%B %d}")
    print(f"Lowest: {result.lowest_reading}C on {low_day:%B %d}")
    print(f"Humidity: {result.humidity_reading}% on {humid_day:%B %d}")


def weather_report_average(result):
    """Displays the average highest lowest temperature and humidity of a month"""
    print(f"Highest Average: {result.highest_reading}C")
    print(f"Lowest Average: {result.lowest_reading}C")
    print(f"Average mean humidity: {result.humidity_reading}%")


def weather_report_chart(weather_readings, input_date_chart):
    """"Displays the bar chart for temperatures through the month"""
    def repeat_plus(x): return '+' * x

    report_month = datetime.strptime(input_date_chart, "%Y/%m")
    print(f"{report_month:%B %Y}")
    day_number = 1
    for reading in weather_readings:

        if reading.max_temperature and reading.min_temperature:
            print(f"{day_number:{0}{2}}{ColorOutput.BLUE}{repeat_plus(reading.min_temperature)}{ColorOutput.RED}"
                  f"{repeat_plus(reading.max_temperature)}{ColorOutput.RESET}{reading.min_temperature}"
                  f"C-{reading.max_temperature}C")
        day_number += 1


def year_validate(year_input):
    if not year_input or re.match('\d{4}$', year_input):
        return year_input
    raise argparse.ArgumentTypeError(year_input+" is invalid format please enter yyyy")


def month_validate(month_input):
    if not month_input or re.match('\d{4}/\d{1,2}$', month_input):
        return month_input
    raise argparse.ArgumentTypeError(month_input+" is invalid format please enter yyyy/mm")


def directory_validate(input_directory):
    if path.exists(input_directory):
        return input_directory
    raise argparse.ArgumentTypeError(input_directory + " is invalid directory")


class ColorOutput:
    RED = "\033[31m"
    BLUE = "\033[34m"
    RESET = "\033[0m"


if __name__ == '__main__':
    main()
