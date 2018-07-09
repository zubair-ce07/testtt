import argparse
import os
import csv
import datetime
import re
from weatherman_ds import WeatherReading
from weatherman_calculation import WeatherReport


def main():

    parser = argparse.ArgumentParser(description='A program that calculates '
                                                 'weather information and'
                                                 ' visualizes it.')

    parser.add_argument('directory', help='directory of the weather readings.')
    parser.add_argument('-e', '--extreme', default='', help='option for extreme '
                        'weather report format:yyyy', type=year_validate)
    parser.add_argument('-a', '--average', default='', help='option for average'
                        ' weather report format:yyyy/mm', type=month_validate)
    parser.add_argument('-c', '--chart', default='', help='option for weather '
                        ' chart format:yyyy/mm', type=month_validate)

    args = parser.parse_args()

    if args.extreme:
        input_date_extreme = args.extreme
        weather_readings_extreme = load_readings(args.directory,
                                                 input_date_extreme)
        if weather_readings_extreme:
            extreme_weather_results = WeatherReport.yearly_results(weather_readings_extreme)
            weather_report_extreme(extreme_weather_results)
        else:
            print("Readings not available for " + args.extreme)
    if args.average:
        input_date_average = args.average
        input_date_average = input_date_average.split('/')
        weather_readings_average = load_readings(args.directory,
                                                 input_date_average[0],
                                                 input_date_average[1])
        if weather_readings_average:
            average_weather_results = WeatherReport.monthly_results(weather_readings_average)
            weather_report_average(average_weather_results)
        else:
            print("Readings not available for " + args.average)

    if args.chart:
        input_date_chart = args.chart
        input_date_chart = input_date_chart.split('/')
        weather_readings_chart = load_readings(args.directory,
                                               input_date_chart[0],
                                               input_date_chart[1])
        if weather_readings_chart:
            weather_report_chart(weather_readings_chart)
        else:
            print("Readings not available for " + args.chart)


def load_readings(directory='', year='', month=''):
        """Loads a given months data in the data structure"""
        files = []
        daily_readings = []
        if not month:
            for i in range(1, 13):
                month_abr = datetime.date(2000, i, 1).strftime('%b')
                file_path = directory + '/Murree_weather_' + year + "_" + month_abr + '.txt'
                if os.path.exists(file_path):
                    file = open(file_path, 'r')
                    files.append(file)
        else:
            month_abr = datetime.date(2000, int(month), 1).strftime('%b')
            file_path = directory + '/Murree_weather_' + year + "_" + month_abr + '.txt'
            if os.path.exists(file_path):
                file = open(file_path, 'r')
                files.append(file)

        for file in files:
            weather_csv = csv.DictReader(file)
            for row in weather_csv:
                daily_readings.append(WeatherReading(row))

        return daily_readings


def weather_report_extreme(result):
    """"Displays the highest lowest temperature and highest humidity report"""
    high_day = datetime.datetime.strptime(result.highest_day, "%Y-%m-%d").strftime('%B %d')
    print("Highest: " + str(result.highest_reading) + "C on " + high_day)
    low_day = datetime.datetime.strptime(result.lowest_day, "%Y-%m-%d").strftime('%B %d')
    print("Lowest: " + str(result.lowest_reading) + "C on " + low_day)
    humid_day = datetime.datetime.strptime(result.humidity_day, "%Y-%m-%d").strftime('%B %d')
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
    report_month = datetime.datetime.strptime(weather_readings[0].pkt, "%Y-%m-%d").strftime('%B %Y')

    print(report_month)
    for reading in weather_readings:
        day_number = datetime.datetime.strptime(reading.pkt, "%Y-%m-%d").strftime('%d')
        max_temp = reading.max_temperature
        min_temp = reading.min_temperature
        if max_temp and min_temp:
            print(day_number + ColorOutput.BLUE + "+" * min_temp + ColorOutput.RED +
                  "+" * max_temp + ColorOutput.RESET + str(min_temp) +
                  "C-" + str(max_temp) + "C")
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


class ColorOutput:
    RED = "\033[31m"
    BLUE = "\033[34m"
    RESET = "\033[0m"


if __name__ == '__main__':
    main()
