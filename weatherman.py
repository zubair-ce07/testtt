import os
import sys
from datetime import date
import argparse
from datetime import datetime
import csv
import glob
from weatherman_data_structure import readings_holder
from weatherman_data_structure import colors
import weatherman_computations


def parse_files(directory):
    readings = []
    for file in glob.iglob(directory+'*.txt'):
        with open(os.path.join(directory, file)) as csvfile:
            csv_reader = csv.DictReader(csvfile)
            required_features = ['Max TemperatureC', 'Min TemperatureC',
                                 'Mean TemperatureC', 'Max Humidity',
                                 ' Min Humidity', ' Mean Humidity']
            for row in csv_reader:
                data = list(row[i] for i in required_features)
                if '' not in data:
                    readings.append(readings_holder(row))
    return readings


def report_generator(report_type, max_temp, min_temp, humidity, max_temp_day,
                     min_temp_day, humidity_day, date):
    if report_type == 'a':
        print(f"{colors.GREEN}\n************ Average Readings of {date} "
              f"************\n\n{colors.RESET}"
              f"Highest Average: {max_temp}C\nLowest Average: "
              f"{min_temp}C\nAverage Mean Humidity: "
              f"{int(humidity)}%\n")
    elif report_type == 'e':
        print(f"{colors.GREEN}\n************ Extreme Readings of {date} "
              f"************\n\n{colors.RESET}"
              f"Highest: {max_temp}C on {max_temp_day}"
              f"\nLowest: {min_temp}C on"
              f"{min_temp_day}\nHumidity: "
              f"{humidity}% on {humidity_day}\n")
    else:
        print (f"{colors.MAGENTA}{int(date)} {colors.BLUE}"
               f"{'+' * int(min_temp)}{colors.RED}{'+' * int(max_temp)}"
               f"{colors.MAGENTA} {int(min_temp)}C - "
               f"{int(max_temp)}C{colors.RESET}")


def readings_of_year(year_, readings):
    year = str(year_.year)
    results = weatherman_computations.calculate(readings, 'e', year, '')
    report_generator('e', results.maximum_temperature,
                     results.minimum_temperature, results.maximum_humidity,
                     results.maximum_temperature_day,
                     results.minimum_temperature_day,
                     results.maximum_humidity_day, year)


def average_of_date(date, readings):
    year, month = str(date.year), str(date.month)
    results = weatherman_computations.calculate(readings, 'a', year, month)
    report_generator('a', results.max_mean_temperature,
                     results.min_mean_temperature,
                     results.average_mean_humidity, '', '', '', year+"/"+month)


def charts(month_, readings):
    year, month = str(month_.year), str(month_.month)
    print(f"{colors.GREEN}\n************ Temperature chart for {year}/{month}"
          f" ************\n{colors.RESET}")
    for row in readings:
        if(row.pkt.split("-")[0] == year and row.pkt.split("-")[1] == month):
            report_generator('c', row.max_temp, row.min_temp, '', '', '', '',
                             row.pkt.split("-")[2])


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
