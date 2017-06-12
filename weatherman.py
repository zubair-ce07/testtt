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

    invalid_field_value=-273

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
    def __init__(self, path_to_weather_files, type_, year, months):
        self.weather_data_all_day = []
        self.highest_temperature_day = None
        self.lowest_temperature_day = None
        self.highest_humidity_day = None
        self.average_highest_temperature = None
        self.average_lowest_temperature = None
        self.average_mean_humidity = None
        self.year = year
        self.months = months

        self._get_and_store_weather_data_form_files(path_to_weather_files)
        self._generate_weather_report(type_)

    def _get_and_store_weather_data_form_files(self, path_to_weather_files, ):
        for month in self.months:
            weather_file_path = (path_to_weather_files
                                 + '/Murree_weather_'
                                 + self.year + '_'
                                 + calendar.month_abbr[month] + '.txt')
            weather_file_in = open(weather_file_path, 'r')
            weather_fields_lines = weather_file_in.readlines()
            for line_number in range(1, len(weather_fields_lines)):
                a_day_weather = Weather(weather_fields_lines[line_number])
                self.weather_data_all_day.append(a_day_weather)

    def _generate_weather_report(self, type_):
        if type_ == '-e':
            self._etype_weather_report()
        elif type_ == '-a':
            self._atype_weather_report()
        elif type_ == '-c':
            self._ctype_weather_report()
        elif type_ == '-p':
            self._ptype_weather_report()

    def _etype_weather_report(self):
        self._calculate_highest_temperature()
        self._calculate_lowest_temperature()
        self._calculate_highest_humidity()

    def _atype_weather_report(self):
        self._calculate_average_highest_temperature()
        self._calculate_average_lowest_temperature()
        self._calculate_average_mean_humidity()

    def _ctype_weather_report(self):
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

    def _ptype_weather_report(self):
        print('{:%B %Y}'.format(self.weather_data_all_day[0].date))
        for a_day_weather in self.weather_data_all_day:
            if not (a_day_weather.max_temperature_c == Weather.invalid_field_value
                    or a_day_weather.min_temperature_c == Weather.invalid_field_value):
                bar = '+' * (abs(a_day_weather.max_temperature_c) + abs(a_day_weather.min_temperature_c))
                print('{:%d} {bar}'.format(a_day_weather.date, bar=bar), end='')
                print(Fore.BLUE + ' {tempe_low}C '.format(tempe_low=a_day_weather.min_temperature_c), end='')
                print(Fore.RED + ' - {temp_high}C'.format(temp_high=a_day_weather.max_temperature_c))
                print(Style.RESET_ALL)

    def _calculate_highest_temperature(self):
        self.highest_temperature_day = max(self.weather_data_all_day,
                                           key=operator.attrgetter('max_temperature_c'))
        print('Highest: {:0>2d}C on {:%B %d}'.format(self.highest_temperature_day.max_temperature_c,
                                                     self.highest_temperature_day.date,
                                                     ))

    def _calculate_lowest_temperature(self):
        self.lowest_temperature_day = min(self.weather_data_all_day,
                                          key=operator.attrgetter('min_temperature_c'))
        print('Lowest: {:0>2d}C on {:%B %d}'.format(self.lowest_temperature_day.min_temperature_c,
                                                    self.lowest_temperature_day.date,
                                                    ))

    def _calculate_highest_humidity(self):
        self.highest_humidity_day = max(self.weather_data_all_day,
                                        key=operator.attrgetter('max_humidity'))
        print('Humidity: {:d}% on {:%B %d}'.format(self.highest_humidity_day.max_humidity,
                                                   self.highest_humidity_day.date,
                                                   ))

    def _calculate_average_highest_temperature(self):
        sum_temperature = 0
        record_count = 0
        for a_day_weather in self.weather_data_all_day:
            if not a_day_weather.max_temperature_c == Weather.invalid_field_value:
                sum_temperature += a_day_weather.max_temperature_c
                record_count += 1
        self.average_highest_temperature = sum_temperature / record_count
        print('Highest Average: {:.0f}%'.format(self.average_highest_temperature))

    def _calculate_average_lowest_temperature(self):
        sum_temperature = 0
        record_count = 0
        for a_day_weather in self.weather_data_all_day:
            if not a_day_weather.min_temperature_c == Weather.invalid_field_value:
                sum_temperature += a_day_weather.min_temperature_c
                record_count += 1
        self.average_lowest_temperature = sum_temperature / record_count
        print('Lowest Average: {:.0f}%'.format(self.average_lowest_temperature))

    def _calculate_average_mean_humidity(self):
        sum_humidity = 0
        record_count = 0
        for a_day_weather in self.weather_data_all_day:
            if not a_day_weather.mean_humidity == Weather.invalid_field_value:
                sum_humidity += a_day_weather.mean_humidity
                record_count += 1
        self.average_mean_humidity = sum_humidity / record_count
        print('Average Mean Humidity: {:.0f}%'.format(self.average_mean_humidity))


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
        WeatherReport(path_to_weather_files, sys.argv[arg_number],
                      year, months)


if __name__ == '__main__':
    main()
