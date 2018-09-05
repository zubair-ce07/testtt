"""Main module which runs the whole weatherman program, It takes Command Line Args to work with

Command Line Args:
'-e' : Gives highest, lowest temperatures and highest humidity
'-a' : Gives average temperature and humidity
'-c' : Gives results in the chart/graph form
'-r' : Gives results in chart form but 1 day has only 1 graph showing range of temperature
"""

import os
import calendar
import csv
import argparse
import re
import dateutil.parser as date_utility
from termcolor import colored


class Weather:
    def __init__(self, data, date):
        self.date = date
        self.min_temp = int(data.get('Min TemperatureC'))
        self.max_temp = int(data.get('Max TemperatureC'))
        self.mean_temp = int(data.get('Mean TemperatureC'))
        self.min_humidity = int(data.get('Min Humidity'))
        self.max_humidity = int(data.get('Max Humidity'))
        self.mean_humidity = int(data.get('Mean Humidity'))


def applying_commandline_arguments():
    """Create Command Line Argument List"""
    parser_arg = argparse.ArgumentParser()
    parser_arg.add_argument("directory", help="directory for records")
    parser_arg.add_argument("-e", "--extreme", help="Show extreme records")
    parser_arg.add_argument("-a", "--average", help="Show average records")
    parser_arg.add_argument("-c", "--chart", help="Show bar chart")
    parser_arg.add_argument("-r", "--range_chart", help="Show range chart")
    return parser_arg.parse_args()


def parser(time_span):
    """It takes time-span and returns list of records from the directory"""

    # Getting date's year and month
    date = get_splitted_date(time_span)
    year = date[0] if len(date) > 0 else None
    month = date[1] if len(date) > 1 else None

    files = get_required_files(year, month)

    return files


def get_required_files(required_year, required_month):
    """It takes year and month to choose those files from directory"""
    try:
        month_name = None if not required_month else calendar.month_abbr[int(required_month)]
    except IndexError:
        raise IndexError("Wrong Month")

    # if month is not defined, we have to search on the basis of year only
    search_pattern = f'r(.{str(required_year)}_{month_name})' if month_name else f'r(.{required_year})'

    file_records = []
    for file_name in os.listdir():
        if re.compile(search_pattern).search(file_name):
            file_records += collect_data_from_files(file_name)
    return file_records


def collect_data_from_files(file):
    """It takes names of files as arguments, returns list of records"""

    # Registering dialect to skip spaces in names of dictionary
    csv.register_dialect('space_eliminator', delimiter=',', skipinitialspace=True)

    # Reading record files and returning in form of list
    csv_records = csv.DictReader(open(file, 'r'), dialect='space_eliminator')
    records = []
    for csv_record in csv_records:
        try:
            date = string_to_date(csv_record.get('PKT') or csv_record.get('PKST'), '-')
            value = Weather(csv_record, date)
            records.append(value)
        except ValueError:
            continue

    return records


def calculate_extreme_temp(data_set, high_temp=0, low_temp=300, humidity=0):
    """Takes list of data and returns extreme conditions and occurrence dates"""
    for row in data_set:
        # Max Temperature Check
        if row.max_temp and high_temp < row.max_temp:
            high_temp_date = row.date
            high_temp = row.max_temp

        # Min Temperature Check
        if row.min_temp and low_temp > row.min_temp:
            low_temp_date = row.date
            low_temp = row.min_temp

        # Humidity Check
        if row.max_humidity and humidity < row.max_humidity:
            humidity = row.max_humidity
            humidity_date = row.date

    temp_record = {
        'high_temp': high_temp, 'low_temp': low_temp,
        'humidity': humidity, 'high_temp_date': high_temp_date,
        'low_temp_date': low_temp_date, 'humidity_date': humidity_date
    }

    return temp_record


def calculate_avg_temperature(data_set, high_temp_avg=0, low_temp_avg=0, humidity_avg=0):
    """Takes List of Data and Calculates Averages"""

    for row in data_set:
        high_temp_avg += row.max_temp if row.max_temp else 0
        low_temp_avg += row.min_temp if row.min_temp else 0
        humidity_avg += row.mean_humidity if row.mean_humidity else 0

    results = dict()
    results['high_avg'] = high_temp_avg // len(data_set)
    results['low_avg'] = low_temp_avg // len(data_set)
    results['humid_avg'] = humidity_avg // len(data_set)

    return results


