import argparse
import calendar
import csv
import glob
import os
from operator import attrgetter
from datetime import datetime


class Color:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    END = '\033[0m'


class WeatherMan:
    def __init__(self, weather_timezone, max_temperature, min_temperature, max_humidity, average_humididty):
        self.weather_timezone = weather_timezone
        self.max_temperature = int(max_temperature) if max_temperature else 0
        self.min_temperature = int(min_temperature) if min_temperature else 0
        self.max_humidity = int(max_humidity) if max_humidity else 0
        self.average_humididty = int(average_humididty) if average_humididty else 0

    def show_month_name_and_date(self):
        year, month, day = self.weather_timezone.split('-')
        return calendar.month_name[int(month)] + " " + day


def prepare_weather_man(path_to_file):
    for weather_row in read_and_filter_csv_file(path_to_file, is_comment, is_whitespace):
        weatherman_row = WeatherMan(weather_row['PKT'] or weather_row['PKST'], weather_row['Max TemperatureC'],
                                    weather_row["Min TemperatureC"],
                                    weather_row['Max Humidity'], weather_row[' Mean Humidity'])
        weather_records.append(weatherman_row)
    return weather_records


def calculate_yearly_report(weather_man):
    return max(weather_man, key=attrgetter('max_temperature')), \
           min(weather_man, key=attrgetter('min_temperature')), \
           max(weather_man, key=attrgetter('max_humidity'))


def show_yearly_report(highest_temperature_obj, lowest_temperature_obj, max_humidity_obj):
    print(f'Highest: {highest_temperature_obj.max_temperature}C on '
          f'{highest_temperature_obj.show_month_name_and_date()}')
    print(f'Lowest: {lowest_temperature_obj.min_temperature}C on {lowest_temperature_obj.show_month_name_and_date()}')
    print(f'Humidity: {max_humidity_obj.max_humidity}% on {highest_temperature_obj.show_month_name_and_date()}')


def calculate_monthly_report(weather_records):
    temperature_count = len(weather_records)
    highest_temperature_value = round(sum(weatherman.max_temperature for weatherman in weather_records)
                                      / temperature_count, 2)
    lowest_temperature_value = round(sum(weatherman.min_temperature for weatherman in weather_records)
                                     / temperature_count, 2)
    average_humidity_value = round(sum(weatherman.average_humididty for weatherman in weather_records)
                                   / temperature_count, 2)
    return highest_temperature_value, lowest_temperature_value, average_humidity_value


def show_monthly_report(highest_average, lowest_average, humidity_average):
    print(f'Highest Average: {highest_average}C')
    print(f'Lowest Average: {lowest_average}C')
    print(f'Average Mean Humidity: {humidity_average}%')


def show_bar_chart(weather_man, header_line):
    print(header_line)
    for day_count, weather_row in enumerate(weather_man):
        print(
            Color.PURPLE + format(day_count + 1, '02d') + ' ' + Color.RED + (
                '+' * abs(weather_row.max_temperature)) + ' ' + Color.PURPLE
            + str(weather_row.max_temperature) + 'C')
        print(
            Color.PURPLE + format(day_count + 1, '02d') + ' ' + Color.BLUE + (
                '+' * abs(weather_row.min_temperature)) + ' ' + Color.PURPLE
            + str(weather_row.min_temperature) + 'C')

    print(Color.END + header_line)
    for day_count, weather_row in enumerate(weather_man):
        print(Color.PURPLE + format(day_count + 1, '02d') + ' ' + Color.BLUE + ('+' * abs(weather_row.min_temperature))
              + Color.RED + ('+' * abs(weather_row.max_temperature)) + ' ' + Color.PURPLE +
              str(weather_row.min_temperature) + 'C - ' + str(weather_row.max_temperature) + 'C')


def is_comment(line):
    return line.startswith('<')


def is_whitespace(line):
    return line.isspace()


def iterate_filtered(input_file, *filters):
    for line in input_file:
        if not any(user_filter(line) for user_filter in filters):
            yield line


def read_and_filter_csv_file(csv_path, *filters):
    with open(csv_path) as input_file:
        iterate_clean_lines = iterate_filtered(input_file, *filters)
        weather_reader = csv.DictReader(iterate_clean_lines)
        return [weather_row for weather_row in weather_reader]


def make_file_name(path_to_file, year_argument):
    for input_file in glob.glob(path_to_file + "/*" + str(year_argument.year) + "_" +
                                calendar.month_name[int(year_argument.month)][:3] + "*"):
        return os.path.join(path_to_file, input_file)


def date_header_for_charts(year_argument):
    return calendar.month_name[int(year_argument.month)] + " " + str(year_argument.year)


def main():
    weather_records = []

    parser = argparse.ArgumentParser(description="Enter Arguments")

    parser.add_argument('path', help='path of directory')
    parser.add_argument("-e", action="store", dest="yearly_report", help="year of show highest and lowest values ",
                        type=lambda x: datetime.strptime(x, '%Y'))

    parser.add_argument("-a", action="store", dest="monthly_report", help="year and month to show average values",
                        type=lambda x: datetime.strptime(x, '%Y/%m'))

    parser.add_argument("-c", action="store", dest="horizontol_charts",
                        help="year and month to display horizontol charts",
                        type=lambda x: datetime.strptime(x, '%Y/%m'))

    args = parser.parse_args()
    if args.yearly_report:
        for input_file in glob.glob(args.path + "/*" + str(args.yearly_report.year) + "*"):
            full_file_path = os.path.join(args.path, input_file)
            weather_records = prepare_weather_man(full_file_path)

        max_temp, min_temp, max_humidity = calculate_yearly_report(weather_records)
        show_yearly_report(max_temp, min_temp, max_humidity)

    elif args.monthly_report:
        prepare_weather_man(make_file_name(args.path, args.monthly_report))
        highest_average, lowest_average, humidity_average = calculate_monthly_report(weather_records)
        show_monthly_report(highest_average, lowest_average, humidity_average)

    elif args.horizontol_charts:
        prepare_weather_man(make_file_name(args.path, args.horizontol_charts))
        bar_charts_header = date_header_for_charts(args.horizontol_charts)
        show_bar_chart(weather_records, bar_charts_header)


if __name__ == "__main__":
    main()
