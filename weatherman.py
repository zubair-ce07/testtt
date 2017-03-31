import argparse
import calendar
from dateutil import parser
from termcolor import colored
import csv
import re
import os


class WeatherParser:

    @staticmethod
    def read_weather_files(file_path, year, month=None):
        weather_readings = []
        weather_fields = ['PKT', 'Max TemperatureC', 'Min TemperatureC', 'Max Humidity', 'Mean TemperatureC',
                          'Mean Humidity']
        if month:
            filename_pattern = '(?=.*{year})(?=.*{month}).*\.txt$'.format(year=year, month=month[:3])
        else:
            filename_pattern = '(?=.*{year}).*\.txt$'.format(year=year)

        for filename in os.listdir(file_path):
            if re.search(filename_pattern, filename, flags=re.IGNORECASE):
                with open('{path}/{filename}'.format(filename=filename, path=file_path)) as csvFile:
                    weather_records_reader = csv.DictReader(csvFile, fieldnames=weather_fields)
                    next(weather_records_reader)  # Skip header because first line in every file is empty
                    weather_readings.extend(list(weather_records_reader))

        return weather_readings

    def get_weather_readings(self, file_path, year, month=None):
        weather_readings = self.read_weather_files(file_path, year, month)

        if not weather_readings:
            print('No relevant weather data found.')

        return weather_readings


class WeatherCalculator:

    def __init__(self):
        self.date = 'PKT'
        self.maximum_temperature = 'Max TemperatureC'
        self.minimum_temperature = 'Min TemperatureC'
        self.maximum_humidity = 'Max Humidity'
        self.mean_temperature = 'Mean TemperatureC'
        self.mean_humidity = 'Mean Humidity'

    @staticmethod
    def filter_empty_weather_readings(weather_readings, weather_field):
        return (weather_reading for weather_reading in weather_readings if weather_reading[weather_field])

    def get_highest_temperature(self, weather_readings):
        cleaned_weather_readings = self.filter_empty_weather_readings(weather_readings, self.maximum_temperature)
        highest_temperature_reading = max(cleaned_weather_readings,
                                          key=lambda weather_reading: int(weather_reading[self.maximum_temperature]))

        highest_temperature = highest_temperature_reading[self.maximum_temperature]
        date = highest_temperature_reading[self.date]

        return date, highest_temperature

    def get_lowest_temperature(self, weather_readings):
        cleaned_weather_readings = self.filter_empty_weather_readings(weather_readings, self.minimum_temperature)
        lowest_temperature_reading = min(cleaned_weather_readings,
                                         key=lambda weather_reading: int(weather_reading[self.minimum_temperature]))

        lowest_temperature = lowest_temperature_reading[self.minimum_temperature]
        date = lowest_temperature_reading[self.date]

        return date, lowest_temperature

    def get_highest_humidity(self, weather_readings):
        cleaned_weather_readings = self.filter_empty_weather_readings(weather_readings, self.maximum_humidity)
        highest_humidity_reading = max(cleaned_weather_readings,
                                       key=lambda weather_reading: int(weather_reading[self.maximum_humidity]))

        highest_humidity = highest_humidity_reading[self.maximum_humidity]
        date = highest_humidity_reading[self.date]

        return date, highest_humidity

    def get_highest_mean_temperature(self, weather_readings):
        cleaned_weather_readings = self.filter_empty_weather_readings(weather_readings, self.mean_temperature)
        highest_mean_temperature_reading = max(cleaned_weather_readings,
                                               key=lambda weather_reading: int(weather_reading[self.mean_temperature]))
        return highest_mean_temperature_reading[self.mean_temperature]

    def get_lowest_mean_temperature(self, weather_readings):
        cleaned_weather_readings = self.filter_empty_weather_readings(weather_readings, self.mean_temperature)
        lowest_mean_temperature_reading = min(cleaned_weather_readings,
                                              key=lambda weather_reading: int(weather_reading[self.mean_temperature]))
        return lowest_mean_temperature_reading[self.mean_temperature]

    def get_highest_mean_humidity(self, weather_readings):
        cleaned_weather_readings = self.filter_empty_weather_readings(weather_readings, self.mean_humidity)
        highest_mean_humidity_reading = max(cleaned_weather_readings,
                                            key=lambda weather_reading: int(weather_reading[self.mean_humidity]))
        return highest_mean_humidity_reading[self.mean_humidity]

    def get_minimum_maximum_temperature_by_day(self, weather_readings):
        for weather_reading in weather_readings:
            yield weather_reading[self.date], weather_reading[self.minimum_temperature], \
                  weather_reading[self.maximum_temperature]


