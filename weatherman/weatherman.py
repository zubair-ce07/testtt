"""weaatherman.py script.
used for manipulating files having daily weather information of a city.
"""
import csv
import os.path
import re
import sys
from datetime import date, datetime
import constants


def display_usage_help():
    """Displays help message if wrong input is given."""
    message = """weatherman.py -[acde] <date> <path/to/files>/
        Parameters :-
            -e = Displays minimum and highest temperatures and highest humidity for given year
            
            -a = Displays average minimum temperature, maximum temperature and average \
            humidity for given month
            
            -c = Displays one line chart for minimum and highest temperatures of given month
            
            -d = Displays two line chart for minimum and highest temperatures of given month
            """
    print(message)


def validate_input(args):
    """ validate command line arguments

    :param args: command line args
    :return: true if input is correct else false
    """
    if len(args) is not 4:
        return False
    if not re.match(r'-[eacd]$', args[1]):
        return False
    if args[1][1] is 'e':
        if not re.match(r'\d{4}$', args[2]):
            return False
    else:
        if not re.match(r'^(\d{4})/((0?[1-9])|(1[012]))$', args[2]):
            return False
    return True


def generate_date(year, month=1, day=1):
    """Generate and return datetime.date object"""
    return date(int(year), int(month), int(day))


def parse_input(args):
    """Parse the input to decide what to do."""
    operation = None
    weather_date = None
    path_to_files = None

    if args[1] == '-e':
        operation = constants.YEARLY_HIGHEST_LOWEST_TEMP_HUMID
    elif args[1] == "-a":
        operation = constants.AVERAGE_TEMPERATURE
    elif args[1] == "-c":
        operation = constants.ONE_LINE_CHART
    else:
        operation = constants.TWO_LINE_CHART

    if operation == constants.YEARLY_HIGHEST_LOWEST_TEMP_HUMID:
        weather_date = generate_date(args[2][:4])
    else:
        weather_date = generate_date(args[2][:4], args[2][5:])

    path_to_files = args[3]

    return operation, weather_date, path_to_files


def get_min_max_row_from_file(func: "min or max function",
                              column_index,
                              csvfile):
    """Find the row in the csvfile which has optimum value for the given
    function and column index
    """
    csvfile.seek(0)
    next(csvfile)
    try:
        result_row = func([row for row in csv.reader(csvfile) if row[column_index] != ""],
                          key=lambda row: int(row[column_index]))

    except ValueError:
        return None
    return result_row


def get_file_path(path_to_files, city_name, year, month):
    """Return path to the required file given the city and date"""
    file_path = "{}{}_weather_{}_{}.txt".format(path_to_files,
                                                city_name,
                                                year,
                                                date(year, month, 1).strftime("%b"))
    return file_path


def get_min_max_row(func: "min or max function", row1, row2, key_index):
    """Compare two row entries depending upon the function given and key index value"""
    if row1 is None:
        return row2
    elif row2 is None:
        return row1
    else:
        return func(row1, row2, key=lambda x: int(x[key_index]))


def min_max_result_formatter(data_row, key_index, unit):
    """Generate result string to be printed provided result elements"""
    if data_row is None:
        return "No data found for given date."
    else:
        result_date = datetime.strptime(data_row[constants.PKT_INDEX], "%Y-%m-%d").date()
        return "{}{} on {} {}".format(data_row[key_index],
                                      unit,
                                      result_date.strftime("%B"),
                                      result_date.day)


def display_min_max_temp_humid(weather_date, path_to_files):
    """Find the min and max temperature and humidity rows for the given year"""
    city_name = "Murree"
    max_temp_row = None
    min_temp_row = None
    max_humid_row = None
    for month in range(1, 13):
        file_path = get_file_path(path_to_files, city_name, weather_date.year, month)
        if os.path.isfile(file_path):
            with open(file_path) as csvfile:
                current_month_max_temp = get_min_max_row_from_file(
                    max, constants.MAX_TEMPERATURE_INDEX, csvfile)

                current_month_min_temp = get_min_max_row_from_file(
                    min, constants.MIN_TEMPERATURE_INDEX, csvfile)

                current_month_max_humid = get_min_max_row_from_file(
                    max, constants.MAX_HUMIDITY_INDEX, csvfile)

                max_temp_row = get_min_max_row(max,
                                               current_month_max_temp,
                                               max_temp_row,
                                               constants.MAX_TEMPERATURE_INDEX)
                min_temp_row = get_min_max_row(min,
                                               current_month_min_temp,
                                               min_temp_row,
                                               constants.MIN_TEMPERATURE_INDEX)
                max_humid_row = get_min_max_row(max,
                                                current_month_max_humid,
                                                max_humid_row,
                                                constants.MAX_HUMIDITY_INDEX)

    result_str = min_max_result_formatter(max_temp_row, constants.MAX_TEMPERATURE_INDEX, "C")
    print("Highest: {}".format(result_str))

    result_str = min_max_result_formatter(min_temp_row, constants.MIN_TEMPERATURE_INDEX, "C")
    print("Lowest: {}".format(result_str))

    result_str = min_max_result_formatter(max_humid_row, constants.MAX_HUMIDITY_INDEX, "%")
    print("Humidity: {}".format(result_str))


