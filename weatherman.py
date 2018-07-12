import os
import sys
from datetime import date
import argparse
from datetime import datetime
import csv
import glob

from weatherman_data_structure import ReadingsHolder
from weatherman_data_structure import Colors
import weatherman_computations


def parse_files(directory):
    readings = []
    for data_file in glob.iglob(directory+'*.txt'):
        with open(os.path.join(directory, data_file)) as csvfile:
            csv_reader = csv.DictReader(csvfile)
            required_features = ['Max TemperatureC', 'Min TemperatureC',
                                 'Mean TemperatureC', 'Max Humidity',
                                 ' Min Humidity', ' Mean Humidity']
            for row in csv_reader:
                if all(row[req_f] for req_f in required_features):
                    readings.append(ReadingsHolder(row))
    return readings


def print_report(report_contents, seperator):
    print(seperator.join(report_contents))


def report_generator(report_type, readings_result, report_date):
    if report_type == 'a':

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

        return results

    elif report_type == 'e':

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

        return results

    else:
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

        return results


def readings_of_year(given_date, weather_readings):
    readings_result = weatherman_computations.calculate_readings(
                      weather_readings, 'e', given_date)
    report = report_generator('e', readings_result,
                              given_date.year)
    print_report(report, '\n')


def average_of_date(given_date, weather_readings):
    readings_result = weatherman_computations.calculate_readings(
                      weather_readings, 'a', given_date)
    report = report_generator('a', readings_result, given_date)
    print_report(report, '\n')


def charts(given_date, weather_readings):
    print(f"{Colors.GREEN}\n************ Temperature chart for "
          f"{given_date.year}/{given_date.month}"
          f" ************\n{Colors.RESET}")
    for row in weather_readings:
        date_from_file = datetime.strptime(row.pkt, '%Y-%m-%d')
        if(date_from_file.year == given_date.year and
           date_from_file.month == given_date.month):
            report = report_generator('c', [row.max_temp,
                                      row.min_temp],
                                      str(date_from_file.day))
            print_report(report, ' ')


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

    readings = parse_files(args.directory_path)
    for arg in args.month:
        average_of_date(arg[0], readings)
    for arg in args.year:
        readings_of_year(arg[0], readings)
    for arg in args.chart:
        charts(arg[0], readings)


if __name__ == "__main__":
    main()
