import argparse
import csv
import re
from datetime import datetime
from glob import glob
from os import path

from weatherman_ds import WeatherReading
from weatherman_calculation import WeatherReport


def main():
    parser = argparse.ArgumentParser(description='A program that calculates '
                                                 'weather information and'
                                                 ' visualizes it.')

    parser.add_argument('directory', help='this argument provides the application '
                        'directory where weather records are available.',
                        type=directory_validate)
    parser.add_argument('-e', '--extreme', help='this option display a report of extreme readings'
                        'of the year provided.', type=year_validate)
    parser.add_argument('-a', '--average', help='this option display a report of average readings'
                        'of a month provided.', type=month_validate)
    parser.add_argument('-c', '--chart', help='this option displays a horizontal bar chart of high and low'
                        'temperature of the month provided.', type=month_validate)

    args = parser.parse_args()

    weather_records = load_weather_records(args.directory)
    if args.extreme:
        extremes_for_year(weather_records, args.extreme)
    if args.average:
        average_for_month(weather_records, args.average)
    if args.chart:
        chart_for_month(weather_records, args.chart)


def load_weather_records(directory):
    directory = glob(f"{directory}/*.txt")
    weather_records = []
    for record_file in directory:
        with open(record_file, 'r') as csv_file:
            weather_record = csv.DictReader(csv_file)
            for row in weather_record:
                weather_records.append(WeatherReading(row))
    return weather_records


def extremes_for_year(weather_records, year):
    weather_records = records_filter_year(weather_records, year)
    if weather_records:
        year_weather_result = WeatherReport.calculate_extreme_for_year(weather_records)
        weather_report_extreme(year_weather_result)
    else:
        print(f"Records not available for {year}")


def average_for_month(weather_records, month):
    weather_records = records_filter_month(weather_records, month)
    if weather_records:
        year_weather_result = WeatherReport.calculate_average_for_month(weather_records)
        weather_report_average(year_weather_result)
    else:
        print(f"Records not available for {month}")


def chart_for_month(weather_records, month):
    weather_records = records_filter_month(weather_records, month)
    if weather_records:
        weather_report_chart(weather_records, month)
    else:
        print(f"Records not available for {month}")


def records_filter_month(weather_records, month):
    month = datetime.strptime(month, '%Y/%m')
    filtered_records = list(filter(lambda day: day.pkt.year == month.year
                            and day.pkt.month == month.month, weather_records))
    return filtered_records


def records_filter_year(weather_records, year):
    year = datetime.strptime(year, '%Y')
    filtered_records = list(filter(lambda day: day.pkt.year == year.year, weather_records))
    return filtered_records


def weather_report_extreme(year_extreme):
    """"Displays the highest lowest temperature and highest humidity report"""
    print(f"Highest: {year_extreme.highest_reading}C on {year_extreme.highest_day:%B %d}")
    print(f"Lowest: {year_extreme.lowest_reading}C on {year_extreme.lowest_day:%B %d}")
    print(f"Humidity: {year_extreme.humidity_reading}% on {year_extreme.humidity_day:%B %d}")


def weather_report_average(month_average):
    """Displays the average highest lowest temperature and humidity of a month"""
    print(f"Highest Average: {month_average.highest_reading}C")
    print(f"Lowest Average: {month_average.lowest_reading}C")
    print(f"Average mean humidity: {month_average.humidity_reading}%")


def weather_report_chart(weather_records, month):
    """"Displays the bar chart for temperatures through the month"""
    def repeat_plus(x): return '+' * x

    month = datetime.strptime(month, "%Y/%m")
    print(f"{month:%B %Y}")
    for day, record in enumerate(weather_records, start=1):
        if record.max_temperature and record.min_temperature:
            print(f"{day:{0}{2}}{ColorOutput.BLUE}{repeat_plus(record.min_temperature)}"
                  f"{ColorOutput.RED}{repeat_plus(record.max_temperature)}"
                  f"{ColorOutput.RESET}{record.min_temperature}C-{record.max_temperature}C")


def year_validate(year):
    if re.match('\d{4}$', year):
        return year
    raise argparse.ArgumentTypeError(f"{year} is invalid format please enter yyyy")


def month_validate(month):
    if re.match('\d{4}/\d{1,2}$', month):
        return month
    raise argparse.ArgumentTypeError(f"{month} is invalid format please enter yyyy/mm")


def directory_validate(directory):
    if path.exists(directory):
        return directory
    raise argparse.ArgumentTypeError(f"{directory} is invalid directory")


class ColorOutput:
    RED = "\033[31m"
    BLUE = "\033[34m"
    RESET = "\033[0m"


if __name__ == '__main__':
    main()
