"""Weatherman

is a program to populate different statictics and graphs about weather
history.
"""

import argparse
import calendar
import operator
import sys
from datetime import datetime

from colorama import Fore, Style


class WeatherRecord(object):
    def __init__(self, date, max_temperature_c, mean_temperature_c,
                 min_temperature_c, max_humidity, mean_humidity, min_humidity):
        self.date = date
        self.max_temperature_c = max_temperature_c
        self.mean_temperature_c = mean_temperature_c
        self.min_temperature_c = min_temperature_c
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.min_humidity = min_humidity

    @classmethod
    def parse_weather_fields_line(cls, weather_fields_line):
        weather_fields = weather_fields_line.split(',')
        weather_record = cls(date=datetime.strptime(weather_fields[0], '%Y-%m-%d'),
                             max_temperature_c=cls.convert_str_to_int(weather_fields[1]),
                             mean_temperature_c=cls.convert_str_to_int(weather_fields[2]),
                             min_temperature_c=cls.convert_str_to_int(weather_fields[3]),
                             max_humidity=cls.convert_str_to_int(weather_fields[7]),
                             mean_humidity=cls.convert_str_to_int(weather_fields[8]),
                             min_humidity=cls.convert_str_to_int(weather_fields[9]),
                             )
        return weather_record

    @staticmethod
    def convert_str_to_int(number):
        try:
            return int(number)
        except ValueError:
            pass


class WeatherReport(object):
    def __init__(self, weather_data_all_days):
        self.weather_data_all_days = weather_data_all_days

    def print_extreme_weather_report(self):
        highest_temperature_day = self._get_highest_temperature_day()
        lowest_temperature_day = self._get_lowest_temperature_day()
        highest_humidity_day = self._get_highest_humidity_day()

        print('Highest: {:0>2d}C on {:%B %d}'.format(highest_temperature_day.max_temperature_c,
                                                     highest_temperature_day.date,
                                                     ))
        print('Lowest: {:0>2d}C on {:%B %d}'.format(lowest_temperature_day.min_temperature_c,
                                                    lowest_temperature_day.date,
                                                    ))
        print('Humidity: {:d}% on {:%B %d}'.format(highest_humidity_day.max_humidity,
                                                   highest_humidity_day.date,
                                                   ))

    def print_average_weather_report(self):
        average_highest_temperature = self._calculate_average_highest_temperature()
        average_lowest_temperature = self._calculate_average_lowest_temperature()
        average_mean_humidity = self._calculate_average_mean_humidity()

        print('Highest Average: {:.0f}%'.format(average_highest_temperature))
        print('Lowest Average: {:.0f}%'.format(average_lowest_temperature))
        print('Average Mean Humidity: {:.0f}%'.format(average_mean_humidity))

    @staticmethod
    def get_bar_for_chart(number):
        if number > 0:
            return '+' * number
        else:
            return '-' * abs(number)

    def print_weather_report_chart_1(self):
        print('{:%B %Y}'.format(self.weather_data_all_days[0].date))
        for a_day_weather in self.weather_data_all_days:
            if a_day_weather.max_temperature_c is not None:
                print(Fore.RED + '{:%d} {bar} {temperature}C'.format(
                    a_day_weather.date,
                    bar=self.get_bar_for_chart(a_day_weather.max_temperature_c),
                    temperature=a_day_weather.max_temperature_c))
            if a_day_weather.min_temperature_c is not None:
                print(Fore.BLUE + '{:%d} {bar} {temperature}c'.format(
                    a_day_weather.date,
                    bar=self.get_bar_for_chart(a_day_weather.min_temperature_c),
                    temperature=a_day_weather.min_temperature_c))
        print(Style.RESET_ALL)

    def print_weather_report_chart_2(self):
        print('{:%B %Y}'.format(self.weather_data_all_days[0].date))
        for a_day_weather in self.weather_data_all_days:
            if a_day_weather.max_temperature_c is not None and a_day_weather.min_temperature_c is not None:
                bar = self.get_bar_for_chart(abs(a_day_weather.max_temperature_c)
                                             + abs(a_day_weather.min_temperature_c))
                print('{:%d} {bar}'.format(a_day_weather.date, bar=bar), end='')
                print(Fore.BLUE + ' {tempe_low}C '.format(tempe_low=a_day_weather.min_temperature_c), end='')
                print(Fore.RED + ' - {temp_high}C'.format(temp_high=a_day_weather.max_temperature_c))
                print(Style.RESET_ALL)

    def _get_highest_temperature_day(self):
        highest_temperature_day = max(self.weather_data_all_days,
                                      key=operator.attrgetter('max_temperature_c'))
        return highest_temperature_day

    def _get_lowest_temperature_day(self):
        lowest_temperature_day = min(self.weather_data_all_days,
                                     key=operator.attrgetter('min_temperature_c'))
        return lowest_temperature_day

    def _get_highest_humidity_day(self):
        highest_humidity_day = max(self.weather_data_all_days,
                                   key=operator.attrgetter('max_humidity'))
        return highest_humidity_day

    def _calculate_average_highest_temperature(self):
        sum_temperature = 0
        record_count = 0
        for a_day_weather in self.weather_data_all_days:
            if a_day_weather.max_temperature_c:
                sum_temperature += a_day_weather.max_temperature_c
                record_count += 1
        average_highest_temperature = sum_temperature / record_count
        return average_highest_temperature

    def _calculate_average_lowest_temperature(self):
        sum_temperature = 0
        record_count = 0
        for a_day_weather in self.weather_data_all_days:
            if a_day_weather.min_temperature_c:
                sum_temperature += a_day_weather.min_temperature_c
                record_count += 1
        average_lowest_temperature = sum_temperature / record_count
        return average_lowest_temperature

    def _calculate_average_mean_humidity(self):
        sum_humidity = 0
        record_count = 0
        for a_day_weather in self.weather_data_all_days:
            if a_day_weather.mean_humidity:
                sum_humidity += a_day_weather.mean_humidity
                record_count += 1
        average_mean_humidity = sum_humidity / record_count
        return average_mean_humidity


