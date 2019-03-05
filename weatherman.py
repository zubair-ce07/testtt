#!/usr/bin/python3

import os
from argparse import ArgumentParser

from dateutil.parser import parse

from parser import WeatherParser
from weather import Weather
from weather_representor import WeatherRepresentor


class Weatherman:
    def __init__(self, command, date, file_path):
        self.command = command
        self.validate_date(date)
        self.validate_path(file_path)

    def validate_date(self, date):
        try:
            # When month is not provided it includes current month in date
            self.date = parse(date)
        except ValueError:
            print('Provided date is invalid {}'.format(self.arguments[1]))
            exit()

    def validate_path(self, path):
        self.data_path = path

        if not os.path.isdir(self.data_path):
            print('Provided directory is not valid {}'.format(self.data_path))
            exit()

    def show_weather(self):
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
                for weather in WeatherParser(
                        self.data_path, self.date.year, month):
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
            for weather in WeatherParser(
                    self.data_path, self.date.year, self.date.month):
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
            for weather in WeatherParser(
                    self.data_path, self.date.year, self.date.month):
                WeatherRepresentor.print_temprature_graph(weather)
        except FileNotFoundError:
            WeatherRepresentor.print_not_fount()


def main():
    arg_parser = ArgumentParser(
        description='Represent weather data in different forms.')

    group = arg_parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        '-e',
        action='store_const',
        const='-e',
        dest='command',
        help="""For a given year display the highest temperature and day,
            lowest temperature and day, most humid day and humidity."""
    )
    group.add_argument(
        '-a',
        action='store_const',
        const='-a',
        dest='command',
        help="""For a given month display the average highest temperature,
            average lowest temperature, average humidity."""
    )
    group.add_argument(
        '-c',
        action='store_const',
        const='-c',
        dest='command',
        help="""For a given month draw one horizontal bar chart on the console
            for the highest and lowest temperature on each day. Highest in
            red and lowest in blue."""
    )

    arg_parser.add_argument(
        'date', help='Date for which data will be displayed.')
    arg_parser.add_argument(
        'files_path', help='Path of directory which contains weather files.')

    args = arg_parser.parse_args()

    weatherman = Weatherman(args.command, args.date, args.files_path)
    weatherman.show_weather()


if __name__ == "__main__":
    main()
