import argparse
import calendar
import csv
import glob
import os


class Color:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    END = '\033[0m'


def show_highest_values(highest_temperature_value, highest_temperature_day, lowest_temperature_value, lowest_day,
                        max_humidity_value, humidity_day):
    yr, mn, dt =highest_temperature_day.split('-')
    highest_day =  calendar.month_name[int(mn)] + " " + dt
    print("Highest: %dC on %s" % (highest_temperature_value, highest_day))
    yr, mn, dt = lowest_day.split('-')
    lowest_day = calendar.month_name[int(mn)] + " " + dt
    print("Lowest: %dC on %s" % (lowest_temperature_value, lowest_day))
    yr, mn, dt = humidity_day.split('-')
    humidity_day = calendar.month_name[int(mn)] + " " + dt
    print("Humidity: %d%% on %s" % (max_humidity_value, humidity_day))


def calculate_highest_values(highest_temperatures_list, lowest_temperatures_list, most_humidity_list,
                             temperature_date_list):
    highest_temperature_value = max(highest_temperatures_list)
    highest_day = temperature_date_list[highest_temperatures_list.index(max(highest_temperatures_list))]
    lowest_temperature_value = min(lowest_temperatures_list)
    lowest_day = temperature_date_list[lowest_temperatures_list.index(min(lowest_temperatures_list))]
    max_humidity_value = max(most_humidity_list)
    humidity_day = temperature_date_list[most_humidity_list.index(max(most_humidity_list))]
    return \
        highest_temperature_value, highest_day, lowest_temperature_value, lowest_day, max_humidity_value, humidity_day


def show_average_values(highest_average, lowest_average, humidity_average):
    print("Highest Average: %dC" %(highest_average))
    print("Lowest Average: %dC" %(lowest_average))
    print("Average Mean Humidity: %d%%" %(humidity_average))


def calculate_average_values(highest_temperatures_list, lowest_temperatures_list_, average_humidity_list):
    highest_temperature_value = round(sum(highest_temperatures_list) / len(highest_temperatures_list), 2)
    lowest_temperature_value = round(sum(lowest_temperatures_list_) / len(lowest_temperatures_list_), 2)
    average_humidity_value = round(sum(average_humidity_list) / len(average_humidity_list), 2)
    return highest_temperature_value, lowest_temperature_value, average_humidity_value


def show_bar_charts(highest_temps, lowest_temps, header_line):
    """this function will print bar-charts of given data lists"""

    print(header_line)
    for i in range(len(highest_temps)):
        print(
            Color.PURPLE + format(i + 1, '02d') + ' ' + Color.RED + ('+' * abs(highest_temps[i])) + ' ' + Color.PURPLE
            + str(highest_temps[i]) + 'C')
        print(
            Color.PURPLE + format(i + 1, '02d') + ' ' + Color.BLUE + ('+' * abs(lowest_temps[i])) + ' ' + Color.PURPLE
            + str(lowest_temps[i]) + 'C')

    print(Color.END + header_line)
    for i in range(len(highest_temps)):
        print(Color.PURPLE + format(i + 1, '02d') + ' ' + Color.BLUE + (
            '+' * abs(lowest_temps[i])) + Color.RED + (
                  '+' * abs(highest_temps[i])) + ' ' + Color.PURPLE + str(lowest_temps[i]) + 'C - ' +
              str(highest_temps[i]) + 'C')


def add_temperatures(lowest, highest, humidity):
    lowest_temperatures.append(int(lowest) if lowest else 0)
    highest_temperatures.append(int(highest) if highest else 0)
    average_humidity.append(int(humidity) if humidity else 0)


def add_temperatures_year(lowest, highest, humidity, pkt):
    lowest_temperatures.append(int(lowest) if lowest else 1000)
    highest_temperatures.append(int(highest) if highest else 0)
    max_humidity.append(int(humidity) if humidity else 0)
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
    year, month = year_argument.split('/')
    for file in glob.glob(path_to_file+"/*" + year + "_" + calendar.month_name[int(month)][:3] + "*"):
        return os.path.join(path_to_file, file)


def date_for_charts(year_argument):
    year, month = year_argument.split('/')
    return calendar.month_name[int(month)] + " " + year


if __name__ == "__main__":

    lowest_temperatures = []
    highest_temperatures = []
    average_humidity = []
    max_humidity = []
    whole_year_dates = []
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
        for file in glob.glob(path_argument+"/*" + year_argument + "*"):
            full_file_path = os.path.join(path_argument, file)
            prepare_function_data_year(full_file_path)
        highest_temperature_value, highest_day, lowest_temperature_value, lowest_day, max_humidity_value,\
            humidity_day = calculate_highest_values(highest_temperatures, lowest_temperatures, max_humidity,
                                                    whole_year_dates)
        show_highest_values(highest_temperature_value, highest_day, lowest_temperature_value, lowest_day,
                                max_humidity_value,humidity_day)
    elif args.average_values:
        prepare_function_data(make_file_name(args.average_values[1], args.average_values[0]))
        highest_average, lowest_average, humidity_average = calculate_average_values(
            highest_temperatures, lowest_temperatures, average_humidity)
        show_average_values(highest_average,lowest_average,humidity_average)
    elif args.charts_values:
        prepare_function_data(make_file_name(args.charts_values[1], args.charts_values[0]))
        barcharts_header = date_for_charts(args.charts_values[0])
        show_bar_charts(highest_temperatures, lowest_temperatures, barcharts_header)
