"""Weatherman

is a program to populate different statictics and graphs about weather
history.
"""
import sys
import calendar
import operator
from datetime import datetime


class Weather(object):

    def __init__(self, weather_fields_line):
        self.date = ''
        self.max_temperature_c = ''
        self.mean_temperature_c = ''
        self.min_temperature_c = ''
        self.max_humidity = ''
        self.mean_humidity = ''
        self.min_humidity = ''
        self._parse_weather_fields_line(weather_fields_line)

    def _parse_weather_fields_line(self, weather_fields_line):
        weather_fields = weather_fields_line.split(',')
        self.date = weather_fields[0]
        self.max_temperature_c = weather_fields[1]
        self.mean_temperature_c = weather_fields[2]
        self.min_temperature_c = weather_fields[3]
        self.max_humidity = weather_fields[7]
        self.mean_humidity = weather_fields[8]
        self.min_humidity = weather_fields[9]


class WeatherReport(object):

    def __init__(self, path_to_weather_files, type_, year, months):
        self.weather_data_for_year = {}
        self.highest_temperature = {}
        self.lowest_temperature = {}
        self.highest_humidity = {}
        self.year = year
        self.months = months

        self._get_and_store_weather_data_form_files(path_to_weather_files)
        self._generate_weather_report(type_)

    def _get_and_store_weather_data_form_files(self, path_to_weather_files,):
        for month in self.months:
            weather_file_path = (path_to_weather_files
                                 + '/Murree_weather_'
                                 + self.year + '_'
                                 + calendar.month_abbr[month] + '.txt')
            weather_file_in = open(weather_file_path, 'r')
            weather_fields_lines = weather_file_in.readlines()
            for line_number in range(1, len(weather_fields_lines)):
                a_day_weather = Weather(weather_fields_lines[line_number])
                self.weather_data_for_year[a_day_weather.date] = a_day_weather

    def _generate_weather_report(self, type_):
        if type_ == '-e':
            self._etype_weather_report()

    def _etype_weather_report(self):
        self._calculate_highest_temperature()
        self._calculate_lowest_temperature()
        print('Highest: {:0>2}C on {:%B %d}'.format(self.highest_temperature['temperature'],
                                                    datetime.strptime(self.highest_temperature['day'],
                                                                      '%Y-%m-%d'),
                                                    ))
        print('Lowest: {:0>2}C on {:%B %d}'.format(self.lowest_temperature['temperature'],
                                                    datetime.strptime(self.lowest_temperature['day'],
                                                                      '%Y-%m-%d'),
                                                    ))

    def _calculate_highest_temperature(self):
        hightest_temp_weather_data = max(self.weather_data_for_year.values(),
                                         key=operator.attrgetter('max_temperature_c'))
        self.highest_temperature['day'] = hightest_temp_weather_data.date
        self.highest_temperature['temperature'] = hightest_temp_weather_data.max_temperature_c

    def _calculate_lowest_temperature(self):
        lowest_temp_weather_data = max(self.weather_data_for_year.values(),
                                       key=operator.attrgetter('min_temperature_c'),
                                       )
        self.lowest_temperature['day'] = lowest_temp_weather_data.date
        self.lowest_temperature['temperature'] = lowest_temp_weather_data.max_temperature_c


def main():
    path_to_weather_files = sys.argv[1]
    for arg_number in range(2, len(sys.argv), 2):
        year_month = sys.argv[arg_number + 1].split('/')
        year = year_month[0]
        months = []
        if len(year_month) == 2:
            months.append(year_month[1])
        else:
            months = list(range(1, 13))  # no month is given , so we include all 12
        WeatherReport(path_to_weather_files, sys.argv[arg_number],
                                         year, months)


main()
