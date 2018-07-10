import calendar as cal
import csv
import argparse
import time
import glob as gb
import os


class DayForecast:

    def __init__(self, day_record):

        if 'PKT' in day_record:
            self.date = day_record['PKT']
        else:
            self.date = day_record['PKST']

        self.max_temp = day_record['Max TemperatureC']
        self.min_temp = day_record['Min TemperatureC']
        self.max_humidity = day_record['Max Humidity']
        self.mean_humidity = day_record[' Mean Humidity']


def get_date_params(date):
    date = date.split("-")
    return [date[0], date[1], date[2]]


def print_blue(text, n):
    print("\033[96m{}\033[00m".format(text) * n, end="")


def print_red(text, n):
    print("\033[31m{}\033[00m".format(text) * n, end="")


def valid_date(date):
    try:
        year_month = time.strptime(date, "%Y/%m")
        return year_month.tm_year, year_month.tm_mon
    except ValueError:
        msg = "Not a valid date. Should be YYYY/MM: '{0}'.".format(date)
        raise argparse.ArgumentTypeError(msg)


def valid_year(date):
    try:
        year = time.strptime(date, "%Y")
        return str(year.tm_year)
    except ValueError:
        msg = "Not a valid year: '{0}'.".format(date)
        raise argparse.ArgumentTypeError(msg)


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("directory", help="Directory to all weather files", type=str)
    parser.add_argument("-c", "--chart",
                        help="Display bar charts for provided month in C (YY/MM)",
                        action="append",
                        type=valid_date)
    parser.add_argument("-a", "--average",
                        help="Calculate average of max temp, min temp, mean humidity for month in A (YY/MM)",
                        action="append",
                        type=valid_date)
    parser.add_argument("-e", "--extreme",
                        help="Calculate max temp, humidity and min temp for year E (YY)",
                        action="append",
                        type=valid_year)

    return parser.parse_args()


def generate_yearly_report(maximum_temperature, minimum_temperature, maximum_humidity):
    year_max, month_max, date_max = get_date_params(maximum_temperature.date)
    year_min, month_min, date_min = get_date_params(minimum_temperature.date)
    year_humid, month_humid, date_humid = get_date_params(maximum_humidity.date)

    print("\nHighest: %sC on %s %s" % (maximum_temperature.max_temp,
                                       cal.month_name[int(month_max)],
                                       date_max))
    print("Lowest: %sC on %s %s" % (minimum_temperature.min_temp,
                                    cal.month_name[int(month_min)],
                                    date_min))
    print("Humidity: %s%% on %s %s\n" % (maximum_humidity.max_humidity,
                                         cal.month_name[int(month_humid)],
                                         date_humid))


def generate_monthly_report(avg_max_temp, avg_lowest_temp, avg_mean_humidity):
    print("Highest Average: %dC" % avg_max_temp)
    print("Lowest Average: %dC" % avg_lowest_temp)
    print("Average Mean Humidity: %d%%\n" % avg_mean_humidity)


def display_bar_charts(day, minimum_temp, maximum_temp, user_choice):
    print("%d " % day, end="")

    if user_choice == 1:
        print_blue("+", int(minimum_temp))
        print_red("+", int(maximum_temp))
        print(" %sC - %sC" % (minimum_temp, maximum_temp))

    elif user_choice == 2:
        print_red("+", int(maximum_temp))
        print(" %sC" % maximum_temp)

        print("%d " % day, end="")
        print_blue("+", int(minimum_temp))
        print(" %sC" % minimum_temp)


def parse_files(directory):
    weather_records = []
    os.chdir(directory)

    for file in gb.glob("*.txt"):
        weather_file = open(file, "r")
        reader = csv.DictReader(weather_file)

        for row in reader:
            if row['Max TemperatureC'] and \
                    row['Min TemperatureC'] and \
                    row['Max Humidity'] and \
                    row[' Mean Humidity']:
                weather_records.append(DayForecast(row))

    return weather_records


def calculate_results(args, weather_records):
    weather_record_subset = []
    if args.extreme:
        year = args.extreme[0]

        for record in weather_records:
            if year in record.date:
                weather_record_subset.append(record)

        maximum_temperature = max(weather_record_subset, key=lambda DayForecast: int(DayForecast.max_temp))
        minimum_temperature = min(weather_record_subset, key=lambda DayForecast: int(DayForecast.min_temp))
        maximum_humidity = max(weather_record_subset, key=lambda DayForecast: int(DayForecast.max_humidity))

        generate_yearly_report(maximum_temperature, minimum_temperature, maximum_humidity)
        weather_record_subset.clear()

    if args.average:
        year, month = args.average[0]
        single_month = f'{year}-{month}'

        for record in weather_records:
            if single_month in record.date:
                weather_record_subset.append(record)

        avg_maximum_temp = round(sum(int(DayForecast.max_temp)
                                     for DayForecast in weather_record_subset) / len(weather_record_subset))

        avg_minimum_temp = round(sum(int(DayForecast.min_temp)
                                     for DayForecast in weather_record_subset) / len(weather_record_subset))

        avg_mean_humidity = round(sum(int(DayForecast.mean_humidity)
                                      for DayForecast in weather_record_subset) / len(weather_record_subset))

        generate_monthly_report(avg_maximum_temp, avg_minimum_temp, avg_mean_humidity)
        weather_record_subset.clear()

    if args.chart:
        day_index = 1
        year, month = args.chart[0]
        single_month = f'{year}-{month}'
        choice = input("1. Single chart\n2. Separate charts\n")

        print(cal.month_name[int(month)], year)
        for record in weather_records:
            if single_month in record.date:
                display_bar_charts(day_index, record.min_temp, record.max_temp, int(choice))
                day_index += 1


def main(arguments):
    weather_records = parse_files(arguments.directory)
    calculate_results(arguments, weather_records)


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
