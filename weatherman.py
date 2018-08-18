"""
Main module which runs the whole weatherman program, It takes Command Line Args to work with

Command Line Args:
'-e' : Gives highest, lowest temperatures and highest humidity
'-a' : Gives average temperature and humidity
'-c' : Gives results in the chart/graph form
'-r' : Gives results in chart form but 1 day has only 1 graph showing range of temperature
"""

import os
from datetime import datetime

import csv
import argparse
import re
from termcolor import colored


def get_month_str(index):
    months = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',
        6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
        11: 'Nov', 12: 'Dec',
    }
    if index in months:
        return months[index]
    else:
        return '(.*)'


def applying_arguments():
    """Create Command Line Argument List"""
    parser_arg = argparse.ArgumentParser()
    parser_arg.add_argument("directory", help="you have to specify a directory for records")
    parser_arg.add_argument("-e", "--extreme", help="Show extreme records of specified date")
    parser_arg.add_argument("-a", "--average", help="Show average records of specified date")
    parser_arg.add_argument("-c", "--chart", help="Show horizontal bar chart of specified date")
    parser_arg.add_argument("-r", "--range_chart", help="Show temperature range chart of specified date")
    return parser_arg.parse_args()


def parser(time_span):
    """This is the main function of this module, it takes directory and date to work on and in return
    it gives a list of records from the directory related to the specified dates"""

    year, month, day = separate_combined_date(time_span)
    files = get_required_files(year, month)
    # If records found
    if len(files) > 0:
        # reads all the files and get records in a list
        return collect_data_from_files(files, day)
    else:
        return None


def get_required_files(required_year, required_month):
    """This function takes directory, year and month to choose those files from it which are required"""

    month_str = get_month_str(required_month)
    search_pattern = f'r(.{str(required_year)})_{month_str}.txt'
    matches = []
    for file_name in os.listdir():
        if re.compile(search_pattern).search(file_name):
            matches.append(file_name)
    return matches


def collect_data_from_files(files, day=None):
    """It takes path of directory with names of files as arguments
     and returns Structured Data in the form of list"""

    csv.register_dialect('space_eliminator', delimiter=',', skipinitialspace=True)
    weather_records = []

    for file in files:
        records = csv.DictReader(open(file, 'r'), dialect='space_eliminator')
        if day:
            for index, record in enumerate(records):
                if index == day - 1:
                    weather_records.append(record)

                    return weather_records
        weather_records.append(records)

    return weather_records


# Calculation Module
def display_extreme(time_span, data_set):
    """Takes TimeSpan and Data Records to show extreme cases of temperature present in records"""
    high_temp, low_temp, humidity, high_temp_date, low_temp_date, humidity_date \
        = calculate_extreme_temperature_dates_values(data_set)

    # Printing the end results
    print(f"{string_to_date(time_span)}")
    print(f"Highest : {high_temp}C on {high_temp_date}")
    print(f"Lowest : {low_temp}C on {low_temp_date}")
    print(f"Humidity : {humidity}% on {humidity_date}")


def calculate_extreme_temperature_dates_values(data_set):
    """Takes list of data and returns extreme conditions and occurrence dates"""

    if isinstance(data_set[0], csv.DictReader):
        for data in data_set:
            for row in data:
                high_temp = -100
                low_temp = 200
                humidity = -1

                high_temp, low_temp, humidity, high_temp_date, low_temp_date, humidity_date \
                    = calculate_extreme_temp(row, high_temp, low_temp, humidity)
    else:
        high_temp, low_temp, humidity, high_temp_date, low_temp_date, humidity_date \
            = calculate_extreme_temp(data_set[0])

    high_temp_date = date_format_converter(high_temp_date)
    low_temp_date = date_format_converter(low_temp_date)
    humidity_date = date_format_converter(humidity_date)

    return high_temp, low_temp, humidity, high_temp_date, low_temp_date, humidity_date


def calculate_extreme_temp(row, high_temp=None, low_temp=None, humidity=None):
    """Compares results with other records"""
    # Max Temperature Check
    if row['Max TemperatureC'] and (not high_temp or high_temp < int(row['Max TemperatureC'])):
        high_temp_date = row['PKT']
        high_temp = int(row['Max TemperatureC'])

    # Min Temperature Check
    if row['Min TemperatureC'] and (not low_temp or low_temp > int(row['Min TemperatureC'])):
        low_temp_date = row['PKT']
        low_temp = int(row['Min TemperatureC'])

    # Humidity Check
    if row['Max Humidity'] and (not humidity or humidity < int(row['Max Humidity'])):
        humidity = int(row['Max Humidity'])
        humidity_date = row['PKT']

    return high_temp, low_temp, humidity, high_temp_date, low_temp_date, humidity_date


