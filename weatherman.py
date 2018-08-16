#!/usr/bin/python3

import os
import sys

from dateutil.parser import parse

import constants
from parser import WeatherParser
from weather import Weather
from weather_representor import WeatherRepresentor


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
        print(constants.USAGE)
        exit()

    def validate_command(self):
        self.command = self.arguments[0]

        if self.command not in constants.COMMANDS:
            print('Invalid command {}'.format(self.arguments[0]))
            self.exit_with_usage()

    def validate_date(self):
        try:
            # When day is not provided it includes current day in date
            self.date = parse(self.arguments[1])
        except ValueError:
            print('Provided date is invalid {}'.format(self.arguments[1]))
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
                with WeatherParser(
                        self.data_path, self.date.year, month) as parser:
                    for weather in parser:
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
            WeatherRepresentor.print_not_fount()
        else:
            WeatherRepresentor.print_summary_of_year(highest, lowest, humid)

    def show_average_of_month(self):
        WeatherRepresentor.print_date(self.date)
        count = 0
        highest_average_temperature = 0
        lowest_average_temperature = 0
        average_humidity = 0
        try:
            with WeatherParser(
                    self.data_path, self.date.year, self.date.month) as parser:
                for weather in parser:
                    if not weather:
                        continue

                    count += 1
                    highest_average_temperature += weather.max_temperature
                    lowest_average_temperature += weather.min_temperature
                    average_humidity += weather.mean_humidity

            if count == 0:
                raise FileNotFoundError

            WeatherRepresentor.print_average_of_month(
                round(highest_average_temperature / count),
                round(lowest_average_temperature / count),
                round(average_humidity / count)
            )

        except FileNotFoundError:
            WeatherRepresentor.print_not_fount()

    def show_weather_of_month(self):
        WeatherRepresentor.print_date(self.date)
        try:
            with WeatherParser(
                    self.data_path, self.date.year, self.date.month) as parser:
                for weather in parser:
                    WeatherRepresentor.print_temprature_graph(weather)
        except FileNotFoundError:
            WeatherRepresentor.print_not_fount()


def main():
    weatherman = Weatherman(sys.argv[1:])
    weatherman.show_weather()


if __name__ == "__main__":
    main()
