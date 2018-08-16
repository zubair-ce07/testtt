"""Calculates the end results, according to given records and options"""

from datetime import datetime
from termcolor import colored

from ParserModule import time_parser


def extreme_temperature_conditions(time_span, list_data):
    """Takes TimeSpan and Data Records to show extreme cases of temperature present in records"""

    for data in list_data:

        # Max Temperature Check
        if data.max_temperature_c and ('highest_temperature' not in locals()
                                       or highest_temperature < data.max_temperature_c):

            highest_temperature_date = data.date_pkt
            highest_temperature = data.max_temperature_c

        # Min Temperature Check
        if data.min_temperature_c and ('lowest_temperature' not in locals()
                                       or lowest_temperature > data.min_temperature_c):

            lowest_temperature_date = data.date_pkt
            lowest_temperature = data.min_temperature_c

        # Humidity Check
        if data.max_humidity and ('humidity' not in locals()
                                  or humidity < data.max_humidity):

            humidity = data.max_humidity
            highest_humidity_date = data.date_pkt

    # Printing the end results
    print(f"{string_to_date(time_span)}")
    print(f"Highest : {highest_temperature}C on {date_format_converter(highest_temperature_date)}")
    print(f"Lowest : {lowest_temperature}C on {date_format_converter(lowest_temperature_date)}")
    print(f"Humidity : {humidity}% on {date_format_converter(highest_humidity_date)}")


def average_temperature_conditions(time_span, list_data):
    """Takes TimeSpan and Data Records to show average temperature according to records"""
    highest_temperature_average = 0
    lowest_temperature_average = 0
    mean_humidity_average = 0

    highest_temperature_days_count = 0
    lowest_temperature_days_count = 0
    humidity_days_count = 0

    for data in list_data:
        if data.max_temperature_c:
            highest_temperature_average += data.max_temperature_c
            highest_temperature_days_count += 1

        if data.min_temperature_c:
            lowest_temperature_average += data.min_temperature_c
            lowest_temperature_days_count += 1

        if data.mean_humidity:
            mean_humidity_average += data.mean_humidity
            humidity_days_count += 1

    # Printing the end results
    print(f"{string_to_date(time_span)}")
    print(f"Highest Temperature Average : {highest_temperature_average / highest_temperature_days_count: .0f}C")
    print(f"Lowest Temperature Average : {lowest_temperature_average / lowest_temperature_days_count: .0f}C")
    print(f"Mean Humidity Average : {mean_humidity_average / humidity_days_count: .2f}%")


def chart_highest_lowest_temperature(time_span, list_data):
    """Takes TimeSpan and Data Records to show Each Day's Chart regarding highest and lowest temperatures"""

    print(f"{string_to_date(time_span)}")

    for num, data in enumerate(list_data):

        # Showing Max Temp Results
        if data.max_temperature_c:
            print(num + 1, end=" ")
            for i in range(data.max_temperature_c):
                print(colored('+', 'red'), end='')
            print(f" {data.max_temperature_c: .0f}C")
        else:
            print(num + 1, "No Value", end="\n")

        # Showing Min Temp Results
        if data.min_temperature_c:
            print(num + 1, end=" ")
            for i in range(data.min_temperature_c):
                print(colored('+', 'blue'), end='')
            print(f" {data.min_temperature_c: .0f}C")
        else:
            print(num + 1, "No Value", end="\n")


def temperature_range_chart(time_span, list_data):
    """Takes TimeSpan and Data Records to show Range of Temperature each Day"""

    # Printing the end results
    print(f"{string_to_date(time_span)}")

    for num, data in enumerate(list_data):
        if data.max_temperature_c and data.min_temperature_c:
            print(num + 1, end=" ")
            for i in range(data.min_temperature_c):
                print(colored('+', 'blue'), end='')
            for i in range(data.max_temperature_c):
                print(colored('+', 'red'), end='')

            print(f"{data.min_temperature_c: .0f}C - {data.max_temperature_c: .0f}C")


def string_to_date(time_span):
    """Here we parse given date in string format to get a well formatted Date pattern (String to Date)"""

    year_required, month_required, day_required = time_parser(time_span)
    if not month_required and not day_required:
        return datetime(year_required, 1, 1, 0, 0).strftime('%Y')

    elif not day_required:
        return datetime(year_required, month_required, 1, 0, 0).strftime('%B %Y')

    else:
        return datetime(year_required, month_required, day_required, 0, 0).strftime('%d %B %Y')


def date_format_converter(date):
    """Here we parse given date to get a well formatted Date pattern (Date to Date) """

    return datetime(date[0].year, date[0].month, date[0].day, 0, 0).strftime('%B %Y')