def display_avg(time_span, data_set):
    """Takes TimeSpan and Data Records to show average temperature according to records"""

    # Calculates Averages
    high_avg, low_avg, humid_avg = calculate_avg_temperature(data_set)

    # Printing the end results
    print(f"{string_to_date(time_span)}")
    print(f"Highest Temperature Average : {high_avg: .0f}C")
    print(f"Lowest Temperature Average : {low_avg: .0f}C")
    print(f"Mean Humidity Average : {humid_avg: .2f}%")


def calculate_avg_temperature(data_set, high_temp_avg=0, low_temp_avg=0, humidity_avg=0,
                              high_temp_days=0, low_temp_days=0, humidity_days=0):
    """Takes List of Data and Calculates Averages"""

    for data in data_set:
        for row in data:

            if row['Max TemperatureC']:
                high_temp_avg += int(row['Max TemperatureC'])
                high_temp_days += 1

            if row['Min TemperatureC']:
                low_temp_avg += int(row['Min TemperatureC'])
                low_temp_days += 1

            if row['Mean Humidity']:
                humidity_avg += int(row['Mean Humidity'])
                humidity_days += 1

    high_avg = high_temp_avg / high_temp_days
    low_avg = low_temp_avg / low_temp_days
    humid_avg = humidity_avg / humidity_days

    return high_avg, low_avg, humid_avg


def display_chart(time_span, data_set):
    """Takes TimeSpan and Data Records to show Each Day's Chart regarding highest and lowest temperatures"""

    print(f"{string_to_date(time_span)}")
    for num, data in enumerate(data_set):
        for row in data:
            # Showing Max Temp Results
            if row['Max TemperatureC']:
                colored_single_print(num + 1, int(row['Max TemperatureC']), 'red')

            # Showing Min Temp Results
            if row['Min TemperatureC']:
                colored_single_print(num + 1, int(row['Min TemperatureC']), 'blue')


def colored_single_print(num, count, color):
    print(num, end=" ")
    for i in range(count):
        print(colored('+', color), end='')
    print(f" {count: .0f}C")


def colored_double_print(num, max_count, min_count, max_color, min_color):
    print(num, end=" ")
    for i in range(min_count):
        print(colored('+', min_color), end='')
    for i in range(max_count):
        print(colored('+', max_color), end='')

    print(f"{min_count: .0f}C - {max_count: .0f}C")


def display_range_chart(time_span, data_set):
    """Takes TimeSpan and Data Records to show Range of Temperature each Day"""

    # Printing the end results
    print(f"{string_to_date(time_span)}")

    for num, data in enumerate(data_set):
        for row in data:
            if row['Max TemperatureC'] and row['Min TemperatureC']:
                colored_double_print(num + 1, int(row['Max TemperatureC']), int(row['Min TemperatureC']), 'red', 'blue')


def string_to_date(time_span, delimeter='/'):
    """Here we parse given date in string format to get a well formatted Date pattern (String to Date)"""

    year_required, month_required, day_required = separate_combined_date(time_span, delimeter)
    if not month_required and not day_required:
        return datetime(year_required, 1, 1, 0, 0)

    elif not day_required:
        return datetime(year_required, month_required, 1, 0, 0)

    else:
        return datetime(year_required, month_required, day_required, 0, 0)


def date_format_converter(date):
    """Here we parse given date to get a well formatted Date pattern (Date to Date) """
    date = string_to_date(date, '-')
    return datetime(date.year, date.month, date.day, 0, 0).strftime('%B %Y')


def separate_combined_date(commandline_dates, delimeter='/'):
    """It takes date in YYYY/MM/DD foramt and Returns the Accurate information
     of date by splitting it in Year, Month and Day"""

    # User can give year, month and day separated by '/', so here we split them
    splitted_date = commandline_dates.split(delimeter)
    try:
        if len(splitted_date) == 3:
            return int(splitted_date[0]), int(splitted_date[1]), int(splitted_date[2])
        elif len(splitted_date) == 2:
            return int(splitted_date[0]), int(splitted_date[1]), None
        elif len(splitted_date) == 1:
            return int(splitted_date[0]), None, None
        else:
            return None, None, None

    except TypeError:
        raise TypeError


def main_function():
    """Takes system args and extract options and time to iterate the whole process over it"""

    function_specifier = {
        'extreme': display_extreme,
        'average': display_avg,
        'chart': display_chart,
        'range_chart': display_range_chart,
    }

    args = applying_arguments()
    os.chdir(args.directory)

    for arg in vars(args):
        attribute_val = getattr(args, arg)
        if attribute_val and arg != "directory":
            data_set = parser(attribute_val)
            if data_set:
                function_specifier[arg](attribute_val, data_set)


if __name__ == "__main__":
    main_function()
