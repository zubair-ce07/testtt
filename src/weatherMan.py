import argparse
import calendar
import csv
import glob
import os


class color:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    END = '\033[0m'


lowest_temperatures = []
highest_temperatures = []
average_humidity = []
max_humidity = []
whole_year_dates = []


def show_highest_values(highest_temperature_value, highest_temperature_day, lowest_temperature_value, lowest_day,
                        max_humidity_value, humidity_day):
    print("Highest: " + highest_temperature_value + "C on " + highest_temperature_day)
    print("Lowest: " + lowest_temperature_value + "C on " + lowest_day)
    print("Humidity: " + max_humidity_value + "% on " + humidity_day)


def calculate_highest_values(highest_temperatures_list, lowest_temperatures_list, most_humidity_list,
                             temperature_date_list):
    highest_temperature_value = max(highest_temperatures_list)
    yr, mn, dt = temperature_date_list[highest_temperatures_list.index(max(highest_temperatures_list))].split('-')
    highest_day = calendar.month_name[int(mn)] + " " + dt
    lowest_temperature_value = min(lowest_temperatures_list)
    yr, mn, dt = temperature_date_list[lowest_temperatures_list.index(min(lowest_temperatures_list))].split('-')
    lowest_day = calendar.month_name[int(mn)] + " " + dt
    max_humidity_value = max(most_humidity_list)
    yr, mn, dt = temperature_date_list[most_humidity_list.index(max(most_humidity_list))].split('-')
    humidity_day = calendar.month_name[int(mn)] + " " + dt
    show_highest_values(str(highest_temperature_value), highest_day, str(lowest_temperature_value), lowest_day,
                        str(max_humidity_value), humidity_day)


def show_average_values(highest_average, lowest_average, humidity_average):
    print("Highest Average: " + highest_average + "C")
    print("Lowest Average: " + lowest_average + "C")
    print("Average Mean Humidity: " + humidity_average + "%")


def calculate_average_values(highest_temperatures_list, lowest_temperatures_list_, average_humidity_list):
    highest_temperature_value = str(round(sum(highest_temperatures_list) / len(highest_temperatures_list), 2))
    lowest_temperature_value = str(round(sum(lowest_temperatures_list_) / len(lowest_temperatures_list_), 2))
    average_humidity_value = str(round(sum(average_humidity_list) / len(average_humidity_list), 2))
    show_average_values(highest_temperature_value, lowest_temperature_value, average_humidity_value)


def show_bar_charts(highest_temps, lowest_temps, header_line):
    """this function will print bar-charts of given data lists"""

    print(header_line)
    for i in range(len(highest_temps)):
        print(
            color.PURPLE + format(i + 1, '02d') + ' ' + color.RED + ('+' * abs(highest_temps[i])) + ' ' + color.PURPLE
            + str(highest_temps[i]) + 'C')
        print(
            color.PURPLE + format(i + 1, '02d') + ' ' + color.BLUE + ('+' * abs(lowest_temps[i])) + ' ' + color.PURPLE
            + str(lowest_temps[i]) + 'C')

    print(color.END + header_line)
    for i in range(len(highest_temps)):
        print(color.PURPLE + format(i + 1, '02d') + ' ' + color.BLUE + (
            '+' * abs(lowest_temps[i])) + color.RED + (
                  '+' * abs(highest_temps[i])) + ' ' + color.PURPLE + str(lowest_temps[i]) + 'C - ' +
              str(highest_temps[i]) + 'C')


def add_temperatures(lowest, highest, humidity):
    lowest_temperatures.append(int(lowest) if lowest != '' else 0)
    highest_temperatures.append(int(highest) if highest != '' else 0)
    average_humidity.append(int(humidity) if humidity != '' else 0)


def add_temperatures_year(lowest, highest, humidity, pkt):
    lowest_temperatures.append(int(lowest) if lowest != '' else 1000)
    highest_temperatures.append(int(highest) if highest != '' else 0)
    max_humidity.append(int(humidity) if humidity != '' else 0)
    whole_year_dates.append(pkt)


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


def prepare_function_data(path_to_file):
    for weather_row in read_and_filter_csv(path_to_file, is_comment, is_whitespace):
        add_temperatures(weather_row["Min TemperatureC"], weather_row['Max TemperatureC'],
                         weather_row[' Mean Humidity'])


def prepare_function_data_year(path_to_file):
    for weather_row in read_and_filter_csv(path_to_file, is_comment, is_whitespace):
        add_temperatures_year(weather_row["Min TemperatureC"], weather_row['Max TemperatureC'],
                              weather_row['Max Humidity'], weather_row['PKT'])


def make_file_name(path_to_file, year_argument):
    os.chdir(path_to_file)
    for file in glob.glob("*" + year_argument[:4] + "_" + calendar.month_name[int(year_argument[5:])][:3] + "*"):
        return os.path.join(path_to_file, file)


def date_for_charts(year_argument):
    return calendar.month_name[int(year_argument[0][5:])] + " " + year_argument[0][:4]


if __name__ == "__main__":

    # parser = argparse.ArgumentParser()
    # parser.add_argument('-e', help='input arguments')
    # parser.add_argument('year')
    # parser.add_argument('filename', nargs='?')
    #
    # args = parser.parse_args()

    highest_values = ''
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
        os.chdir(path_argument)
        for file in glob.glob("*" + year_argument + "*"):
            full_file_path = os.path.join(path_argument, file)
            prepare_function_data_year(full_file_path)
        calculate_highest_values(highest_temperatures, lowest_temperatures, max_humidity, whole_year_dates)
    elif args.average_values:
        prepare_function_data(make_file_name(args.average_values[1], args.average_values[0]))
        calculate_average_values(highest_temperatures, lowest_temperatures, average_humidity)
    elif args.charts_values:
        prepare_function_data(make_file_name(args.charts_values[1], args.charts_values[0]))
        barcharts_header = date_for_charts(args.charts_values[0])
        show_bar_charts(highest_temperatures, lowest_temperatures, barcharts_header)
