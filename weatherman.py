import csv
import argparse
import glob as gb

from operator import attrgetter
from calendar import month_name
from datetime import datetime


class DayForecast:

    def __init__(self, day_record):
        temp_date = day_record.get('PKT') or day_record.get('PKST')
        self.date = datetime.strptime(temp_date, '%Y-%m-%d')
        self.max_temp = int(day_record['Max TemperatureC'])
        self.min_temp = int(day_record['Min TemperatureC'])
        self.max_humidity = int(day_record['Max Humidity'])
        self.mean_humidity = int(day_record[' Mean Humidity'])


def print_in_blue(text, n):
    print(f'\033[96m{text}\033[00m' * n, end='')


def print_in_red(text, n):
    print(f'\033[31m{text}\033[00m' * n, end='')


def validate_year(date):
    try:
        date = datetime.strptime(date, "%Y")
        return date.year
    except ValueError:
        msg = f'Not a valid year {date}. Use format YYYY'
        raise argparse.ArgumentTypeError(msg)


def validate_date(date):
    try:
        date = datetime.strptime(date, "%Y/%m")
        return date.year, date.month
    except ValueError:
        msg = f'Not a valid date {date}. Use format YYYY/MM:'
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

    for file_name in gb.glob(f'{directory}/*.txt'):
        with open(file_name) as weather_file:
            reader = csv.DictReader(weather_file)
            weather_records += [row for row in reader]

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
        display_yearly_report(generate_yearly_report(args.extreme[0], weather_records))

    if args.average:
        display_monthly_report(generate_monthly_report(args.average[0], weather_records))

    if args.chart:
        generate_bar_charts(args.chart[0], weather_records)


def generate_yearly_report(year, weather_records):
    year_records = list(filter(lambda record: record.date.year == year, weather_records))

    if year_records:
        return [max(year_records, key=attrgetter('max_temp')),
                min(year_records, key=attrgetter('min_temp')),
                max(year_records, key=attrgetter('max_humidity'))]


def generate_monthly_report(date, weather_records):
    month_records = list(filter(lambda record: record.date.year == date[0] and
                                               record.date.month == date[1], weather_records))
    if month_records:
        return [round(sum(DayForecast.max_temp for DayForecast in month_records) / len(month_records)),
                round(sum(DayForecast.min_temp for DayForecast in month_records) / len(month_records)),
                round(sum(DayForecast.mean_humidity for DayForecast in month_records) / len(month_records))]


def generate_bar_charts(date, weather_records):
    choice = input(f'\n1. Single chart\n2. Separate charts\n')
    print(f'\n{month_name[date[1]]} {date[0]}')

    for record in weather_records:
        if date[0] == record.date.year and date[1] == record.date.month:
            display_bar_charts(record.date.day, record.min_temp,
                               record.max_temp, int(choice))


def display_yearly_report(yearly_results):
    if yearly_results:
        print(f'\nHighest: {yearly_results[0].max_temp}C on {yearly_results[0].date:%B %d}')
        print(f'Lowest: {yearly_results[1].min_temp}C on {yearly_results[1].date:%B %d}')
        print(f'Humidity: {yearly_results[2].max_humidity}% on {yearly_results[2].date:%B %d}')
    else:
        print(f'\nNo yearly record')


def display_monthly_report(monthly_results):
    if monthly_results:
        print(f'\nHighest Average: {monthly_results[0]}C')
        print(f'Lowest Average: {monthly_results[1]}C')
        print(f'Average Mean Humidity: {monthly_results[2]}C')
    else:
        print(f'\nNo monthly record')


def display_bar_charts(day, minimum_temp, maximum_temp, user_choice):
    print(f'{day} ', end='')
    if user_choice == 1:                        # 1 if the user wants to print Single bar chart
        print_in_blue("+", minimum_temp)
        print_in_red("+", maximum_temp)
        print(f' {minimum_temp}C - {maximum_temp}C')

    elif user_choice == 2:                      # 2 if the user wants to print Separate bar charts
        print_in_red("+", maximum_temp)
        print(f' {maximum_temp}C')
        print(f'{day} ', end='')
        print_in_blue("+", minimum_temp)
        print(f' {minimum_temp}C')


def main():
    args = parse_arguments()
    weather_records = parse_files(args.directory)
    weather_records = clean_weather_records(weather_records)
    calculate_results(args, weather_records)


if __name__ == '__main__':
    main()
