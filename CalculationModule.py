"""Calculates the end results, according to given records and options"""

from datetime import datetime
from termcolor import colored

from ParserModule import time_parser


def calculate_results(time_span, option_given, list_data):
    """Takes time span, option and list of data to calculate accordingly"""

    # extreme_temperature or -e  option will give highest, lowest temperature statistics of records
    if option_given == "-e" or option_given == "extreme_temperature":
        extreme_temperature_conditions(time_span, list_data)

    # average_temperature or -a option will give average statistics of records
    elif option_given == "-a" or option_given == "average_temperature":
        average_temperature_conditions(time_span, list_data)

    # chart_temperature or -c option will give horizontal chart bar
    elif option_given == "-c" or option_given == "chart_temperature":
        chart_highest_lowest_temperature(time_span, list_data)

    # range_temperature or -r option will give horizontal chart bar of each day defining lowest and highest temperatures
    elif option_given == "-r" or option_given == "range_temperature":
        temperature_range_chart(time_span, list_data)

    else:
        print("The Given Option is not valid")


def extreme_temperature_conditions(time_span, list_data):
    """Takes TimeSpan and Data Records to show extreme cases of temperature present in records"""
    highest_temperature_date = None
    lowest_temperature_date = None
    highest_humidity_date = None
    highest_temperature = None
    lowest_temperature = None
    humidity = None

    for data in list_data:
        if data.max_temperature_c is not None:
            if not highest_temperature:
                highest_temperature_date = data.date_pkt
                highest_temperature = data.max_temperature_c
            elif highest_temperature < data.max_temperature_c:
                highest_temperature_date = data.date_pkt
                highest_temperature = data.max_temperature_c
        if data.min_temperature_c:
            if not lowest_temperature:
                lowest_temperature_date = data.date_pkt
                lowest_temperature = data.min_temperature_c
            elif lowest_temperature > data.min_temperature_c:
                lowest_temperature_date = data.date_pkt
                lowest_temperature = data.min_temperature_c
        if data.max_humidity:
            if not humidity:
                humidity = data.max_humidity
                highest_humidity_date = data.date_pkt
            elif humidity < data.max_humidity:
                humidity = data.max_humidity
                highest_humidity_date = data.date_pkt

    # Here we parse given date to get a well formatted Date pattern
    year_required, month_required, day_required = time_parser(time_span)
    if not month_required and not day_required:
        print(datetime(int(year_required), 1,
                       1, 0, 0).strftime('%Y'))
    elif not day_required:
        print(datetime(int(year_required), int(month_required),
                       1, 0, 0).strftime('%B %Y'))
    else:
        print(datetime(int(year_required), int(month_required),
                       int(day_required), 0, 0).strftime('%d %B %Y'))

    print("Highest : {0}C on {1}".format(highest_temperature,
                                         datetime(highest_temperature_date[0].year, highest_temperature_date[0].month,
                                                  highest_temperature_date[0].day, 0, 0).strftime('%B %Y')))
    print("Lowest : {0}C on {1}".format(lowest_temperature,
                                        datetime(lowest_temperature_date[0].year, lowest_temperature_date[0].month,
                                                 lowest_temperature_date[0].day, 0, 0).strftime('%B %Y')))
    print("Humidity : {0}% on {1}".format(humidity,
                                          datetime(highest_humidity_date[0].year, highest_humidity_date[0].month,
                                                   highest_humidity_date[0].day, 0, 0).strftime('%B %Y')))


