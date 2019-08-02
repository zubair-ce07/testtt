import argparse
import calendar
import csv
import glob
import os
from operator import attrgetter
from datetime import datetime


weather_records = []


class Color:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    END = '\033[0m'


class WeatherMan:
    def __init__(self, complete_date, max_temperature, min_temperature, max_humidity, average_humidity):
        self.day = complete_date.day
        self.year = complete_date.year
        self.month = complete_date.month
        self.max_temperature = int(max_temperature) if max_temperature else 0
        self.min_temperature = int(min_temperature) if min_temperature else 0
        self.max_humidity = int(max_humidity) if max_humidity else 0
        self.average_humidity = int(average_humidity) if average_humidity else 0


def prepare_weather_man(path_to_file):
    for input_file in glob.glob(path_to_file + "/*.txt"):
        full_file_path = os.path.join(path_to_file, input_file)
        for weather_row in read_and_filter_csv_file(full_file_path, is_comment, is_whitespace):
            weather_record_date = datetime.strptime(weather_row.get('PKT'), '%Y-%m-%d') if weather_row.get('PKT') \
                else datetime.strptime(weather_row.get('PKST'), '%Y-%m-%d')
            weatherman_row = WeatherMan(weather_record_date,
                                        weather_row['Max TemperatureC'],
                                        weather_row["Min TemperatureC"],
                                        weather_row['Max Humidity'], weather_row[' Mean Humidity'])
            weather_records.append(weatherman_row)


def calculate_yearly_report(yearly_report):
    highest_temp = max([record for record in weather_records if record.year == yearly_report.year],
                       key=attrgetter('max_temperature'))

    lowest_temp = min([record for record in weather_records if record.year == yearly_report.year],
                      key=attrgetter('min_temperature'))

    max_humidity = max([record for record in weather_records if record.year == yearly_report.year],
                       key=attrgetter('max_humidity'))

    return highest_temp, lowest_temp, max_humidity


def show_yearly_report(highest_temperature_obj, lowest_temperature_obj, max_humidity_obj):
    print(f'Highest: {highest_temperature_obj.max_temperature}C on '
          f'{calendar.month_name[highest_temperature_obj.month]} {highest_temperature_obj.day}')

    print(f'Lowest: {lowest_temperature_obj.min_temperature}C on '
          f'{calendar.month_name[lowest_temperature_obj.month]} {lowest_temperature_obj.day}')

    print(f'Humidity: {max_humidity_obj.max_temperature}C on '
          f'{calendar.month_name[max_humidity_obj.month]} {max_humidity_obj.day}\n')


def calculate_monthly_report(monthly_report):
    highest_temp_records = [record.max_temperature for record in weather_records if record.max_temperature and
                            record.year == monthly_report.year and record.month == monthly_report.month]

    lowest_temp_records = [record.min_temperature for record in weather_records if record.min_temperature and
                           record.year == monthly_report.year and record.month == monthly_report.month]

    humidity_records = [record.average_humidity for record in weather_records if record.average_humidity and
                        record.year == monthly_report.year and record.month == monthly_report.month]

    highest_temperature_value = sum(highest_temp_records)//len(highest_temp_records)
    lowest_temperature_value = sum(lowest_temp_records)//len(lowest_temp_records)
    average_humidity_value = sum(humidity_records)//len(humidity_records)

    return highest_temperature_value, lowest_temperature_value, average_humidity_value


def show_monthly_report(highest_average, lowest_average, humidity_average):
    print(f'Highest Average: {highest_average}C')
    print(f'Lowest Average: {lowest_average}C')
    print(f'Average Mean Humidity: {humidity_average}%\n')


def draw_bar_chart(year_argument):
    month_and_year = calendar.month_name[int(year_argument.month)] + " " + str(year_argument.year)
    print(month_and_year)
    month_records = [record for record in weather_records if record.year == year_argument.year and
                     record.month == year_argument.month]

    for day_count, weather_row in enumerate(month_records):

        print(f'{Color.PURPLE}{day_count + 1} {Color.RED}{"+" * abs(weather_row.max_temperature)}'
              f'{Color.PURPLE}{str(weather_row.max_temperature)}C')

        print(f'{Color.PURPLE}{day_count + 1} {Color.BLUE}{"+" * abs(weather_row.min_temperature)}'
              f'{Color.PURPLE}{str(weather_row.min_temperature)}C')
    print(Color.END + month_and_year)
    for day_count, weather_row in enumerate(month_records):
        print(f'{Color.PURPLE}{day_count + 1} {Color.BLUE}{"+" * abs(weather_row.min_temperature)}{Color.RED} '
              f'{"+" * abs(weather_row.max_temperature)} {Color.PURPLE}{str(weather_row.min_temperature)}C - '
              f'{str(weather_row.max_temperature)}C')


def is_comment(line):
    return line.startswith('<')


def is_whitespace(line):
    return line.isspace()


def iterate_filtered(input_file, *filters):
    for line in input_file:
        if not any(user_filter(line) for user_filter in filters):
            yield line


def read_and_filter_csv_file(csv_path, *filters):
    with open(csv_path) as input_file:
        iterate_clean_lines = iterate_filtered(input_file, *filters)
        weather_reader = csv.DictReader(iterate_clean_lines)
        return [weather_row for weather_row in weather_reader]


def main():
    parser = argparse.ArgumentParser(description="Enter Arguments")
    parser.add_argument('path', help='Please enter path of directory')
    parser.add_argument("-e", action="store", dest="yearly_report", nargs="*",
                        help="Please enter year of which you want the system to display highest and lowest temperature"
                             " values", type=lambda x: datetime.strptime(x, '%Y'))

    parser.add_argument("-a", action="store", dest="monthly_report", nargs="*",
                        help="Please enter particular year and month of which you want the system to display average"
                             " temperature values", type=lambda x: datetime.strptime(x, '%Y/%m'))

    parser.add_argument("-c", action="store", dest="horizontal_charts", nargs="*",
                        help="Please enter particular year and month of which you want the system to display horizontal"
                             " charts", type=lambda x: datetime.strptime(x, '%Y/%m'))

    args = parser.parse_args()
    prepare_weather_man(args.path)

    if args.yearly_report:
        for argument in args.yearly_report:
            max_temp, min_temp, max_humidity = calculate_yearly_report(argument)
            show_yearly_report(max_temp, min_temp, max_humidity)

    elif args.monthly_report:
        for argument in args.monthly_report:
            highest_average, lowest_average, humidity_average = calculate_monthly_report(argument)
            show_monthly_report(highest_average, lowest_average, humidity_average)

    elif args.horizontal_charts:
        for argument in args.horizontal_charts:
            draw_bar_chart(argument)


if __name__ == "__main__":
    main()
