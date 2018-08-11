"""Calculates the end results, according to given records and options"""

from datetime import datetime
from termcolor import colored

from ParserModule import time_parser


def calculator(time_span, option_given, list_data):
    """Takes time span, option and list of data and calculate accordingly"""

    # -e option will give highest, lowest temperature statistics of records
    if option_given == "-e":
        highest_date = None
        lowest_date = None
        humidity_date = None
        highest_temperature = None
        lowest_temperature = None
        humidity = None

        for data in list_data:
            if data.max_temperature_c is not None:
                if highest_temperature is None:
                    highest_date = data.date_pkt
                    highest_temperature = data.max_temperature_c
                elif highest_temperature < data.max_temperature_c:
                    highest_date = data.date_pkt
                    highest_temperature = data.max_temperature_c
            if data.min_temperature_c is not None:
                if lowest_temperature is None:
                    lowest_date = data.date_pkt
                    lowest_temperature = data.min_temperature_c
                elif lowest_temperature > data.min_temperature_c:
                    lowest_date = data.date_pkt
                    lowest_temperature = data.min_temperature_c
            if data.max_humidity is not None:
                if humidity is None:
                    humidity = data.max_humidity
                    humidity_date = data.date_pkt
                elif humidity < data.max_humidity:
                    humidity = data.max_humidity
                    humidity_date = data.date_pkt

        year_required, month_required, day_required = time_parser(time_span)
        if month_required is None and day_required is None:
            print(datetime(int(year_required), 1,
                           1, 0, 0).strftime('%Y'))
        elif day_required is None:
            print(datetime(int(year_required), int(month_required),
                           1, 0, 0).strftime('%B %Y'))
        else:
            print(datetime(int(year_required), int(month_required),
                           int(day_required), 0, 0).strftime('%d %B %Y'))

        print("Highest : {0}C on {1}".format(highest_temperature,
                                             datetime(highest_date[0].year, highest_date[0].month,
                                                      highest_date[0].day, 0, 0).strftime('%B %Y')))
        print("Lowest : {0}C on {1}".format(lowest_temperature,
                                            datetime(lowest_date[0].year, lowest_date[0].month,
                                                     lowest_date[0].day, 0, 0).strftime('%B %Y')))
        print("Humidity : {0}% on {1}".format(humidity, datetime(humidity_date[0].year, humidity_date[0].month,
                                                                 humidity_date[0].day, 0, 0).strftime('%B %Y')))

    # -a option will give average statistics of records
    elif option_given == "-a":
        highest_temperature_avg = None
        lowest_temperature_avg = None
        mean_humidity_avg = None

        highest_days = 0
        lowest_days = 0
        humidity_days = 0

        for data in list_data:
            if data.max_temperature_c is not None:
                if highest_temperature_avg is None:
                    highest_temperature_avg = data.max_temperature_c
                    highest_days += 1
                else:
                    highest_temperature_avg += data.max_temperature_c
                    highest_days += 1

            if data.min_temperature_c is not None:
                if lowest_temperature_avg is None:
                    lowest_temperature_avg = data.min_temperature_c
                    lowest_days += 1
                else:
                    lowest_temperature_avg += data.min_temperature_c
                    lowest_days += 1

            if data.mean_humidity is not None:
                if mean_humidity_avg is None:
                    mean_humidity_avg = data.mean_humidity
                    humidity_days += 1
                else:
                    mean_humidity_avg = data.mean_humidity
                    humidity_days += 1

        year_required, month_required, day_required = time_parser(time_span)
        if month_required is None and day_required is None:
            print(datetime(int(year_required), 1,
                           1, 0, 0).strftime('%Y'))
        elif day_required is None:
            print(datetime(int(year_required), int(month_required),
                           1, 0, 0).strftime('%B %Y'))
        else:
            print(datetime(int(year_required), int(month_required),
                           int(day_required), 0, 0).strftime('%d %B %Y'))

        print("Highest Temperature Average : {0: .0f}C".format(highest_temperature_avg / highest_days))
        print("Lowest Temperature Average : {0: .0f}C".format(lowest_temperature_avg / lowest_days))
        print("Mean Humidity Average : {0: .2f}%".format(mean_humidity_avg / humidity_days))

    # -c option will give horizontal chart bar
    elif option_given == "-c":

        year_required, month_required, day_required = time_parser(time_span)
        if month_required is None and day_required is None:
            print(datetime(int(year_required), 1,
                           1, 0, 0).strftime('%Y'))
        elif day_required is None:
            print(datetime(int(year_required), int(month_required),
                           1, 0, 0).strftime('%B %Y'))
        else:
            print(datetime(int(year_required), int(month_required),
                           int(day_required), 0, 0).strftime('%d %B %Y'))

        for num, data in enumerate(list_data):
            if data.max_temperature_c is not None:
                print(num + 1, end=" ")
                for i in range(data.max_temperature_c):
                    text = colored('+', 'red')
                    print(text, end='')
                print(" {0: .0f}C".format(data.max_temperature_c))
            else:
                print(num + 1, "No Value", end="\n")

            if data.min_temperature_c is not None:
                print(num + 1, end=" ")
                for i in range(data.min_temperature_c):
                    text = colored('+', 'blue')
                    print(text, end='')
                print(" {0: .0f}C".format(data.min_temperature_c))
            else:
                print(num + 1, "No Value", end="\n")

    # -d option will give horizontal chart bar of each day defining lowest and highest temperatures
    elif option_given == "-d":

        year_required, month_required, day_required = time_parser(time_span)
        if month_required is None and day_required is None:
            print(datetime(int(year_required), 1,
                           1, 0, 0).strftime('%Y'))
        elif day_required is None:
            print(datetime(int(year_required), int(month_required),
                           1, 0, 0).strftime('%B %Y'))
        else:
            print(datetime(int(year_required), int(month_required),
                           int(day_required), 0, 0).strftime('%d %B %Y'))

        for num, data in enumerate(list_data):
            if data.max_temperature_c is not None and data.min_temperature_c is not None:
                print(num + 1, end=" ")
                for i in range(data.min_temperature_c):
                    text = colored('+', 'blue')
                    print(text, end='')
                for i in range(data.max_temperature_c):
                    text = colored('+', 'red')
                    print(text, end='')
                print("{0: .0f}C - {1: .0f}C".format(data.min_temperature_c, data.max_temperature_c))
    else:
        print("The Given Option is not valid")
