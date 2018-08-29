"""
Main module which runs the whole weatherman program, It takes Command Line Args to work with

Command Line Args:
'-e' : Gives highest, lowest temperatures and highest humidity
'-a' : Gives average temperature and humidity
'-c' : Gives results in the chart/graph form
'-r' : Gives results in chart form but 1 day has only 1 graph showing range of temperature
"""

import os
import datetime

import csv
import argparse
import re
from termcolor import colored


def get_month_name(index):
    """Takes a number to return its month"""
    months = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',
        6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
        11: 'Nov', 12: 'Dec',
    }

    return months.get(index)


def applying_commandline_arguments():
    """Create Command Line Argument List"""
    parser_arg = argparse.ArgumentParser()
    parser_arg.add_argument("directory", help="you have to specify a directory for records")
    parser_arg.add_argument("-e", "--extreme", help="Show extreme records of specified date")
    parser_arg.add_argument("-a", "--average", help="Show average records of specified date")
    parser_arg.add_argument("-c", "--chart", help="Show horizontal bar chart of specified date")
    parser_arg.add_argument("-r", "--range_chart", help="Show temperature range chart of specified date")
    return parser_arg.parse_args()


def parser(time_span):
    """
    This is the main function of this module, it takes directory and date to work on and in return
    it gives a list of records from the directory related to the specified dates, if no data found
    it wil return none
    """

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

    month_name = get_month_name(required_month)

    # if month is not defined, we have to use wildcard for regex string matching
    if not month_name:
        month_name = "(.*)"
    search_pattern = f'r(.{str(required_year)})_{month_name}.txt'

    matches = []
    for file_name in os.listdir():
        if re.compile(search_pattern).search(file_name):
            matches.append(file_name)
    return matches


def collect_data_from_files(files, day=None):
    """It takes path of directory with names of files as arguments
     and returns Structured Data in the form of list"""

    # Registering dialect to skip spaces in names of dictionary
    csv.register_dialect('space_eliminator', delimiter=',', skipinitialspace=True)

    weather_records = []

    for file in files:
        records = csv.DictReader(open(file, 'r'), dialect='space_eliminator')

        for index, record in enumerate(records):
            '''
            Each month-file contains list of day's records, when the user specifies a day along with
            year and month, we have to skip all the records from list => except the required day
            
            The csv.DictReader doesn't give us a subscriptable object (means we can't use indexing with such object)
            So we still have to iterate over the object and then extract the day which user defined through
            commandline
            '''
            if not day:
                weather_records.append(record)
            elif index == day - 1:
                weather_records.append(record)

    return weather_records


# Calculation Module
def display_extreme(time_span, data_set):
    """Takes TimeSpan and Data Records to show extreme cases of temperature present in records"""

    results = calculate_extreme_temp(data_set)

    # Printing the end results
    print(f"{string_to_date(time_span)}")
    print(f"Highest : {results.get('high_temp')}C on {results.get('high_temp_date')}")
    print(f"Lowest : {results.get('low_temp')}C on {results.get('low_temp_date')}")
    print(f"Humidity : {results.get('humidity')}% on {results.get('humidity_date')}")


def calculate_extreme_temp(data_set, high_temp=None, low_temp=None, humidity=None):
    """Takes list of data and returns extreme conditions and occurrence dates"""
    for row in data_set:
        # Max Temperature Check
        if row.get('Max TemperatureC') and (not high_temp or high_temp < int(row.get('Max TemperatureC'))):
            high_temp_date = row.get('PKT')
            high_temp = int(row.get('Max TemperatureC'))

        # Min Temperature Check
        if row.get('Min TemperatureC') and (not low_temp or low_temp > int(row.get('Min TemperatureC'))):
            low_temp_date = row.get('PKT')
            low_temp = int(row.get('Min TemperatureC'))

        # Humidity Check
        if row.get('Max Humidity') and (not humidity or humidity < int(row.get('Max Humidity'))):
            humidity = int(row.get('Max Humidity'))
            humidity_date = row.get('PKT')

    high_temp_date = string_to_date(high_temp_date, '-')
    low_temp_date = string_to_date(low_temp_date, '-')
    humidity_date = string_to_date(humidity_date, '-')

    return {
        'high_temp': high_temp, 'low_temp': low_temp,
        'humidity': humidity, 'high_temp_date': high_temp_date,
        'low_temp_date': low_temp_date, 'humidity_date': humidity_date
    }


