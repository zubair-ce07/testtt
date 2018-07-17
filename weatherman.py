import os
import argparse
import csv
import glob
from datetime import datetime
from statistics import mean
from collections import namedtuple
from operator import attrgetter


class WeatherRecord:

    def __init__(self, features):
        self.pkt = features.get('PKT') or features.get('PKST')
        self.pkt = datetime.strptime(self.pkt, '%Y-%m-%d')
        self.max_temp = int(features.get('Max TemperatureC'))
        self.min_temp = int(features.get('Min TemperatureC'))
        self.mean_temp = int(features.get('Mean TemperatureC'))
        self.max_humidity = int(features.get('Max Humidity'))
        self.min_humidity = int(features.get(' Min Humidity'))
        self.mean_humidity = int(features.get(' Mean Humidity'))


class CalculateReadings:

    @staticmethod
    def ext_readings(weather_records, given_date):
        weather_readings = list(filter(lambda e: e.pkt.year == given_date.year,
                                       weather_records))

        max_temperatures = list(
            filter(attrgetter('max_temp'), weather_readings))
        min_temperatures = list(
            filter(attrgetter('min_temp'), weather_readings))
        max_humidity = list(
            filter(attrgetter('max_humidity'), weather_readings))

        max_temperature = max(max_temperatures, key=attrgetter('max_temp'))
        min_temperature = min(min_temperatures, key=attrgetter('min_temp'))
        max_humid = max(max_humidity, key=attrgetter('max_humidity'))

        calculation_holder = namedtuple('calculation_holder', 'maximum_temp,\
                                        minimum_temp, maximum_humidity,\
                                        maximum_temp_day, minimum_temp_day,\
                                        maximum_humidity_day')
        return calculation_holder(max_temperature.max_temp,
                                  min_temperature.min_temp,
                                  max_humid.max_humidity,
                                  max_temperature.pkt.strftime("%A %B %d"),
                                  min_temperature.pkt.strftime("%A %B %d"),
                                  max_humid.pkt.strftime("%A %B %d"))

    @staticmethod
    def avg_readings(weather_records, given_date):
        weather_readings = list(filter(lambda a: a.pkt.year == given_date.year and
                                       a.pkt.month == given_date.month, weather_records))
        mean_temps = list(filter(attrgetter('mean_temp'), weather_readings))
        mean_humid = list(
            filter(attrgetter('mean_humidity'), weather_readings))

        mean_value = mean(m.mean_humidity for m in mean_humid)
        highest_mean_temp = max(mean_temps, key=attrgetter('mean_temp'))
        lowest_mean_temp = min(mean_temps, key=attrgetter('mean_temp'))

        calculation_holder = namedtuple(
            'calculation_holder', 'max_mean_temp, min_mean_temp, average_mean_humidity')
        return calculation_holder(highest_mean_temp.mean_temp,
                                  lowest_mean_temp.mean_temp,
                                  mean_value)


class PrintReports:

    @staticmethod
    def extreme_readings(given_date, weather_readings):

        highest = f"Highest: {weather_readings.maximum_temp}C on {weather_readings.maximum_temp_day}"
        lowest = f"Lowest: {weather_readings.minimum_temp}C on {weather_readings.minimum_temp_day}"
        humidity = f"Humidity: {weather_readings.maximum_humidity}% on {weather_readings.maximum_humidity_day}\n"

        results = [
            highest,
            lowest,
            humidity
        ]

        print('\n'.join(results))

    @staticmethod
    def average_readings(given_date, weather_readings):

        highest_avg = f"Highest Average: {weather_readings.max_mean_temp}C"
        lowest_average = f"Lowest Average: {weather_readings.min_mean_temp}C"
        mean_humidity = f"Average Mean Humidity: {int(weather_readings.average_mean_humidity)}%\n"

        results = [
            highest_avg,
            lowest_average,
            mean_humidity
        ]

        print('\n'.join(results))

    @staticmethod
    def charts_of_readings(weather_readings):

        RED = "\u001b[31m"
        BLUE = "\u001b[34m"
        RESET = "\u001b[0m"

        report_date = weather_readings[2]
        day = f"{int(report_date)}"
        symbols = f"{BLUE}{'+' * int(weather_readings[1])}{RED}{'+' * int(weather_readings[0])}"
        min_temp = f" {RESET}{int(weather_readings[1])}C - "
        max_temp = f"{int(weather_readings[0])}C{RESET}"

        results = [
            day,
            symbols,
            min_temp,
            max_temp
        ]

        print(' '.join(results))


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory_path", type=str,
                        help="Path to the directory containing data files")
    parser.add_argument("-a", "--average", type=lambda a:
                        datetime.strptime(a, '%Y/%m'),
                        action='append')
    parser.add_argument("-e", "--extreme", type=lambda e:
                        datetime.strptime(e, '%Y'),
                        action='append')
    parser.add_argument("-c", "--chart", type=lambda c:
                        datetime.strptime(c, '%Y/%m'),
                        action='append')
    return parser.parse_args()


def parse_files(directory):
    if not os.path.isabs(directory):
        directory = os.path.abspath(directory)+"/"
    weather_records = []
    required_features = ['Max TemperatureC', 'Min TemperatureC',
                         'Mean TemperatureC', 'Max Humidity',
                         ' Min Humidity', ' Mean Humidity']
    for data_file in glob.iglob(directory+'*.txt'):
        with open(data_file) as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                if all(row[rf] for rf in required_features):
                    weather_records.append(WeatherRecord(row))
    return weather_records


def main():

    args = parse_arguments()
    weather_records = parse_files(args.directory_path)

    if args.average:
        for arg in args.average:
            weather_result = CalculateReadings.avg_readings(
                weather_records, arg)
            PrintReports.average_readings(arg, weather_result)

    if args.extreme:
        for arg in args.extreme:
            weather_result = CalculateReadings.ext_readings(
                weather_records, arg)
            PrintReports.extreme_readings(arg, weather_result)

    if args.chart:
        for arg in args.chart:
            weather_readings = list(filter(lambda a: a.pkt.year == arg.year and
                                           a.pkt.month == arg.month, weather_records))
            for record in weather_readings:
                PrintReports.charts_of_readings([record.max_temp,
                                                 record.min_temp,
                                                 str(record.pkt.day)])


if __name__ == "__main__":
    main()
