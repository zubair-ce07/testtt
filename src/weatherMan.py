import argparse
import calendar
import csv
import glob
import os
from operator import attrgetter


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

    def weather_date(self):
        year, month, day = self.weather_timezone.split('-')
        return calendar.month_name[int(month)] + " " + day


def prepare_weather_man(path_to_file):
    for weather_row in read_and_filter_csv(path_to_file, is_comment, is_whitespace):
        weatherman_row = WeatherMan(weather_row['PKT'], weather_row['Max TemperatureC'],
                                    weather_row["Min TemperatureC"],
                                    weather_row['Max Humidity'], weather_row[' Mean Humidity'])
        weather_mans.append(weatherman_row)


def calculate_highest_value(weather_man):
    return max(weather_man, key=attrgetter('max_temperature')), \
           min(weather_man, key=attrgetter('min_temperature')), \
           max(weather_man, key=attrgetter('max_humidity'))


def show_highest_values(highest_temperature_obj, lowest_temperature_obj, max_humidity_obj):
    print("Highest: %dC on %s" % (highest_temperature_obj.max_temperature, highest_temperature_obj.weather_date()))
    print("Lowest: %dC on %s" % (lowest_temperature_obj.min_temperature, lowest_temperature_obj.weather_date()))
    print("Humidity: %d%% on %s" % (max_humidity_obj.max_humidity, highest_temperature_obj.weather_date()))


def calculate_average_value(weather_mans):
    temperature_count = len(weather_mans)
    highest_temperature_value = round(sum(weatherman.max_temperature for weatherman in weather_mans)
                                      / temperature_count, 2)
    lowest_temperature_value = round(sum(weatherman.min_temperature for weatherman in weather_mans)
                                     / temperature_count, 2)
    average_humidity_value = round(sum(weatherman.average_humididty for weatherman in weather_mans)
                                   / temperature_count, 2)
    return highest_temperature_value, lowest_temperature_value, average_humidity_value


def show_average_values(highest_average, lowest_average, humidity_average):
    print("Highest Average: %dC" % highest_average)
    print("Lowest Average: %dC" % lowest_average)
    print("Average Mean Humidity: %d%%" % humidity_average)


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


def iterate_filtered(in_file, *filters):
    for line in in_file:
        if not any(user_filter(line) for user_filter in filters):
            yield line


def read_and_filter_csv(csv_path, *filters):
    with open(csv_path) as fin:
        iterate_clean_lines = iterate_filtered(fin, *filters)
        weather_reader = csv.DictReader(iterate_clean_lines)
        return [weather_row for weather_row in weather_reader]


def make_file_name(path_to_file, year_argument):
    year, month = year_argument.split('/')
    for file in glob.glob(path_to_file + "/*" + year + "_" + calendar.month_name[int(month)][:3] + "*"):
        return os.path.join(path_to_file, file)


def dateheader_for_charts(year_argument):
    year, month = year_argument.split('/')
    return calendar.month_name[int(month)] + " " + year


if __name__ == "__main__":

    weather_mans = []
    parser = argparse.ArgumentParser(description="File Arguments")

    parser.add_argument("-e", nargs=2, action="store",
                        dest="highest_values",
                        help="year and file name to display highest values")

    parser.add_argument("-a", nargs=2, action="store",
                        dest="average_values",
                        help="year and file name to display average values")

    parser.add_argument("-c", nargs=2, action="store",
                        dest="charts_values",
                        help="year and file name to display charts")

    args = parser.parse_args()
    if args.highest_values:
        path_argument = args.highest_values[1]
        year_argument = args.highest_values[0]

        for file in glob.glob(path_argument + "/*" + year_argument + "*"):
            full_file_path = os.path.join(path_argument, file)
            prepare_weather_man(full_file_path)

        max_temp_obj, min_temp_obj, max_humidity_obj = calculate_highest_value(weather_mans)
        show_highest_values(max_temp_obj, min_temp_obj, max_humidity_obj)

    elif args.average_values:
        prepare_weather_man(make_file_name(args.average_values[1], args.average_values[0]))
        highest_average, lowest_average, humidity_average = calculate_average_value(weather_mans)
        show_average_values(highest_average, lowest_average, humidity_average)

    elif args.charts_values:
        prepare_weather_man(make_file_name(args.charts_values[1], args.charts_values[0]))
        barcharts_header = dateheader_for_charts(args.charts_values[0])
        show_bar_chart(weather_mans, barcharts_header)
