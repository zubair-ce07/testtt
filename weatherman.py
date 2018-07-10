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

    reading_file_paths = glob(args.directory+'/*.txt')
    weather_readings = []
    for file_path in reading_file_paths:
            with open(file_path, 'r') as opened_reading_file:
                weather_reading_csv = csv.DictReader(opened_reading_file)
                for row in weather_reading_csv:
                    weather_readings.append(WeatherReading(row))

    if args.extreme:
        weather_readings_extreme = list(filter(lambda x: x.pkt.startswith(args.extreme), weather_readings))
        if weather_readings_extreme:
            extreme_weather_results = WeatherReport.yearly_results(weather_readings_extreme)
            weather_report_extreme(extreme_weather_results)
        else:
            print("Readings not available for " + args.extreme)
    if args.average:
        input_date_average = args.average
        input_date_average = input_date_average.split('/')
        average_weather_regex = input_date_average[0]+'-'+str(int(input_date_average[1]))+'-'
        weather_readings_average = list(filter(lambda x: re.match(average_weather_regex, x.pkt), weather_readings))
        if weather_readings_average:
            average_weather_results = WeatherReport.monthly_results(weather_readings_average)
            weather_report_average(average_weather_results)
        else:
            print("Readings not available for " + args.average)

    if args.chart:
        input_date_chart = args.chart
        input_date_chart = input_date_chart.split('/')
        chart_weather_regex = input_date_chart[0]+'-'+str(int(input_date_chart[1]))+'-'
        weather_readings_chart = list(filter(lambda x: re.match(chart_weather_regex, x.pkt), weather_readings))
        if weather_readings_chart:
            weather_report_chart(weather_readings_chart)
        else:
            print("Readings not available for " + args.chart)


def weather_report_extreme(result):
    """"Displays the highest lowest temperature and highest humidity report"""
    high_day = datetime.strptime(result.highest_day, "%Y-%m-%d").strftime('%B %d')
    print("Highest: " + str(result.highest_reading) + "C on " + high_day)
    low_day = datetime.strptime(result.lowest_day, "%Y-%m-%d").strftime('%B %d')
    print("Lowest: " + str(result.lowest_reading) + "C on " + low_day)
    humid_day = datetime.strptime(result.humidity_day, "%Y-%m-%d").strftime('%B %d')
    print("Humidity: " + str(result.humidity_reading) + "% on " + humid_day)
    print("")


def weather_report_average(result):
    """Displays the average highest lowest temperature and humidity of a month"""
    print("Highest Average: " + str(result.highest_reading) + "C")
    print("Lowest Average: " + str(result.lowest_reading) + "C")
    print("Average mean humidity: " + str(result.humidity_reading) + "%")
    print("")


def weather_report_chart(weather_readings):
    """"Displays the bar chart for temperatures through the month"""
    report_month = datetime.strptime(weather_readings[0].pkt, "%Y-%m-%d").strftime('%B %Y')

    print(report_month)
    for reading in weather_readings:
        day_number = datetime.strptime(reading.pkt, "%Y-%m-%d").strftime('%d')
        if reading.max_temperature and reading.min_temperature:
            print(day_number + ColorOutput.BLUE + "+" * reading.min_temperature + ColorOutput.RED +
                  "+" * reading.max_temperature + ColorOutput.RESET + str(reading.min_temperature) +
                  "C-" + str(reading.max_temperature) + "C")
    print("")


def year_validate(year_input):
    if re.match('\d\d\d\d$', year_input) or not year_input:
        return year_input
    else:
        raise argparse.ArgumentTypeError(year_input+" is invalid format please enter yyyy")


def month_validate(month_input):
    if re.match('\d\d\d\d/\d?\d$', month_input) or not month_input:
        return month_input
    else:
        raise argparse.ArgumentTypeError(month_input+" is invalid format please enter yyyy/mm")


def directory_validate(input_directory):
    if path.exists(input_directory):
        return input_directory
    else:
        raise argparse.ArgumentTypeError(input_directory + ' is invalid directory.')


class ColorOutput:
    RED = "\033[31m"
    BLUE = "\033[34m"
    RESET = "\033[0m"


if __name__ == '__main__':
    main()
