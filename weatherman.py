from operator import attrgetter
from time import strptime
from calendar import month_name
from datetime import date as get_date
import csv
import argparse
import glob as gb
import os


class DayForecast:

    def __init__(self, day_record):
        temp_date = day_record.get('PKT') or day_record.get('PKST')
        temp_date = list(map(int, temp_date.split("-")))
        self.date = get_date(temp_date[0], temp_date[1], temp_date[2])
        self.max_temp = int(day_record['Max TemperatureC'])
        self.min_temp = int(day_record['Min TemperatureC'])
        self.max_humidity = int(day_record['Max Humidity'])
        self.mean_humidity = int(day_record[' Mean Humidity'])


def print_blue(text, n):
    print("\033[96m{}\033[00m".format(text) * n, end="")


def print_red(text, n):
    print("\033[31m{}\033[00m".format(text) * n, end="")


def validate_year(date):
    try:
        date = strptime(date, "%Y")
        return date.tm_year
    except ValueError:
        msg = "Invalid input. Use format YYYY: '{0}'.".format(date)
        raise argparse.ArgumentTypeError(msg)


def validate_date(date):
    try:
        date = strptime(date, "%Y/%m")
        return date.tm_year, date.tm_mon
    except ValueError:
        msg = "Not a valid date. Should be YYYY/MM: '{0}'.".format(date)
        raise argparse.ArgumentTypeError(msg)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="Directory to all weather files", type=str)
    parser.add_argument("-c", "--chart",
                        help="Display bar charts for provided month in C (YY/MM)",
                        action="append",
                        type=validate_date)
    parser.add_argument("-a", "--average",
                        help="Calculate average of max temp, min temp, mean humidity for month in A (YY/MM)",
                        action="append",
                        type=validate_date)
    parser.add_argument("-e", "--extreme",
                        help="Calculate max temp, humidity and min temp for year E (YY)",
                        action="append",
                        type=validate_year)
    return parser.parse_args()


def parse_files(directory):
    weather_records = []
    os.chdir(directory)

    for file in gb.glob("*.txt"):
        weather_file = open(file, "r")
        reader = csv.DictReader(weather_file)

        for row in reader:
            weather_records.append(row)

    return weather_records


def clean_weather_records(weather_records):
    clean_records = []
    weather_records = list(filter(lambda record: record.get('Max TemperatureC') and
                                                 record.get('Min TemperatureC') and
                                                 record.get('Max Humidity') and
                                                 record.get(' Mean Humidity'), weather_records))
    for record in weather_records:
        clean_records.append(DayForecast(record))
    return clean_records


def calculate_results(args, weather_records):
    if args.extreme:
        generate_yearly_report(args.extreme[0], weather_records)

    if args.average:
        generate_monthly_report(args.average[0], weather_records)

    if args.chart:
        generate_bar_charts(args.chart[0], weather_records)


def generate_yearly_report(year, weather_records):
    year_records = []

    for record in weather_records:
        if year == record.date.year:
            year_records.append(record)

    if len(year_records) > 0:
        maximum_temperature = max(year_records, key=attrgetter('max_temp'))
        minimum_temperature = min(year_records, key=attrgetter('min_temp'))
        maximum_humidity = max(year_records, key=attrgetter('max_humidity'))

        display_yearly_report(maximum_temperature, minimum_temperature, maximum_humidity)
    else:
        print(f'\nNo record for year {year} present')


def generate_monthly_report(date, weather_records):
    month_records = []

    for record in weather_records:
        if date[0] == record.date.year and date[1] == record.date.month:
            month_records.append(record)

    if len(month_records) > 0:
        avg_maximum_temp = round(sum(DayForecast.max_temp
                                     for DayForecast in month_records) / len(month_records))
        avg_minimum_temp = round(sum(DayForecast.min_temp
                                     for DayForecast in month_records) / len(month_records))
        avg_mean_humidity = round(sum(DayForecast.mean_humidity
                                      for DayForecast in month_records) / len(month_records))
        display_monthly_report(avg_maximum_temp, avg_minimum_temp, avg_mean_humidity)
    else:
        print(f'\nNo record for {month_name[date[1]]} {date[0]} present')


def generate_bar_charts(date, weather_records):
    choice = input("\n1. Single chart\n2. Separate charts\n")
    print(f'\n{month_name[date[1]]} {date[0]}')

    for record in weather_records:
        if date[0] == record.date.year and date[1] == record.date.month:
            display_bar_charts(record.date.day, record.min_temp,
                               record.max_temp, int(choice))


def display_yearly_report(maximum_temp, minimum_temp, maximum_humidity):
    print(f'\nHighest: {maximum_temp.max_temp}C on {maximum_temp.date:%B %d}')
    print(f'Lowest: {minimum_temp.min_temp}C on {minimum_temp.date:%B %d}')
    print(f'Humidity: {maximum_humidity.max_humidity}% on {maximum_humidity.date:%B %d}')


def display_monthly_report(avg_maximum_temp, avg_minimum_temp, avg_mean_humidity):
    print(f'\nHighest Average: {avg_maximum_temp}C')
    print(f'Lowest Average: {avg_minimum_temp}C')
    print(f'Average Mean Humidity: {avg_mean_humidity}C')


def display_bar_charts(day, minimum_temp, maximum_temp, user_choice):
    print("%d " % day, end="")
    if user_choice == 1:
        print_blue("+", minimum_temp)
        print_red("+", maximum_temp)
        print(" %dC - %dC" % (minimum_temp, maximum_temp))

    elif user_choice == 2:
        print_red("+", maximum_temp)
        print(" %dC" % maximum_temp)

        print("%d " % day, end="")
        print_blue("+", minimum_temp)
        print(" %dC" % minimum_temp)


def main(arguments):
    weather_records = parse_files(arguments.directory)
    weather_records = clean_weather_records(weather_records)
    calculate_results(arguments, weather_records)


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
