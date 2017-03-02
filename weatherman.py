import argparse
import calendar
from dateutil import parser
from termcolor import colored
import csv
import re
import os


class WeatherMan:

    def __init__(self):
        self.field_date = 'PKT'
        self.field_temp_max = 'Max TemperatureC'
        self.field_temp_min = 'Min TemperatureC'
        self.field_humid_max = 'Max Humidity'
        self.field_temp_mean = 'Mean TemperatureC'
        self.field_humid_mean = 'Mean Humidity'

    def read_weather_files(self, file_path, year, month=None):
        weather_records = []
        data_fields = [self.field_date, self.field_temp_max, self.field_temp_min, self.field_humid_max,
                       self.field_temp_mean, self.field_humid_mean]
        if month:
            filename_pattern = '(?=.*{year})(?=.*{month}).*\.txt$'.format(year=year, month=month[:3])
        else:
            filename_pattern = '(?=.*{year}).*\.txt$'.format(year=year)

        for filename in os.listdir(file_path):
            if re.search(filename_pattern, filename, flags=re.IGNORECASE):
                with open('{path}/{filename}'.format(filename=filename, path=file_path)) as csvFile:
                    dict_reader = csv.DictReader(csvFile, fieldnames=data_fields)
                    next(dict_reader)  # Skip header because first row in every file is empty
                    weather_records.extend(list(dict_reader))

        return weather_records

    @staticmethod
    def filter_empty_weather_records(weather_records, field_name):
        return (weather_record for weather_record in weather_records if weather_record[field_name])

    def print_two_bar_charts_record(self, day, temp, symbol, color):
        print('{day} '.format(day=day), end='')
        self.colored_print(temp, symbol, color)
        print(' {temperature}C'.format(temperature=temp))

    @staticmethod
    def colored_print(count, symbol, color):
        for index in range(int(count)):
            print(colored(symbol, color), end='')

    def display_highest_lowest_temperature(self, file_path, year):
        if not file_path or not year:
            print('Please pass correct arguments.')
            return

        weather_records = self.read_weather_files(file_path, year)
        if not weather_records:
            print('No relevant weather data found.')
            return

        filtered_weather_records = self.filter_empty_weather_records(weather_records, self.field_temp_max)
        highest_temp_record = max(filtered_weather_records,
                                  key=lambda weather_record: weather_record[self.field_temp_max])
        if highest_temp_record[self.field_date]:
            date = parser.parse(highest_temp_record[self.field_date])
            print('Highest Temperature: {temp}C on {month} {day}'.format(
                temp=highest_temp_record[self.field_temp_max],
                month=calendar.month_name[date.month],
                day=date.day))

        filtered_weather_records = self.filter_empty_weather_records(weather_records, self.field_temp_min)
        lowest_temp_record = min(filtered_weather_records,
                                 key=lambda weather_record: weather_record[self.field_temp_min])
        if lowest_temp_record[self.field_date]:
            date = parser.parse(lowest_temp_record[self.field_date])
            print('Lowest Temperature: {temp}C on {month} {day}'.format(
                temp=lowest_temp_record[self.field_temp_min],
                month=calendar.month_name[date.month],
                day=date.day))

        filtered_weather_records = self.filter_empty_weather_records(weather_records, self.field_humid_max)
        highest_humid_record = max(filtered_weather_records,
                                   key=lambda weather_record: weather_record[self.field_humid_max])
        if highest_humid_record[self.field_date]:
            date = parser.parse(highest_humid_record[self.field_date])
            print('Highest Humidity: {humidity}% on {month} {day}'.format(
                humidity=highest_humid_record[self.field_humid_max],
                month=calendar.month_name[date.month],
                day=date.day))

    def display_average(self, file_path, year, month):
        if not file_path or not year or not month:
            print('Please pass correct arguments.')
            return

        weather_records = self.read_weather_files(file_path, year, calendar.month_name[month])
        if not weather_records:
            print('No relevant weather data found.')
            return

        filtered_weather_records = self.filter_empty_weather_records(weather_records, self.field_temp_mean)
        highest_temp_record = max(filtered_weather_records,
                                  key=lambda weather_record: int(weather_record[self.field_temp_mean]))
        print('Highest Average Temperature: {highest_mean_temp}C'.format(
            highest_mean_temp=highest_temp_record[self.field_temp_mean]))

        filtered_weather_records = self.filter_empty_weather_records(weather_records, self.field_temp_mean)
        lowest_temp_record = min(filtered_weather_records,
                                 key=lambda weather_record: int(weather_record[self.field_temp_mean]))
        print('Lowest Average Temperature: {lowest_mean_temp}C'.format(
            lowest_mean_temp=lowest_temp_record[self.field_temp_mean]))

        filtered_weather_records = self.filter_empty_weather_records(weather_records, self.field_humid_mean)
        highest_humid_record = max(filtered_weather_records,
                                   key=lambda weather_record: int(weather_record[self.field_humid_mean]))
        print('Highest Average Humidity: {highest_mean_humid}%'.format(
            highest_mean_humid=highest_humid_record[self.field_humid_mean]))

    def display_two_bar_charts(self, file_path, year, month):
        if not file_path or not year or not month:
            print('Please pass correct arguments.')
            return

        print('{month} {year}'.format(month=calendar.month_name[month], year=year))

        weather_records = self.read_weather_files(file_path, year, calendar.month_name[month])
        if not weather_records:
            print('No relevant weather data found.')
            return

        for weather_record in weather_records:
            try:
                day = parser.parse(weather_record[self.field_date]).day
            except ValueError:
                continue

            if weather_record[self.field_temp_max]:
                self.print_two_bar_charts_record(day, weather_record[self.field_temp_max], '+', 'red')

            if weather_record[self.field_temp_min]:
                self.print_two_bar_charts_record(day, weather_record[self.field_temp_min], '+', 'blue')

    def display_one_bar_chart(self, file_path, year, month):
        if not file_path or not year or not month:
            print('Please pass correct arguments.')
            return

        print('{month} {year}'.format(month=calendar.month_name[month], year=year))

        weather_records = self.read_weather_files(file_path, year, calendar.month_name[month])
        if not weather_records:
            print('No relevant weather data found.')
            return

        for weather_record in weather_records:
            highest_temp = weather_record[self.field_temp_max]
            lowest_temp = weather_record[self.field_temp_min]

            if lowest_temp or highest_temp:
                print('{day} '.format(day=parser.parse(weather_record[self.field_date]).day), end='')

                if weather_record[self.field_temp_min]:
                    self.colored_print(lowest_temp, '+', 'blue')

                if weather_record[self.field_temp_max]:
                    self.colored_print(highest_temp, '+', 'red')

                print(' {lowest_temp}C-{highest_temp}C'.format(lowest_temp=lowest_temp, highest_temp=highest_temp))


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-e', nargs=2, dest='highest_lowest_temp')
    arg_parser.add_argument('-a', nargs=2, dest='average')
    arg_parser.add_argument('-c', nargs=2, dest='bar_chart')
    args = arg_parser.parse_args()

    weatherman = WeatherMan()

    try:
        if args.highest_lowest_temp:
            date = parser.parse(args.highest_lowest_temp[0])
            weatherman.display_highest_lowest_temperature(args.highest_lowest_temp[1], date.year)
        if args.average:
            date = parser.parse(args.average[0])
            weatherman.display_average(args.average[1], date.year, date.month)
        if args.bar_chart:
            date = parser.parse(args.bar_chart[0])
            weatherman.display_two_bar_charts(args.bar_chart[1], date.year, date.month)
            weatherman.display_one_bar_chart(args.bar_chart[1], date.year, date.month)
    except ValueError:
        print('Please pass date in correct format.')


if __name__ == "__main__":
    main()