def count_entries(file, key_index):
    """count number of rows in a file"""
    file.seek(0)
    next(file)
    count = sum([1 for row in file if row[key_index] != ""])
    return count


def get_average_value(csvfile, key_index):
    """Get the average of values for a column given the key_index"""
    days_count = count_entries(csvfile, key_index)
    csvfile.seek(0)
    next(csvfile)
    try:
        values = [int(row[key_index]) for row in csv.reader(csvfile)
                  if row[key_index] != ""]
        sum_value = sum(values)
        average_value = int(sum_value / days_count)
        return average_value
    except ValueError:
        return None


def average_result_formatter(value, unit):
    """Generate result string to be displayed"""
    if value is None:
        return "No data could be found on the given date."
    else:
        return "{}{}".format(value, unit)


def display_average_temperature_humidity(weather_date, path_to_files):
    """Provided the -a option, Display the average temperatures and humidity for a month"""
    city_name = "Murree"
    average_max_temp = None
    average_min_temp = None
    average_humidity = None
    file_path = get_file_path(path_to_files, city_name, weather_date.year, weather_date.month)
    if os.path.isfile(file_path):
        with open(file_path) as csvfile:
            average_max_temp = get_average_value(csvfile, constants.MAX_TEMPERATURE_INDEX)
            average_min_temp = get_average_value(csvfile, constants.MIN_TEMPERATURE_INDEX)
            average_humidity = get_average_value(csvfile, constants.MEAN_HUMIDITY_INDEX)

        print("Highest Average : {}".format(
            average_result_formatter(average_max_temp, "C")))
        print("Lowest Average : {}".format(
            average_result_formatter(average_min_temp, "C")))
        print("Average Humidity : {}".format(
            average_result_formatter(average_humidity, "%")))

    else:
        print("Error in opening the file. Such file does not exist.")


def one_line_chart(index, low, low_color, high, high_color, unit):
    """displays a one line chart for highest and lowest values provided"""

    result_string = "{index:02d} {low_color}{low_marks}{high_color}{high_marks}\
    {color_reset} {low}{unit} - {high}{unit}".format(index=index,
                                                     low_color=low_color,
                                                     low_marks="+" * low,
                                                     high_color=high_color,
                                                     high_marks="+" * high,
                                                     color_reset=constants.COLOR_RESET,
                                                     low=low,
                                                     high=high,
                                                     unit=unit)
    return result_string


def two_line_chart(index, low, low_color, high, high_color, unit):
    """displays a one line chart for highest and lowest values provided"""
    result_1 = "{index:02d} {low_color}{low_marks} {color_reset} {low}{unit}".format(
        index=index, low_color=low_color, low_marks="+" * low,
        color_reset=constants.COLOR_RESET, low=low, unit=unit)
    result_2 = "{index:02d} {high_color}{high_marks}{color_reset} {high}{unit}".format(
        index=index, high_color=high_color, high_marks="+" * high,
        color_reset=constants.COLOR_RESET, high=high, unit=unit)
    result_string = "{}\n{}".format(result_1, result_2)

    return result_string


def display_temperature_chart(weather_date, path_to_files, chart_type):
    """Provided the -d option, Display lower and higher temperatures of each day of
    the given month in line chart form"""
    city_name = "Murree"
    file_path = get_file_path(path_to_files, city_name, weather_date.year, weather_date.month)
    if os.path.isfile(file_path):
        month = weather_date.strftime("%B")
        print("{} {}".format(month, weather_date.year))
        with open(file_path) as csvfile:
            next(csvfile)
            for row in csv.reader(csvfile):
                try:
                    min_temperature = int(row[constants.MIN_TEMPERATURE_INDEX])
                    max_temperature = int(row[constants.MAX_TEMPERATURE_INDEX])
                    day = datetime.strptime(
                        row[constants.PKT_INDEX], "%Y-%m-%d").date().day
                    if chart_type == constants.ONE_LINE_CHART:
                        line_chart = one_line_chart(day,
                                                    min_temperature,
                                                    constants.COLOR_BLUE,
                                                    max_temperature,
                                                    constants.COLOR_RED,
                                                    "C")
                    else:
                        line_chart = two_line_chart(day,
                                                    min_temperature,
                                                    constants.COLOR_BLUE,
                                                    max_temperature,
                                                    constants.COLOR_RED,
                                                    "C")
                    print(line_chart)
                except ValueError:
                    print("Invalid data in the file for this date.")
    else:
        print("File not found!")


def main():
    """Driver function for the script."""
    if validate_input(sys.argv) is not True:
        display_usage_help()
        return

    operation, weather_date, path_to_files = parse_input(sys.argv)

    if operation == constants.YEARLY_HIGHEST_LOWEST_TEMP_HUMID:
        display_min_max_temp_humid(weather_date, path_to_files)
    elif operation == constants.AVERAGE_TEMPERATURE:
        display_average_temperature_humidity(weather_date, path_to_files)
    elif operation in (constants.ONE_LINE_CHART, constants.TWO_LINE_CHART):
        display_temperature_chart(weather_date, path_to_files, operation)


if __name__ == "__main__":
    main()