class WeatherReports:

    @staticmethod
    def display_highest_temperature(weather_readings):
        weather_calculator = WeatherCalculator()
        date, highest_temperature = weather_calculator.get_highest_temperature(weather_readings)
        if date and highest_temperature:
            parsed_date = parser.parse(date)
            print('Highest Temperature: {temp}C on {month} {day}'.format(
                temp=highest_temperature,
                month=calendar.month_name[parsed_date.month],
                day=parsed_date.day))

    @staticmethod
    def display_lowest_temperature(weather_readings):
        weather_calculator = WeatherCalculator()
        date, lowest_temperature = weather_calculator.get_lowest_temperature(weather_readings)
        if date and lowest_temperature:
            parsed_date = parser.parse(date)
            print('Lowest Temperature: {temp}C on {month} {day}'.format(
                temp=lowest_temperature,
                month=calendar.month_name[parsed_date.month],
                day=parsed_date.day))

    @staticmethod
    def display_highest_humidity(weather_readings):
        weather_calculator = WeatherCalculator()
        date, highest_humidity = weather_calculator.get_highest_humidity(weather_readings)
        if date and highest_humidity:
            parsed_date = parser.parse(date)
            print('Highest Humidity: {humidity}% on {month} {day}'.format(
                humidity=highest_humidity,
                month=calendar.month_name[parsed_date.month],
                day=parsed_date.day))

    def display_temperature_humidity(self, file_path, year):
        if not all([file_path or year]):
            print('Please pass correct arguments.')
            return

        weather_parser = WeatherParser()
        weather_readings = weather_parser.get_weather_readings(file_path, year)

        self.display_highest_temperature(weather_readings)
        self.display_lowest_temperature(weather_readings)
        self.display_highest_humidity(weather_readings)

    @staticmethod
    def display_highest_mean_temperature(weather_readings):
        weather_calculator = WeatherCalculator()
        highest_mean_temperature = weather_calculator.get_highest_mean_temperature(weather_readings)
        print('Highest Average Temperature: {highest_mean_temp}C'.format(
            highest_mean_temp=highest_mean_temperature))

    @staticmethod
    def display_lowest_mean_temperature(weather_readings):
        weather_calculator = WeatherCalculator()
        lowest_mean_temperature = weather_calculator.get_lowest_mean_temperature(weather_readings)
        print('Lowest Average Temperature: {lowest_mean_temp}C'.format(
            lowest_mean_temp=lowest_mean_temperature))

    @staticmethod
    def display_highest_mean_humidity(weather_readings):
        weather_calculator = WeatherCalculator()
        highest_mean_humidity = weather_calculator.get_highest_mean_humidity(weather_readings)
        print('Highest Average Humidity: {highest_mean_humid}%'.format(
            highest_mean_humid=highest_mean_humidity))

    def display_mean_temperature_humidity(self, file_path, year, month):
        if not all([file_path or year or month]):
            print('Please pass correct arguments.')
            return

        weather_parser = WeatherParser()
        weather_readings = weather_parser.get_weather_readings(file_path, year, calendar.month_name[month])

        self.display_highest_mean_temperature(weather_readings)
        self.display_lowest_mean_temperature(weather_readings)
        self.display_highest_mean_humidity(weather_readings)

    def print_two_bar_charts_record(self, day, temp, symbol, color):
        print('{day} '.format(day=day), end='')
        self.print_colored(temp, symbol, color)
        print(' {temperature}C'.format(temperature=temp))

    @staticmethod
    def print_colored(count, symbol, color):
        for index in range(int(count)):
            print(colored(symbol, color), end='')

    def display_bar_charts(self, file_path, year, month):
        if not all([file_path or year or month]):
            print('Please pass correct arguments.')
            return

        weather_parser = WeatherParser()
        weather_readings = weather_parser.get_weather_readings(file_path, year, calendar.month_name[month])

        print('{month} {year}'.format(month=calendar.month_name[month], year=year))
        self.display_two_bar_charts(weather_readings)

        print('{month} {year}'.format(month=calendar.month_name[month], year=year))
        self.display_one_bar_charts(weather_readings)

    def display_two_bar_charts(self, weather_readings):
        weather_calculator = WeatherCalculator()
        minimum_maximum_temperature_by_day = weather_calculator.get_minimum_maximum_temperature_by_day(weather_readings)
        for date, minimum_temperature, maximum_temperature in minimum_maximum_temperature_by_day:
            try:
                day = parser.parse(date).day
            except ValueError:
                continue

            if maximum_temperature:
                self.print_two_bar_charts_record(day, maximum_temperature, '+', 'red')

            if minimum_temperature:
                self.print_two_bar_charts_record(day, minimum_temperature, '+', 'blue')

    def display_one_bar_charts(self, weather_readings):
        weather_calculator = WeatherCalculator()
        temperature_by_day = weather_calculator.get_minimum_maximum_temperature_by_day(weather_readings)

        for date, minimum_temperature, maximum_temperature in temperature_by_day:
            try:
                day = parser.parse(date).day
            except ValueError:
                continue

            print('{day} '.format(day=day), end='')

            if minimum_temperature:
                self.print_colored(minimum_temperature, '+', 'blue')

            if maximum_temperature:
                self.print_colored(maximum_temperature, '+', 'red')

            print(' {lowest_temp}C-{highest_temp}C'.format(
                lowest_temp=minimum_temperature, highest_temp=maximum_temperature))


def main():
    weather_arg_parser = argparse.ArgumentParser()
    weather_arg_parser.add_argument('-e', nargs=2, dest='highest_lowest_temp')
    weather_arg_parser.add_argument('-a', nargs=2, dest='average')
    weather_arg_parser.add_argument('-c', nargs=2, dest='bar_chart')
    weather_args = weather_arg_parser.parse_args()

    weather_reports = WeatherReports()

    try:
        if weather_args.highest_lowest_temp:
            date = parser.parse(weather_args.highest_lowest_temp[0])
            weather_reports.display_temperature_humidity(weather_args.highest_lowest_temp[1], date.year)
        if weather_args.average:
            date = parser.parse(weather_args.average[0])
            weather_reports.display_mean_temperature_humidity(weather_args.average[1], date.year, date.month)
        if weather_args.bar_chart:
            date = parser.parse(weather_args.bar_chart[0])
            weather_reports.display_bar_charts(weather_args.bar_chart[1], date.year, date.month)
    except ValueError:
        print('Please enter correct date.')


if __name__ == "__main__":
    main()
