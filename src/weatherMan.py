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


class WeatherManData:
    def __init__(self, pkt, max_temperature, min_temperature, max_humidity, average_humididty):
        self.pkt = pkt
        self.max_temperature = int(max_temperature) if max_temperature else 0
        self.min_temperature = int(min_temperature) if min_temperature else 0
        self.max_humidity = int(max_humidity) if max_humidity else 0
        self.average_humididty = int(average_humididty) if average_humididty else 0

    def weather_date(self):
        year, month, day = self.pkt.split('-')
        return calendar.month_name[int(month)] + " " + day


def prepare_function_data(path_to_file):
    for weather_row in read_and_filter_csv(path_to_file, is_comment, is_whitespace):
        new_data = WeatherManData(weather_row['PKT'], weather_row['Max TemperatureC'], weather_row["Min TemperatureC"],
                                  weather_row['Max Humidity'], weather_row[' Mean Humidity'])
        weather_data.append(new_data)


def calculate_highest_value(weather_data_list):
    return max(weather_data_list, key=attrgetter('max_temperature')), \
           min(weather_data_list, key=attrgetter('min_temperature')), \
           max(weather_data_list, key=attrgetter('max_humidity'))


def show_highest_values(highest_temperature_obj, lowest_temperature_obj, max_humidity_obj):
    print("Highest: %dC on %s" % (highest_temperature_obj.max_temperature, highest_temperature_obj.weather_date()))
    print("Lowest: %dC on %s" % (lowest_temperature_obj.min_temperature, lowest_temperature_obj.weather_date()))
    print("Humidity: %d%% on %s" % (max_humidity_obj.max_humidity, highest_temperature_obj.weather_date()))


def calculate_average_value(weather_data_list):
    length_of_list = len(weather_data_list)
    highest_temperature_value = round(sum(obj.max_temperature for obj in weather_data_list)
                                      / length_of_list, 2)
    lowest_temperature_value = round(sum(obj.min_temperature for obj in weather_data_list)
                                     / length_of_list, 2)
    average_humidity_value = round(sum(obj.average_humididty for obj in weather_data_list)
                                   / length_of_list, 2)
    return highest_temperature_value, lowest_temperature_value, average_humidity_value


def show_average_values(highest_average, lowest_average, humidity_average):
    print("Highest Average: %dC" % highest_average)
    print("Lowest Average: %dC" % lowest_average)
    print("Average Mean Humidity: %d%%" % humidity_average)


def show_bar_chart(weather_data_list, header_line):
    """this function will print bar-charts of given data lists"""

    print(header_line)
    for i, data in enumerate(weather_data_list):
        print(
            Color.PURPLE + format(i + 1, '02d') + ' ' + Color.RED + (
                '+' * abs(data.max_temperature)) + ' ' + Color.PURPLE
            + str(data.max_temperature) + 'C')
        print(
            Color.PURPLE + format(i + 1, '02d') + ' ' + Color.BLUE + (
                '+' * abs(data.min_temperature)) + ' ' + Color.PURPLE
            + str(data.min_temperature) + 'C')

    print(Color.END + header_line)
    for j, data in enumerate(weather_data_list):
        print(Color.PURPLE + format(j + 1, '02d') + ' ' + Color.BLUE + ('+' * abs(data.min_temperature))
              + Color.RED + ('+' * abs(data.max_temperature)) + ' ' + Color.PURPLE +
              str(data.min_temperature) + 'C - ' + str(data.max_temperature) + 'C')


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
        reader = csv.DictReader(iterate_clean_lines)
        return [data_row for data_row in reader]


def make_file_name(path_to_file, year_argument):
    year, month = year_argument.split('/')
    for file in glob.glob(path_to_file + "/*" + year + "_" + calendar.month_name[int(month)][:3] + "*"):
        return os.path.join(path_to_file, file)


def date_for_charts(year_argument):
    year, month = year_argument.split('/')
    return calendar.month_name[int(month)] + " " + year


if __name__ == "__main__":

    weather_data = []
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
            prepare_function_data(full_file_path)
        max_temp_obj, min_temp_obj, max_humidity_obj = calculate_highest_value(weather_data)
        show_highest_values(max_temp_obj, min_temp_obj, max_humidity_obj)
    elif args.average_values:
        prepare_function_data(make_file_name(args.average_values[1], args.average_values[0]))
        highest_average, lowest_average, humidity_average = calculate_average_value(weather_data)
        show_average_values(highest_average, lowest_average, humidity_average)
    elif args.charts_values:
        prepare_function_data(make_file_name(args.charts_values[1], args.charts_values[0]))
        barcharts_header = date_for_charts(args.charts_values[0])
        show_bar_chart(weather_data, barcharts_header)
