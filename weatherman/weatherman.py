import csv
import os.path
import re
import sys
from datetime import date, datetime
import constants


def validate_input(args):
    if len(args) is not 4:
        return False
    if not re.match(r'-[eac]$', args[1]):
        return False
    if args[1][1] is 'e':
        if not re.match(r'\d{4}$', args[2]):
            return False
    else:
        if not re.match(r'^(\d{4})/((0?[1-9])|(1[012]))$', args[2]):
            return False
    return True


def generate_date(year, month=1, day=1):
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
        operation = constants.TWO_LINE_CHART
    else:
        operation = constants.ONE_LINE_CHART

    if operation == constants.YEARLY_HIGHEST_LOWEST_TEMP_HUMID:
        weather_date = generate_date(args[2][:4])
    else:
        weather_date = generate_date(args[2][:4], args[2][5:])

    path_to_files = args[3]

    return operation, weather_date, path_to_files


def get_min_max_row_from_file(func: "min or max function",
                              column_index,
                              csvfile):
    csvfile.seek(0)
    next(csvfile)
    result_row = func(csv.reader(csvfile),
                      key=lambda row: int(row[column_index]))
    return result_row


def get_file_path(path_to_files, city_name, year, month):
    file_path = "{}{}_weather_{}_{}.txt".format(path_to_files,
                                                city_name,
                                                year,
                                                date(year, month, 1).strftime("%b"))
    return file_path


def get_min_max_row(func: "min or max function", row1, row2, key_index):
    if row1 is None:
        return row2
    elif row2 is None:
        return row1
    else:
        return func(row1, row2, key=lambda x: int(x[key_index]))


def result_formatter(data_row, key_index):
    if data_row is None:
        return "No data found for given date."
    else:
        result_date = datetime.strptime(data_row[constants.PKT_INDEX], "%Y-%m-%d").date()
        return "{}C on {} {}".format(data_row[key_index],
                                     result_date.strftime("%B"),
                                     result_date.day)


def display_min_max_temp_humid(weather_date, path_to_files):
    city_name = "Murree"
    max_temp_row = None
    min_temp_row = None
    max_humid_row = None
    for month in range(1, 12):
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

    result_str = result_formatter(max_temp_row, constants.MAX_TEMPERATURE_INDEX)
    print("Highest: {}".format(result_str))

    result_str = result_formatter(min_temp_row, constants.MIN_TEMPERATURE_INDEX)
    print("Lowest: {}".format(result_str))

    result_str = result_formatter(max_humid_row, constants.MAX_HUMIDITY_INDEX)
    print("Humidity: {}".format(result_str))


def main():
    operation, weather_date, path_to_files = parse_input(sys.argv)

    if operation == constants.YEARLY_HIGHEST_LOWEST_TEMP_HUMID:
        display_min_max_temp_humid(weather_date, path_to_files)


if __name__ == "__main__":
    main()
