"""Weatherman

is a program to populate different statictics and graphs about weather
history.
"""
import calendar
import operator
import sys
from datetime import datetime

from colorama import Fore, Style


class Weather(object):
    invalid_field_value = -273

    def __init__(self, weather_fields_line):
        self.date = None
        self.max_temperature_c = 0
        self.mean_temperature_c = 0
        self.min_temperature_c = 0
        self.max_humidity = 0
        self.mean_humidity = 0
        self.min_humidity = 0
        self._parse_weather_fields_line(weather_fields_line)

    def _parse_weather_fields_line(self, weather_fields_line):
        weather_fields = weather_fields_line.split(',')
        self.date = datetime.strptime(weather_fields[0], '%Y-%m-%d')
        self.max_temperature_c = self.convert_str_to_int(weather_fields[1])
        self.mean_temperature_c = self.convert_str_to_int(weather_fields[2])
        self.min_temperature_c = self.convert_str_to_int(weather_fields[3])
        self.max_humidity = self.convert_str_to_int(weather_fields[7])
        self.mean_humidity = self.convert_str_to_int(weather_fields[8])
        self.min_humidity = self.convert_str_to_int(weather_fields[9])

    def convert_str_to_int(self, number):
        try:
            return int(number)
        except ValueError:
            return self.invalid_field_value


class WeatherReport(object):
    def __init__(self, path_to_weather_files, year, months):
        self.weather_data_all_day = []

        self._get_and_store_weather_data_form_files(path_to_weather_files, year, months)

    def _get_and_store_weather_data_form_files(self, path_to_weather_files, year, months):
        for month in months:
            weather_file_path = (path_to_weather_files
                                 + '/Murree_weather_'
                                 + year + '_'
                                 + calendar.month_abbr[month] + '.txt')
            weather_file_in = open(weather_file_path, 'r')
            weather_fields_lines = weather_file_in.readlines()
            for line_number in range(1, len(weather_fields_lines)):
                a_day_weather = Weather(weather_fields_lines[line_number])
                self.weather_data_all_day.append(a_day_weather)

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

    def print_weather_report_chart_1(self):
        print('{:%B %Y}'.format(self.weather_data_all_day[0].date))
        for a_day_weather in self.weather_data_all_day:
            if not a_day_weather.max_temperature_c == Weather.invalid_field_value:
                print(Fore.RED + '{:%d} {bar} {temperature}C'.format(
                    a_day_weather.date,
                    bar='+' * abs(a_day_weather.max_temperature_c),
                    temperature=a_day_weather.max_temperature_c))
            if not a_day_weather.min_temperature_c == Weather.invalid_field_value:
                print(Fore.BLUE + '{:%d} {bar} {temperature}c'.format(
                    a_day_weather.date,
                    bar='+' * abs(a_day_weather.min_temperature_c),
                    temperature=a_day_weather.min_temperature_c))
        print(Style.RESET_ALL)

    def print_weather_report_chart_2(self):
        print('{:%B %Y}'.format(self.weather_data_all_day[0].date))
        for a_day_weather in self.weather_data_all_day:
            if not (a_day_weather.max_temperature_c == Weather.invalid_field_value
                    or a_day_weather.min_temperature_c == Weather.invalid_field_value):
                bar = '+' * (abs(a_day_weather.max_temperature_c) + abs(a_day_weather.min_temperature_c))
                print('{:%d} {bar}'.format(a_day_weather.date, bar=bar), end='')
                print(Fore.BLUE + ' {tempe_low}C '.format(tempe_low=a_day_weather.min_temperature_c), end='')
                print(Fore.RED + ' - {temp_high}C'.format(temp_high=a_day_weather.max_temperature_c))
                print(Style.RESET_ALL)

    def _get_highest_temperature_day(self):
        highest_temperature_day = max(self.weather_data_all_day,
                                      key=operator.attrgetter('max_temperature_c'))
        return highest_temperature_day

    def _get_lowest_temperature_day(self):
        lowest_temperature_day = min(self.weather_data_all_day,
                                     key=operator.attrgetter('min_temperature_c'))
        return lowest_temperature_day

    def _get_highest_humidity_day(self):
        highest_humidity_day = max(self.weather_data_all_day,
                                   key=operator.attrgetter('max_humidity'))
        return highest_humidity_day

    def _calculate_average_highest_temperature(self):
        sum_temperature = 0
        record_count = 0
        for a_day_weather in self.weather_data_all_day:
            if not a_day_weather.max_temperature_c == Weather.invalid_field_value:
                sum_temperature += a_day_weather.max_temperature_c
                record_count += 1
        average_highest_temperature = sum_temperature / record_count
        return average_highest_temperature

    def _calculate_average_lowest_temperature(self):
        sum_temperature = 0
        record_count = 0
        for a_day_weather in self.weather_data_all_day:
            if not a_day_weather.min_temperature_c == Weather.invalid_field_value:
                sum_temperature += a_day_weather.min_temperature_c
                record_count += 1
        average_lowest_temperature = sum_temperature / record_count
        return average_lowest_temperature

    def _calculate_average_mean_humidity(self):
        sum_humidity = 0
        record_count = 0
        for a_day_weather in self.weather_data_all_day:
            if not a_day_weather.mean_humidity == Weather.invalid_field_value:
                sum_humidity += a_day_weather.mean_humidity
                record_count += 1
        average_mean_humidity = sum_humidity / record_count
        return average_mean_humidity


def generate_weather_report(weather_report, flag):
    if flag == '-e':
        weather_report.print_extreme_weather_report()
    elif flag == '-a':
        weather_report.print_average_weather_report()
    elif flag == '-c':
        weather_report.print_weather_report_chart_1()
    elif flag == '-p':
        weather_report.print_weather_report_chart_2()


def main():
    path_to_weather_files = sys.argv[1]
    for arg_number in range(2, len(sys.argv), 2):
        year_month = sys.argv[arg_number + 1].split('/')
        year = year_month[0]
        months = []
        if len(year_month) == 2:
            months.append(int(year_month[1]))
        else:
            months = list(range(1, 13))  # no month is given , so we include all 12

        weather_report = WeatherReport(path_to_weather_files, year, months)
        generate_weather_report(weather_report, flag=sys.argv[arg_number])


if __name__ == '__main__':
    main()
