import os
import argparse
import csv
import glob
from datetime import datetime

from weatherman_data_structure import ReadingsHolder
from weatherman_data_structure import Colors
import weatherman_computations


def parse_files(directory):
    readings = []
    required_features = ['Max TemperatureC', 'Min TemperatureC',
                         'Mean TemperatureC', 'Max Humidity',
                         ' Min Humidity', ' Mean Humidity']
    for data_file in glob.iglob(directory+'*.txt'):
        with open(os.path.join(directory, data_file)) as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                if all(row[req_f] for req_f in required_features):
                    readings.append(ReadingsHolder(row))
    return readings


def average_report_generator(readings_result, report_date):
    header = f"{Colors.GREEN}\n{'*' * 12}Average Readings of "\
             f"{report_date} {'*' * 12}\n{Colors.RESET}"

    highest_avg = f"Highest Average: {readings_result.max_mean_temp}C"
    lowest_average = f"Lowest Average: {readings_result.min_mean_temp}C"
    mean_humidity = f"Average Mean Humidity: "\
        f"{int(readings_result.average_mean_humidity)}%\n"

    results = [
        header,
        highest_avg,
        lowest_average,
        mean_humidity
    ]

    print('\n'.join(results))


def extreme_report_generator(readings_result, report_date):
    header = f"{Colors.GREEN}\n{'*' * 12} Extreme Readings of "\
             f"{report_date} {'*' * 12}\n{Colors.RESET}"

    highest = f"Highest: {readings_result.maximum_temp}"\
        f"C on {readings_result.maximum_temp_day}"

    lowest = f"Lowest: {readings_result.minimum_temp}C on "\
        f"{readings_result.minimum_temp_day}"

    humidity = f"Humidity: {readings_result.maximum_humidity}% on "\
        f"{readings_result.maximum_humidity_day}"

    results = [
        header,
        highest,
        lowest,
        humidity
    ]

    print('\n'.join(results))


def charts_report_generator(readings_result, report_date):
    day = f"{Colors.MAGENTA}{int(report_date)}"
    symbols = f"{Colors.BLUE}{'+' * int(readings_result[1])}"\
        f"{Colors.RED}{'+' * int(readings_result[0])}"
    min_temp = f"{Colors.MAGENTA} {int(readings_result[1])}C - "
    max_temp = f"{int(readings_result[0])}C{Colors.RESET}"

    results = [
        day,
        symbols,
        min_temp,
        max_temp
    ]

    print(' '.join(results))


def get_extreme_of_readings(given_date, weather_readings):
    readings_result = weatherman_computations.calculate_extreme_readings(
                      weather_readings, given_date)
    extreme_report_generator(readings_result,
                             given_date.year)


def get_average_of_readings(given_date, weather_readings):
    readings_result = weatherman_computations.calculate_average_readings(
                      weather_readings, given_date)
    average_report_generator(readings_result,
                             given_date.strftime("%Y/%m"))


def get_charts_of_readings(given_date, weather_readings):
    print(f"{Colors.GREEN}\n************ Temperature chart for "
          f"{given_date.year}/{given_date.month}"
          f" ************\n{Colors.RESET}")
    for reading in weather_readings:
        date_from_file = reading.pkt
        if(date_from_file.year == given_date.year and
           date_from_file.month == given_date.month):
            charts_report_generator([reading.max_temp,
                                     reading.min_temp],
                                    str(date_from_file.day))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("directory_path", type=str,
                        help="Path to the directory containing data files")
    parser.add_argument("-a", "--month", type=lambda m:
                        datetime.strptime(m, '%Y/%m'),
                        action='append', nargs='*', default=[])
    parser.add_argument("-e", "--year", type=lambda y:
                        datetime.strptime(y, '%Y'),
                        action='append', nargs='*', default=[])
    parser.add_argument("-c", "--chart", type=lambda c:
                        datetime.strptime(c, '%Y/%m'),
                        action='append', nargs='*', default=[])
    args = parser.parse_args()
    directory_path = args.directory_path+"/"
    if directory_path.startswith('.'):
        abs_path = os.path.abspath(os.path.dirname(__file__))
        directory_path = abs_path + directory_path.strip(".")
    readings = parse_files(directory_path)
    for arg in args.month:
        get_average_of_readings(arg[0], readings)
    for arg in args.year:
        get_extreme_of_readings(arg[0], readings)
    for arg in args.chart:
        get_charts_of_readings(arg[0], readings)


if __name__ == "__main__":
    main()