def average_temperature_conditions(time_span, list_data):
    """Takes TimeSpan and Data Records to show average temperature according to records"""
    highest_temperature_average = None
    lowest_temperature_average = None
    mean_humidity_average = None

    highest_temperature_days_count = 0
    lowest_temperature_days_count = 0
    humidity_days_count = 0

    for data in list_data:
        if data.max_temperature_c:
            if not highest_temperature_average:
                highest_temperature_average = data.max_temperature_c
                highest_temperature_days_count += 1
            else:
                highest_temperature_average += data.max_temperature_c
                highest_temperature_days_count += 1

        if data.min_temperature_c:
            if not lowest_temperature_average:
                lowest_temperature_average = data.min_temperature_c
                lowest_temperature_days_count += 1
            else:
                lowest_temperature_average += data.min_temperature_c
                lowest_temperature_days_count += 1

        if data.mean_humidity:
            if not mean_humidity_average:
                mean_humidity_average = data.mean_humidity
                humidity_days_count += 1
            else:
                mean_humidity_average += data.mean_humidity
                humidity_days_count += 1

    # Here we parse given date to get a well formatted Date pattern
    year_required, month_required, day_required = time_parser(time_span)
    if not month_required and not day_required:
        print(datetime(int(year_required), 1,
                       1, 0, 0).strftime('%Y'))
    elif not day_required:
        print(datetime(int(year_required), int(month_required),
                       1, 0, 0).strftime('%B %Y'))
    else:
        print(datetime(int(year_required), int(month_required),
                       int(day_required), 0, 0).strftime('%d %B %Y'))

    print(
        "Highest Temperature Average : {0: .0f}C".format(highest_temperature_average / highest_temperature_days_count))
    print("Lowest Temperature Average : {0: .0f}C".format(lowest_temperature_average / lowest_temperature_days_count))
    print("Mean Humidity Average : {0: .2f}%".format(mean_humidity_average / humidity_days_count))


def chart_highest_lowest_temperature(time_span, list_data):
    """Takes TimeSpan and Data Records to show Each Day's Chart regarding highest and lowest temperatures"""

    # Here we parse given date to get a well formatted Date pattern
    year_required, month_required, day_required = time_parser(time_span)
    if not month_required and not day_required:
        print(datetime(int(year_required), 1,
                       1, 0, 0).strftime('%Y'))
    elif not day_required:
        print(datetime(int(year_required), int(month_required),
                       1, 0, 0).strftime('%B %Y'))
    else:
        print(datetime(int(year_required), int(month_required),
                       int(day_required), 0, 0).strftime('%d %B %Y'))

    for num, data in enumerate(list_data):
        if data.max_temperature_c:
            print(num + 1, end=" ")
            for i in range(data.max_temperature_c):
                text = colored('+', 'red')
                print(text, end='')
            print(" {0: .0f}C".format(data.max_temperature_c))
        else:
            print(num + 1, "No Value", end="\n")

        if data.min_temperature_c:
            print(num + 1, end=" ")
            for i in range(data.min_temperature_c):
                text = colored('+', 'blue')
                print(text, end='')
            print(" {0: .0f}C".format(data.min_temperature_c))
        else:
            print(num + 1, "No Value", end="\n")


def temperature_range_chart(time_span, list_data):
    """Takes TimeSpan and Data Records to show Range of Temperature each Day"""

    # Here we parse given date to get a well formatted Date pattern
    year_required, month_required, day_required = time_parser(time_span)
    if not month_required and not day_required:
        print(datetime(int(year_required), 1,
                       1, 0, 0).strftime('%Y'))
    elif not day_required:
        print(datetime(int(year_required), int(month_required),
                       1, 0, 0).strftime('%B %Y'))
    else:
        print(datetime(int(year_required), int(month_required),
                       int(day_required), 0, 0).strftime('%d %B %Y'))

    for num, data in enumerate(list_data):
        if data.max_temperature_c and data.min_temperature_c:
            print(num + 1, end=" ")
            for i in range(data.min_temperature_c):
                text = colored('+', 'blue')
                print(text, end='')
            for i in range(data.max_temperature_c):
                text = colored('+', 'red')
                print(text, end='')
            print("{0: .0f}C - {1: .0f}C".format(data.min_temperature_c, data.max_temperature_c))
