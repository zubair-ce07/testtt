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

import argparse
from termcolor import colored


parser_arg = argparse.ArgumentParser()
parser_arg.add_argument("directory", help="you have to specify a directory for records")
parser_arg.add_argument("-e", "--extreme", help="Show extreme records of specified date")
parser_arg.add_argument("-a", "--average", help="Show average records of specified date")
parser_arg.add_argument("-c", "--chart", help="Show horizontal bar chart of specified date")
parser_arg.add_argument("-r", "--range_chart", help="Show temperature range chart of specified date")
args = parser_arg.parse_args()

total_months = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',
    6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
    11: 'Nov', 12: 'Dec',
}


def parser(directory_path, time_span):
    """This is the main function of this module, it takes directory and date to work on and in return
    it gives a list of records from the directory related to the specified dates"""

    year, month, day = separate_combined_date(time_span)
    files = get_required_files(directory_path, year, month)

    # If records found
    if len(files) > 0:
        # reads all the files and get records in a list
        return data_collector(directory_path, files, day)
    else:
        return None


def get_required_files(directory_path, year_required, month_required):
    """This function takes directory, year and month to choose those files from it which are required"""

    if month_required in total_months:
        month = total_months[month_required]
        search_pattern = str(year_required) + "_" + str(month) + ".txt"
    else:
        search_pattern = str(year_required)

    matches = []

    for root, dir_names, file_names in os.walk(directory_path):
        for file_name in file_names:
            if search_pattern in file_name:
                matches.append(os.path.join(file_name))
    return matches


def data_collector(directory_path, records, day=None):
    """It takes path of directory with names of files as arguments
     and returns Structured Data in the form of list"""

    weather_structure = []
    for record in records:
        weather_structure.extend(file_reader(directory_path, record, day))
    return weather_structure


def file_reader(directory_path, file_name, specific_date=None):
    """It takes path of directory with names of files as arguments
     and returns Structured Data in the form of WeatherRecord Object list"""

    file_records = []

    # Opening file
    month_file = open(directory_path + file_name, 'r')
    # First line contains information of file structure, so skipping them
    month_file.__next__()

    # if specific date is not given
    if not specific_date:
        lines = month_file.readlines()
        for line in lines:
            file_records.append(create_weather_instance(line))
    else:
        lines = month_file.readlines()
        line = lines[int(specific_date) - 1]
        file_records.append(create_weather_instance(line))
    # Closing file
    month_file.close()

    return file_records


# Calculation Module
def display_extreme(time_span, list_data):
    """Takes TimeSpan and Data Records to show extreme cases of temperature present in records"""
    high_temp, low_temp, humidity, high_temp_date, low_temp_date, humidity_date \
        = calculate_extreme_temperature_dates_values(list_data)

    # Printing the end results
    print(f"{string_to_date(time_span)}")
    print(f"Highest : {high_temp}C on {high_temp_date}")
    print(f"Lowest : {low_temp}C on {low_temp_date}")
    print(f"Humidity : {humidity}% on {humidity_date}")


def calculate_extreme_temperature_dates_values(list_data):
    """Takes list of data and returns extreme conditions and occurrence dates"""
    for data in list_data:
        # Max Temperature Check

        if data.max_temp and ('high_temp' not in locals()
                              or high_temp < data.max_temp):
            high_temp_date = data.date_pkt
            high_temp = data.max_temp

        # Min Temperature Check
        if data.min_temp and ('low_temp' not in locals()
                              or low_temp > data.min_temp):
            low_temp_date = data.date_pkt
            low_temp = data.min_temp

        # Humidity Check
        if data.max_humidity and ('humidity' not in locals()
                                  or humidity < data.max_humidity):
            humidity = data.max_humidity
            humidity_date = data.date_pkt

    high_temp_date = date_format_converter(high_temp_date)
    low_temp_date = date_format_converter(low_temp_date)
    humidity_date = date_format_converter(humidity_date)

    return high_temp, low_temp, humidity, high_temp_date, low_temp_date, humidity_date


def display_avg(time_span, list_data):
    """Takes TimeSpan and Data Records to show average temperature according to records"""

    # Calculates Averages
    high_avg, low_avg, humid_avg = calculate_avg_temperature(list_data)

    # Printing the end results
    print(f"{string_to_date(time_span)}")
    print(f"Highest Temperature Average : {high_avg: .0f}C")
    print(f"Lowest Temperature Average : {low_avg: .0f}C")
    print(f"Mean Humidity Average : {humid_avg: .2f}%")