def get_weather_record_form_files(path_to_weather_files, year, months=list(range(1, 13))):
    weather_records = []

    for month in months:
        weather_file_path = ('{dir}/Murree_weather_{year}_{month}.txt'.format(dir=path_to_weather_files,
                                                                              year=year,
                                                                              month=calendar.month_abbr[month]))

        try:
            with open(weather_file_path, 'r') as (weather_file_in):
                weather_file_in.readline()  # neglecting first line
                for weather_record_line in weather_file_in:
                    a_day_weather = WeatherRecord.parse_weather_fields_line(weather_record_line)
                    weather_records.append(a_day_weather)
        except FileNotFoundError:
            print("source is not corrector. Use -h option for help", file=sys.stderr)
            sys.exit(1)

    return weather_records


def is_valid_year_range(year):
    return 2004 <= year <= 2015


def valid_year(year):
    try:
        date = datetime.strptime(year, "%Y")
        if is_valid_year_range(date.year):
            return date
        msg = "use a valid year range"
        raise argparse.ArgumentTypeError(msg)
    except ValueError:
        msg = "Not a valid year: '{0}' (try format: YYYY).".format(year)
        raise argparse.ArgumentTypeError(msg)


def valid_month(month):
    try:
        date = datetime.strptime(month, "%Y/%m")
        if is_valid_year_range(date.year):
            return date
        msg = "use a valid year"
        raise argparse.ArgumentTypeError(msg)
    except ValueError:
        msg = "Not a valid date: '{0}' (try format: YYYY/MM).".format(month)
        raise argparse.ArgumentTypeError(msg)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('source', help='Path to weather data files')
    parser.add_argument('-e', '--extreme', type=valid_year,
                        help='Display extreme weather report for given year(format: YYYY)')
    parser.add_argument('-a', '--average', type=valid_month,
                        help='Display average weather report for given month(format: YYYY/MM)')
    parser.add_argument('-c', '--chart', type=valid_month,
                        help='Display char weather report for given month(format: YYYY/MM)')
    parser.add_argument('-m', '--mergedchart', type=valid_month,
                        help='Display merged char weather report for given month(format: YYYY/MM)')

    args = parser.parse_args()

    if not any((args.extreme, args.average, args.chart, args.mergedchart)):
        print("Give at least one argument or use -h option for help", file=sys.stderr)
        sys.exit(1)

    if args.extreme:
        weather_records = get_weather_record_form_files(args.source, year=args.extreme.year)
        weather_report = WeatherReport(weather_records)
        weather_report.print_extreme_weather_report()

    if args.average:
        weather_records = get_weather_record_form_files(args.source, args.average.year, [args.average.month])
        weather_report = WeatherReport(weather_records)
        weather_report.print_average_weather_report()

    if args.chart:
        weather_records = get_weather_record_form_files(args.source, args.chart.year, [args.chart.month])
        weather_report = WeatherReport(weather_records)
        weather_report.print_weather_report_chart_1()

    if args.mergedchart:
        weather_records = get_weather_record_form_files(args.source, args.chart.year, [args.chart.month])
        weather_report = WeatherReport(weather_records)
        weather_report.print_weather_report_chart_2()


if __name__ == '__main__':
    main()
