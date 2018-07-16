import os
import argparse
import csv
import glob
from datetime import datetime

from weatherman_data_structure import WeatherRecord
from weatherman_data_structure import Colors
import weatherman_computations


def parse_files(directory):
    if not os.path.isabs(directory):
        directory = os.path.dirname(os.path.abspath(__file__)
                                    ) + directory.strip(".")
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


def display_extreme_readings(given_date, weather_readings):

    header = f"{Colors.GREEN}\n{'*' * 12} Extreme Readings of "\
        f"{given_date} {'*' * 12}\n{Colors.RESET}"

    highest = f"Highest: {weather_readings.maximum_temp}"\
        f"C on {weather_readings.maximum_temp_day}"

    lowest = f"Lowest: {weather_readings.minimum_temp}C on "\
        f"{weather_readings.minimum_temp_day}"

    humidity = f"Humidity: {weather_readings.maximum_humidity}% on "\
        f"{weather_readings.maximum_humidity_day}"

    results = [
        header,
        highest,
        lowest,
        humidity
    ]

    print('\n'.join(results))


def display_average_readings(given_date, weather_readings):

    header = f"{Colors.GREEN}\n{'*' * 12}Average Readings of "\
        f"{given_date} {'*' * 12}\n{Colors.RESET}"

    highest_avg = f"Highest Average: {weather_readings.max_mean_temp}C"
    lowest_average = f"Lowest Average: {weather_readings.min_mean_temp}C"
    mean_humidity = f"Average Mean Humidity: "\
        f"{int(weather_readings.average_mean_humidity)}%\n"

    results = [
        header,
        highest_avg,
        lowest_average,
        mean_humidity
    ]

    print('\n'.join(results))


def display_charts_of_readings(weather_readings):

    report_date = weather_readings[2]
    day = f"{Colors.MAGENTA}{int(report_date)}"
    symbols = f"{Colors.BLUE}{'+' * int(weather_readings[1])}"\
        f"{Colors.RED}{'+' * int(weather_readings[0])}"
    min_temp = f"{Colors.MAGENTA} {int(weather_readings[1])}C - "
    max_temp = f"{int(weather_readings[0])}C{Colors.RESET}"

    results = [
        day,
        symbols,
        min_temp,
        max_temp
    ]

    print(' '.join(results))


def filter_by_month(weather_records, given_date):
    return list(filter(lambda a: a.pkt.year == given_date.year and
                       a.pkt.month == given_date.month, weather_records))


def filter_by_year(weather_records, given_date):
    return list(filter(lambda e: e.pkt.year == given_date.year,
                       weather_records))


def main():

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
    args = parser.parse_args()
    weather_records = parse_files(args.directory_path)
    if args.average:
        for arg in args.average:
            weather_readings = filter_by_month(weather_records, arg)
            weather_result = weatherman_computations.calculate_avg_readings(
                             weather_readings)
            display_average_readings(arg, weather_result)
    if args.extreme:
        for arg in args.extreme:
            weather_readings = filter_by_year(weather_records, arg)
            weather_result = weatherman_computations.calculate_ext_readings(
                             weather_readings)
            display_extreme_readings(arg, weather_result)
    if args.chart:
        for arg in args.chart:
            weather_readings = filter_by_month(weather_records, arg)
            for record in weather_readings:
                display_charts_of_readings([record.max_temp,
                                            record.min_temp,
                                            str(record.pkt.day)])


if __name__ == "__main__":
    main()