def display_avg(time_span, data_set):
    """Takes TimeSpan and Data Records to show average temperature according to records"""

    # Calculates Averages
    high_avg, low_avg, humid_avg = calculate_avg_temperature(data_set)

    # Printing the end results
    print(f"{string_to_date(time_span)}")

    # .0f means that we are skipping the decimal part while showing
    print(f"Highest Temperature Average : {high_avg: .0f}C")
    print(f"Lowest Temperature Average : {low_avg: .0f}C")
    print(f"Mean Humidity Average : {humid_avg: .2f}%")


def calculate_avg_temperature(data_set, high_temp_avg=0, low_temp_avg=0, humidity_avg=0,
                              high_temp_days=0, low_temp_days=0, humidity_days=0):
    """Takes List of Data and Calculates Averages"""

    for row in data_set:
        if row.get('Max TemperatureC'):
            high_temp_avg += int(row.get('Max TemperatureC'))
            high_temp_days += 1

        if row.get('Min TemperatureC'):
            low_temp_avg += int(row.get('Min TemperatureC'))
            low_temp_days += 1

        if row.get('Mean Humidity'):
            humidity_avg += int(row.get('Mean Humidity'))
            humidity_days += 1

    high_avg = high_temp_avg / high_temp_days
    low_avg = low_temp_avg / low_temp_days
    humid_avg = humidity_avg / humidity_days

    return high_avg, low_avg, humid_avg


def display_chart(time_span, data_set):
    """Takes TimeSpan and Data Records to show Each Day's Chart regarding highest and lowest temperatures"""

    print(f"{string_to_date(time_span)}")
    for num, row in enumerate(data_set):

        # Showing Max Temp Results
        if row.get('Max TemperatureC') and row.get('Min TemperatureC'):
            params = [{
                'day': num + 1,
                'temp': int(row.get('Max TemperatureC')),
                'color': 'red'
            }, ]

            colored_text(params)

        # Showing Min Temp Results
        if row.get('Min TemperatureC'):
            params = [{
                'day': num + 1,
                'temp': int(row.get('Min TemperatureC')),
                'color': 'blue'
            }, ]

            colored_text(params)


def colored_text(params):
    """Create chart lines"""
    temp_value = ''
    for param in params:
        temp_value += "-" if temp_value else ''
        print(param.get('day', ''), end="")
        print_line(param.get('temp'), param.get('color'))
        temp_value += f" {param.get('temp')}C "
    print(temp_value)


def print_line(count, color):
    """This function print line with specified color taken as argument"""
    for i in range(count):
        print(colored('+', color), end='')


def display_range_chart(time_span, data_set):
    """Takes TimeSpan and Data Records to show Range of Temperature each Day"""

    # Printing the end results
    print(f"{string_to_date(time_span)}")

    for num, row in enumerate(data_set):
        if row.get('Max TemperatureC') and row.get('Min TemperatureC'):

            params = [{
                'day': num + 1,
                'temp': int(row.get('Max TemperatureC')),
                'color': 'red'
            }, {
                'temp': int(row.get('Min TemperatureC')),
                'color': 'blue'
            }]

            colored_text(params)


def string_to_date(time_span, delimeter='/'):
    """Here we parse given date in string format to get a well formatted Date pattern (String to Date)"""

    date = separate_combined_date(time_span, delimeter)

    year, month, day = date

    if day:
        date = datetime.date(year, month, day).strftime('%d %B %Y')
    elif month:
        date = datetime.date(year, month, 1).strftime('%B %Y')
    else:
        date = datetime.date(year, 1, 1).strftime('%Y')

    return date


def separate_combined_date(commandline_dates, delimeter='/'):
    """It takes date in YYYY/MM/DD foramt and Returns the Accurate information
     of date by splitting it in Year, Month and Day"""

    # User can give year, month and day separated by '/', so here we split them
    default_date = [None, None, None]
    splitted_date = commandline_dates.split(delimeter)

    for index, value in enumerate(splitted_date):
        default_date[index] = int(value)

    return default_date


def main():
    """Takes system args and extract options and time to iterate the whole process over it"""

    function_specifier = {
        'extreme': display_extreme,
        'average': display_avg,
        'chart': display_chart,
        'range_chart': display_range_chart,
    }

    args = applying_commandline_arguments()
    os.chdir(args.directory)

    for arg in vars(args):
        attribute_val = getattr(args, arg)
        if attribute_val and arg != "directory":
            data_set = parser(attribute_val)
            if data_set:
                function_specifier.get(arg)(attribute_val, data_set)
            else:
                print("No Data Found")


if __name__ == "__main__":
    main()
