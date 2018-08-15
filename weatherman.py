#!/usr/bin/python3

import os
import sys
import calendar

from parser import WeatherParser
from weather import Weather

CEND = '\33[0m'
CRED = '\33[31m'
CBLUE = '\33[34m'

COMMANDS = ('-e', '-a', '-c')

USAGE = """\
usage: weatherman.py command argument /path/to/weather/data/files

commands:
-e      For a given year display the highest temperature and day,
        lowest temperature and day, most humid day and humidity.
        Example  Usage: weatherman.py -e 2002 /path/to/files
        Example output:
            Highest: 45C on June 23
            Lowest: 01C on December 22
            Humid: 95% on August 14

-a      For a given month display the average highest temperature,
        average lowest temperature, average humidity.
        Example  Usage: weatherman.py -a 2005/6 /path/to/files
        Example output:
            Highest Average: 39C
            Lowest Average: 18C
            Average Humidity: 71%

-c      For a given month draw one horizontal bar chart on the console
        for the highest and lowest temperature on each day. Highest in
        red and lowest in blue.
        Example  Usage: weatherman.py -c 2011/3 /path/to/files
        Example output:
            March 2011
            01 {0}+++++++++++{1}++++++++++++++++++++++++{2} 11C - 25C
            02 {0}++++++++{1}+++++++++++++++++++++{2} 08C - 22C
""".format(CBLUE, CRED, CEND)


class Weatherman:
    def __init__(self, arguments):
        self.arguments = arguments

    def validate_arguments(self):
        if len(self.arguments) != 3:
            self.exit_with_usage()

        self.validate_command()
        self.validate_date()
        self.validate_path()

    def exit_with_usage(self):
        print(USAGE)
        exit()

    def validate_command(self):
        self.command = self.arguments[0]

        if self.command not in COMMANDS:
            print('Invalid command {}'.format(self.arguments[0]))
            self.exit_with_usage()

    def validate_date(self):
        arguments = self.arguments[1].split('/')

        try:
            self.year = int(arguments[0])

            if self.year < 1900 or self.year > 9999:
                raise ValueError('invalid year')
        except ValueError:
            print('Provided year is not valid {}'.format(arguments[0]))
            self.exit_with_usage()

        if self.command != '-e':
            if len(arguments) < 2:
                print('Month not provided in argument {}'.format(sys.argv[2]))
                self.exit_with_usage()

            try:
                self.month = int(arguments[1])

                if self.month < 1 or self.month > 12:
                    raise ValueError('invalid month')
            except ValueError:
                print('Provided month is not valid {}'.format(arguments[1]))
                self.exit_with_usage()

    def validate_path(self):
        self.data_path = self.arguments[2]

        if not os.path.isdir(self.data_path):
            print('Provided directory is not valid {}'.format(self.data_path))
            self.exit_with_usage()

    def show_weather(self):
        self.validate_arguments()

        if self.command == '-e':
            self.show_summary_of_year()
        elif self.command == '-a':
            self.show_average_of_month()
        elif self.command == '-c':
            self.show_weather_of_month()

    def show_summary_of_year(self):
        highest = Weather(None, float('inf'), float('-inf'),
                          None, float('inf'), float('-inf'), None)
        lowest = Weather(None, float('inf'), float('-inf'),
                         None, float('inf'), float('-inf'), None)
        humid = Weather(None, float('inf'), float('-inf'),
                        None, float('inf'), float('-inf'), None)

        for month in range(1, 13):
            try:
                with WeatherParser(self.data_path, self.year, month) as parser:
                    for day, weather in enumerate(parser, start=1):
                        if not weather:
                            continue

                        if weather.max_temperature > highest.max_temperature:
                            highest = weather
                        if weather.min_temperature < lowest.min_temperature:
                            lowest = weather
                        if weather.max_humidity > humid.max_humidity:
                            humid = weather

            except FileNotFoundError:
                pass

        if not highest.mean_humidity:
            print('No record found!')
        else:
            print('Highest: {}C on {}'.format(
                highest.max_temperature, highest.date.strftime('%B %d')))
            print('Lowest: {}C on {}'.format(
                lowest.min_temperature, lowest.date.strftime('%B %d')))
            print('Humid: {}% on {}'.format(
                humid.max_humidity, humid.date.strftime('%B %d')))

    def show_average_of_month(self):
        print('{} {}'.format(calendar.month_name[self.month], self.year))
        count = 0
        highest_average_temperature = 0
        lowest_average_temperature = 0
        average_humidity = 0
        try:
            with WeatherParser(
                    self.data_path, self.year, self.month) as parser:
                for day, weather in enumerate(parser, start=1):
                    if not weather:
                        continue

                    count += 1
                    highest_average_temperature += weather.max_temperature
                    lowest_average_temperature += weather.min_temperature
                    average_humidity += weather.mean_humidity

            if count == 0:
                print('No record found!')
            else:
                print('Highest Average: {}C'.format(
                    int(highest_average_temperature / count)))
                print('Lowest Average: {}C'.format(
                    int(lowest_average_temperature / count)))
                print('Average Humidity: {}%'.format(
                    int(average_humidity / count)))

        except FileNotFoundError:
            print('No record found!')

    def show_weather_of_month(self):
        print('{} {}'.format(calendar.month_name[self.month], self.year))
        try:
            with WeatherParser(
                    self.data_path, self.year, self.month) as parser:
                for day, weather in enumerate(parser, start=1):
                    if not weather:
                        row = 'Record not found!'
                    else:
                        row = '{}{}{}{}{} {}C - {}C'.format(
                            CBLUE, '+' * weather.min_temperature, CRED,
                            '+' * weather.max_temperature, CEND,
                            weather.min_temperature, weather.max_temperature)

                    print('{} {}'.format(str(day).zfill(2), row))
        except FileNotFoundError:
            print('No record found!')


weatherman = Weatherman(sys.argv[1:])
weatherman.show_weather()
