import argparse
import calendar
from dateutil import parser
from termcolor import colored
import csv
import re
import os


class WeatherMan:

    def __init__(self):
        self.weather_field_date = 'PKT'
        self.weather_field_temp_max = 'Max TemperatureC'
        self.weather_field_temp_min = 'Min TemperatureC'
        self.weather_field_humid_max = 'Max Humidity'
        self.weather_field_temp_mean = 'Mean TemperatureC'
        self.weather_field_humid_mean = 'Mean Humidity'

    def read_weather_files(self, file_path, year, month=None):
        weather_readings = []
        weather_fields = [self.weather_field_date, self.weather_field_temp_max, self.weather_field_temp_min,
                          self.weather_field_humid_max, self.weather_field_temp_mean, self.weather_field_humid_mean]
        if month:
            filename_pattern = '(?=.*{year})(?=.*{month}).*\.txt$'.format(year=year, month=month[:3])
        else:
            filename_pattern = '(?=.*{year}).*\.txt$'.format(year=year)

        for filename in os.listdir(file_path):
            if re.search(filename_pattern, filename, flags=re.IGNORECASE):
                with open('{path}/{filename}'.format(filename=filename, path=file_path)) as csvFile:
                    weather_records_reader = csv.DictReader(csvFile, fieldnames=weather_fields)
                    next(weather_records_reader)  # Skip header because first row in every file is empty
                    weather_readings.extend(list(weather_records_reader))

        return weather_readings

    def get_weather_readings(self, file_path, year, month=None):
        weather_readings = self.read_weather_files(file_path, year, month)

        if not weather_readings:
            print('No relevant weather data found.')

        return weather_readings

    @staticmethod
    def filter_empty_weather_readings(weather_readings, weather_field):
        return (weather_reading for weather_reading in weather_readings if weather_reading[weather_field])

    def display_highest_temp(self, weather_readings):
        cleaned_weather_readings = self.filter_empty_weather_readings(weather_readings, self.weather_field_temp_max)
        highest_temp_reading = max(cleaned_weather_readings,
                                   key=lambda weather_reading:
                                   int(weather_reading[self.weather_field_temp_max]))

        if highest_temp_reading[self.weather_field_date]:
            date = parser.parse(highest_temp_reading[self.weather_field_date])
            print('Highest Temperature: {temp}C on {month} {day}'.format(
                temp=highest_temp_reading[self.weather_field_temp_max],
                month=calendar.month_name[date.month],
                day=date.day))

    def display_lowest_temp(self, weather_readings):
        cleaned_weather_readings = self.filter_empty_weather_readings(weather_readings, self.weather_field_temp_min)
        lowest_temp_reading = min(cleaned_weather_readings,
                                  key=lambda weather_reading:
                                  int(weather_reading[self.weather_field_temp_min]))

        if lowest_temp_reading[self.weather_field_date]:
            date = parser.parse(lowest_temp_reading[self.weather_field_date])
            print('Lowest Temperature: {temp}C on {month} {day}'.format(
                temp=lowest_temp_reading[self.weather_field_temp_min],
                month=calendar.month_name[date.month],
                day=date.day))

    def display_highest_humidity(self, weather_readings):
        cleaned_weather_readings = self.filter_empty_weather_readings(weather_readings, self.weather_field_humid_max)
        highest_humid_reading = max(cleaned_weather_readings,
                                    key=lambda weather_reading:
                                    int(weather_reading[self.weather_field_humid_max]))

        if highest_humid_reading[self.weather_field_date]:
            date = parser.parse(highest_humid_reading[self.weather_field_date])
            print('Highest Humidity: {humidity}% on {month} {day}'.format(
                humidity=highest_humid_reading[self.weather_field_humid_max],
                month=calendar.month_name[date.month],
                day=date.day))

    def display_highest_lowest_temperature(self, file_path, year):
        if not all([file_path or year]):
            print('Please pass correct arguments.')
            return

        weather_readings = self.get_weather_readings(file_path, year)

        self.display_highest_temp(weather_readings)
        self.display_lowest_temp(weather_readings)
        self.display_highest_humidity(weather_readings)

    def display_highest_mean_temp(self, weather_readings):
        cleaned_weather_readings = self.filter_empty_weather_readings(weather_readings, self.weather_field_temp_mean)
        highest_mean_temp_reading = max(cleaned_weather_readings,
                                        key=lambda weather_reading:
                                        int(weather_reading[self.weather_field_temp_mean]))
        print('Highest Average Temperature: {highest_mean_temp}C'.format(
            highest_mean_temp=highest_mean_temp_reading[self.weather_field_temp_mean]))

    def display_lowest_mean_temp(self, weather_readings):
        cleaned_weather_readings = self.filter_empty_weather_readings(weather_readings, self.weather_field_temp_mean)
        lowest_mean_temp_reading = min(cleaned_weather_readings,
                                       key=lambda weather_reading:
                                       int(weather_reading[self.weather_field_temp_mean]))
        print('Lowest Average Temperature: {lowest_mean_temp}C'.format(
            lowest_mean_temp=lowest_mean_temp_reading[self.weather_field_temp_mean]))

    def display_highest_mean_humidity(self, weather_readings):
        cleaned_weather_readings = self.filter_empty_weather_readings(weather_readings, self.weather_field_humid_mean)
        highest_mean_humidity_reading = max(cleaned_weather_readings,
                                            key=lambda weather_reading:
                                            int(weather_reading[self.weather_field_humid_mean]))
        print('Highest Average Humidity: {highest_mean_humid}%'.format(
            highest_mean_humid=highest_mean_humidity_reading[self.weather_field_humid_mean]))

    def display_mean_temp_humidity(self, file_path, year, month):
        if not all([file_path or year or month]):
            print('Please pass correct arguments.')
            return

        weather_readings = self.get_weather_readings(file_path, year, calendar.month_name[month])

        self.display_highest_mean_temp(weather_readings)
        self.display_lowest_mean_temp(weather_readings)
        self.display_highest_mean_humidity(weather_readings)

    def print_two_bar_charts_record(self, day, temp, symbol, color):
        print('{day} '.format(day=day), end='')
        self.colored_print(temp, symbol, color)
        print(' {temperature}C'.format(temperature=temp))

    @staticmethod
    def colored_print(count, symbol, color):
        for index in range(int(count)):
            print(colored(symbol, color), end='')

    def display_two_bar_charts(self, file_path, year, month):
        if not all([file_path or year or month]):
            print('Please pass correct arguments.')
            return

        print('{month} {year}'.format(month=calendar.month_name[month], year=year))

        weather_readings = self.get_weather_readings(file_path, year, calendar.month_name[month])

        for weather_reading in weather_readings:
            try:
                day = parser.parse(weather_reading[self.weather_field_date]).day
            except ValueError:
                continue

            if weather_reading[self.weather_field_temp_max]:
                self.print_two_bar_charts_record(day, weather_reading[self.weather_field_temp_max], '+', 'red')

            if weather_reading[self.weather_field_temp_min]:
                self.print_two_bar_charts_record(day, weather_reading[self.weather_field_temp_min], '+', 'blue')

    def print_one_bar_chart(self, weather_reading):
        highest_temp = weather_reading[self.weather_field_temp_max]
        lowest_temp = weather_reading[self.weather_field_temp_min]

        if lowest_temp or highest_temp:
            print('{day} '.format(day=parser.parse(weather_reading[self.weather_field_date]).day), end='')

            if weather_reading[self.weather_field_temp_min]:
                self.colored_print(lowest_temp, '+', 'blue')

            if weather_reading[self.weather_field_temp_max]:
                self.colored_print(highest_temp, '+', 'red')

            print(' {lowest_temp}C-{highest_temp}C'.format(lowest_temp=lowest_temp, highest_temp=highest_temp))

    def display_one_bar_charts(self, file_path, year, month):
        if not all([file_path or year or month]):
            print('Please pass correct arguments.')
            return

        print('{month} {year}'.format(month=calendar.month_name[month], year=year))

        weather_readings = self.get_weather_readings(file_path, year, calendar.month_name[month])

        for weather_reading in weather_readings:
            self.print_one_bar_chart(weather_reading)


def main():
    weather_arg_parser = argparse.ArgumentParser()
    weather_arg_parser.add_argument('-e', nargs=2, dest='highest_lowest_temp')
    weather_arg_parser.add_argument('-a', nargs=2, dest='average')
    weather_arg_parser.add_argument('-c', nargs=2, dest='bar_chart')
    weather_args = weather_arg_parser.parse_args()

    weatherman = WeatherMan()

    try:
        if weather_args.highest_lowest_temp:
            date = parser.parse(weather_args.highest_lowest_temp[0])
            weatherman.display_highest_lowest_temperature(weather_args.highest_lowest_temp[1], date.year)
        if weather_args.average:
            date = parser.parse(weather_args.average[0])
            weatherman.display_mean_temp_humidity(weather_args.average[1], date.year, date.month)
        if weather_args.bar_chart:
            date = parser.parse(weather_args.bar_chart[0])
            weatherman.display_two_bar_charts(weather_args.bar_chart[1], date.year, date.month)
            weatherman.display_one_bar_charts(weather_args.bar_chart[1], date.year, date.month)
    except ValueError:
        print('Please enter correct date.')


if __name__ == "__main__":
    main()