def calculate_avg_temperature(list_data, high_temp_avg=0, low_temp_avg=0, humidity_avg=0,
                  high_temp_days=0, low_temp_days=0, humidity_days=0):
    """Takes List of Data and Calculates Averages"""

    for data in list_data:
        if data.max_temp:
            high_temp_avg += data.max_temp
            high_temp_days += 1

        if data.min_temp:
            low_temp_avg += data.min_temp
            low_temp_days += 1

        if data.mean_humidity:
            humidity_avg += data.mean_humidity
            humidity_days += 1

    high_avg = high_temp_avg / high_temp_days
    low_avg = low_temp_avg / low_temp_days
    humid_avg = humidity_avg / humidity_days

    return high_avg, low_avg, humid_avg


def display_chart(time_span, list_data):
    """Takes TimeSpan and Data Records to show Each Day's Chart regarding highest and lowest temperatures"""

    print(f"{string_to_date(time_span)}")

    for num, data in enumerate(list_data):

        # Showing Max Temp Results
        if data.max_temp:
            colored_single_print(num + 1, data.max_temp, 'red')

        # Showing Min Temp Results
        if data.min_temp:
            colored_single_print(num + 1, data.min_temp, 'blue')


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


def display_range_chart(time_span, list_data):
    """Takes TimeSpan and Data Records to show Range of Temperature each Day"""

    # Printing the end results
    print(f"{string_to_date(time_span)}")

    for num, data in enumerate(list_data):
        if data.max_temp and data.min_temp:
            colored_double_print(num + 1, data.max_temp, data.min_temp, 'red', 'blue')


def string_to_date(time_span):
    """Here we parse given date in string format to get a well formatted Date pattern (String to Date)"""

    year_required, month_required, day_required = separate_combined_date(time_span)
    if not month_required and not day_required:
        return datetime(year_required, 1, 1, 0, 0).strftime('%Y')

    elif not day_required:
        return datetime(year_required, month_required, 1, 0, 0).strftime('%B %Y')

    else:
        return datetime(year_required, month_required, day_required, 0, 0).strftime('%d %B %Y')


def date_format_converter(date):
    """Here we parse given date to get a well formatted Date pattern (Date to Date) """

    return datetime(date[0].year, date[0].month, date[0].day, 0, 0).strftime('%B %Y')


def create_weather_instance(line):
    """this function takes a line from file and create an instance of weather records"""

    line.replace('\n', '')
    fields = line.split(',')
    date_pkt = datetime.strptime(fields[0], '%Y-%m-%d').date(),
    max_temp = fields[1],
    mean_temp = fields[2],
    min_temp = fields[3],
    max_humidity = fields[7],
    mean_humidity = fields[8],
    min_humidity = fields[9],

    return WeatherRecord(date_pkt, max_temp, mean_temp,
                         min_temp, max_humidity, mean_humidity, min_humidity)


def separate_combined_date(commandline_dates):
    """It takes date in YYYY/MM/DD foramt and Returns the Accurate information
     of date by splitting it in Year, Month and Day"""

    # User can give year, month and day separated by '/', so here we split them
    splitted_date = commandline_dates.split('/')
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


# Data Structure
class WeatherRecord:

    def __init__(self, date_pkt, max_temp, mean_temp, min_temp,
                 max_humidity, mean_humidity, min_humidity):

        self.date_pkt = date_pkt

        # Temperatures
        if not max_temp[0]:
            self.max_temp = None
        else:
            self.max_temp = int(max_temp[0])

        if not mean_temp[0]:
            self.mean_temp = None
        else:
            self.mean_temp = int(mean_temp[0])

        if not min_temp[0]:
            self.min_temp = None
        else:
            self.min_temp = int(min_temp[0])

        # Humidity
        if not max_humidity[0]:
            self.max_humidity = None
        else:
            self.max_humidity = float(max_humidity[0])

        if not mean_humidity[0]:
            self.mean_humidity = None
        else:
            self.mean_humidity = float(mean_humidity[0])

        if not min_humidity[0]:
            self.min_humidity = None
        else:
            self.min_humidity = float(min_humidity[0])


def main_function():
    """Takes system args and extract options and time to iterate the whole process over it"""

    function_specifier = {
        'extreme': display_extreme,
        'average': display_avg,
        'chart': display_chart,
        'range_chart': display_range_chart,
    }

    directory_path = args.directory

    for arg in vars(args):
        attribute_val = getattr(args, arg)
        if attribute_val and arg != "directory":
            data_set = parser(directory_path, attribute_val)
            function_specifier[arg](attribute_val, data_set)


if __name__ == "__main__":
    main_function()