def string_to_date(time_span, delimeter='/'):
    """Converts given date to a formatted Date pattern (String to Date)"""

    try:
        date = date_utility.parse(time_span)
    except ValueError:
        raise ValueError

    date_splitted = get_splitted_date(time_span, delimeter)

    if len(date_splitted) == 3:
        date = date.strftime('%d %B %Y')
    elif len(date_splitted) == 2:
        date = date.strftime('%B %Y')
    else:
        date = date.strftime('%Y')

    return date


def get_splitted_date(date, delimeter='/'):
    return date.split(delimeter)


def main():
    """Takes system args and executes the whole process over it"""

    function_specifier = {
        'extreme': WeatherReport.print_summary_extreme,
        'average': WeatherReport.print_summary_avg,
        'chart': WeatherReport.print_horizontal_chart,
        'range_chart': WeatherReport.print_range_chart
    }

    args = applying_commandline_arguments()
    os.chdir(args.directory)

    for arg in vars(args):
        attribute_val = getattr(args, arg)
        if attribute_val and arg != "directory":
            data_set = parser(attribute_val)
            if len(data_set) > 0:
                function_specifier.get(arg)(attribute_val, data_set)
            else:
                print("No Data Found")


class WeatherReport:

    def print_summary_extreme(time_span, data_set):
        """Takes TimeSpan and Data Records to show extreme cases of temperature present in records"""

        results = calculate_extreme_temp(data_set)
        print(f"{string_to_date(time_span)}")
        print(f"Highest : {results.get('high_temp')}C on {results.get('high_temp_date')}")
        print(f"Lowest : {results.get('low_temp')}C on {results.get('low_temp_date')}")
        print(f"Humidity : {results.get('humidity')}% on {results.get('humidity_date')}")

    def print_summary_avg(time_span, data_set):
        """It will print the average temperature conditions"""

        results = calculate_avg_temperature(data_set)
        print(f"{string_to_date(time_span)}")
        print(f"Highest Temperature Average : {results['high_avg']}C")
        print(f"Lowest Temperature Average : {results['low_avg']}C")
        print(f"Mean Humidity Average : {results['humid_avg']}%")

    def print_range_chart(time_span, data_set):
        """Takes TimeSpan and Data Records to show Range of Temperature each Day"""

        print(f"{string_to_date(time_span)}")
        for num, row in enumerate(data_set):
            if row.max_temp and row.min_temp:
                params = [
                    {'day': num + 1, 'temp': row.max_temp, 'color': 'red'},
                    {'temp': row.min_temp, 'color': 'blue'}
                ]
                WeatherReport.colored_text(params)

    def print_horizontal_chart(time_span, data_set):
        """Takes TimeSpan and Data Records to show Each Day's Chart regarding highest and lowest temperatures"""

        print(f"{string_to_date(time_span)}")
        for num, row in enumerate(data_set):
            # Showing Max Temp Bar
            if row.max_temp:
                params = [{'day': num + 1, 'temp': row.max_temp, 'color': 'red'}, ]
                WeatherReport.colored_text(params)

            # Showing Min Temp Bar
            if row.min_temp:
                params = [{'day': num + 1, 'temp': row.min_temp, 'color': 'blue'}, ]
                WeatherReport.colored_text(params)

    def colored_text(params):
        """Creates chart lines"""
        temp_value = ''
        for param in params:
            temp_value += "-" if temp_value else ''
            print(param.get('day', ''), end="")
            WeatherReport.print_line(param.get('temp'), param.get('color'))
            temp_value += f" {param.get('temp')}C "
        print(temp_value)

    def print_line(count, color):
        """This function prints line with specified color taken as argument"""
        if count < 0:
            color = 'green'
        for i in range(abs(count)):
            print(colored('+', color), end='')


if __name__ == "__main__":
    main()
