import argparse
import calendar
import csv
import re
from dateutil import parser
from os import listdir
from termcolor import colored


class WeatherMan:
    def __init__(self):
        self.months = calendar.month_name

        self.pkt = 'PKT'
        self.max_temperature_c = 'Max TemperatureC'
        self.min_temperature_c = 'Min TemperatureC'
        self.max_humidity = 'Max Humidity'
        self.mean_humidity = 'Mean Humidity'

        self.red_color = 'red'
        self.blue_color = 'blue'

        self.data_fields = ['PKT', 'Max TemperatureC', 'Mean TemperatureC', 'Min TemperatureC', 'Dew PointC',
                            'MeanDew PointC', 'Min DewpointC', 'Max Humidity', 'Mean Humidity', 'Min Humidity',
                            'Max Sea Level PressurehPa', 'Mean Sea Level PressurehPa', 'Min Sea Level PressurehPa',
                            'Max VisibilityKm', 'Mean VisibilityKm', 'Min VisibilitykM', 'Max Wind SpeedKm/h',
                            'Mean Wind SpeedKm/h', 'Max Gust SpeedKm/h', 'PrecipitationCm', 'CloudCover',
                            'Events', 'WindDirDegrees'
                            ]

    # Function for converting string to Integer if string is empty then return 0
    @staticmethod
    def convert_string_to_int(text):
        text = text.strip()
        return int(text) if text else 0

    def read_single_file(self, file_path):
        with open(file_path) as csvFile:
            dict_reader = csv.DictReader(csvFile, self.data_fields)  # Read File as List of Dictionaries
            next(dict_reader)  # Skip Header
            file_details = list(dict_reader)
            file_details.pop()  # Skip Footer
            return file_details

    def find_and_read_file(self, year, month, path):
        month = self.months[month]
        files = []
        # Find all files that matches the given pattern
        for f in listdir(path):
            if re.match(r'(?=.*{year})(?=.*{month}).*\.txt$'.format(year=year,
                                                                    month=month[:3]), f):
                files.append(f)

        file_detail = []

        # Read all files that matches the above pattern
        for temp in range(len(files)):
            file_name = path + files.pop()
            file_detail.extend(self.read_single_file(file_name))

        return file_detail

    # Method to Display highest temperature and day, lowest temperature and day, most humid day and humidity.
    def highest_lowest_humid(self, year, path):
        highest_temperature = 0
        highest_temperature_day_month = 0
        highest_temperature_day = 0
        lowest_temperature = 100
        lowest_temperature_day_month = 0
        lowest_temperature_day = 0
        most_humidity = 0
        most_humid_day_month = 0
        most_humid_day = 0

        # Find all files that matches the given pattern
        files = [f for f in listdir(path) if re.match(r'(?=.*{year}).*\.txt$'.format(year=year), f)]

        for temp in range(len(files)):
            file_name = path + files.pop()
            file_detail = self.read_single_file(file_name)

            for single_day in file_detail:
                pkt = parser.parse(single_day[self.pkt])
                tmp_highest_temperature = WeatherMan.convert_string_to_int(single_day[self.max_temperature_c])
                tmp_lowest_temperature = WeatherMan.convert_string_to_int(single_day[self.min_temperature_c])
                tmp_most_humidity = WeatherMan.convert_string_to_int(single_day[self.max_humidity])

                # Finding Highest Max Temperature
                if tmp_highest_temperature > highest_temperature:
                    highest_temperature = tmp_highest_temperature
                    highest_temperature_day_month = pkt.month
                    highest_temperature_day = pkt.day

                # Finding Lowest Min Temperature
                if tmp_lowest_temperature < lowest_temperature:
                    lowest_temperature = tmp_lowest_temperature
                    lowest_temperature_day_month = pkt.month
                    lowest_temperature_day = pkt.day

                # Finding Highest Max Humidity
                if tmp_most_humidity > most_humidity:
                    most_humidity = tmp_most_humidity
                    most_humid_day_month = pkt.month
                    most_humid_day = pkt.day

        print 'Highest: {temp}C on {month} {day}'.format(temp=highest_temperature,
                                                         month=self.months[highest_temperature_day_month],
                                                         day=highest_temperature_day)
        print 'Lowest: {temp}C on {month} {day}'.format(temp=lowest_temperature,
                                                        month=self.months[lowest_temperature_day_month],
                                                        day=lowest_temperature_day)
        print "Humid: {humidity}% on {month} {day}".format(humidity=most_humidity,
                                                           month=self.months[most_humid_day_month],
                                                           day=most_humid_day)

    # Method to display the average highest temperature, average lowest temperature, average humidity.
    def average_highest_lowest_humid(self, year, month, path):
        file_detail = self.find_and_read_file(year, month, path)

        # Finding Sum of all Max Temperature for finding average
        sum_max_temperature_c = sum(WeatherMan.convert_string_to_int
                                    (single_day[self.max_temperature_c]) for single_day in file_detail)

        # Finding Sum of all min Temperature for finding average
        sum_min_temperature_c = sum(WeatherMan.convert_string_to_int
                                    (single_day[self.min_temperature_c]) for single_day in file_detail)

        # Finding Sum of all mean Humidity for finding average
        sum_mean_humidity = sum(WeatherMan.convert_string_to_int
                                (single_day[self.mean_humidity]) for single_day in file_detail)

        avg_max_temperature_c = sum_max_temperature_c / len(file_detail)
        avg_min_temperature_c = sum_min_temperature_c / len(file_detail)
        avg_mean_humidity = sum_mean_humidity / len(file_detail)

        print 'Highest Average: {avg_max_temperature_c}C'.format(avg_max_temperature_c=avg_max_temperature_c)
        print 'Lowest Average: {avg_min_temperature_c}C'.format(avg_min_temperature_c=avg_min_temperature_c)
        print 'Average Humidity: {avg_mean_humidity}%'.format(avg_mean_humidity=avg_mean_humidity)

    @staticmethod
    def colored_print(temperature, color):
        bar_graph = ""
        for index in range(int(temperature)):
            bar_graph += colored('+', color)
        return bar_graph

    @staticmethod
    def display_bar_graph(current_day, temperature, color):
        bar_graph = ""
        bar_graph += str(current_day) + " "
        bar_graph += WeatherMan.colored_print(temperature, color)
        bar_graph += " " + str(temperature) + "C"
        print bar_graph

    def display_double_graph_per_day(self, current_day, highest_temperature, lowest_temperature):
        WeatherMan.display_bar_graph(current_day, highest_temperature, self.red_color)
        WeatherMan.display_bar_graph(current_day, lowest_temperature, self.blue_color)

    def display_single_graph_per_day(self, current_day, highest_temperature, lowest_temperature):
        bar_graph = ""
        bar_graph += str(current_day) + " "
        bar_graph += WeatherMan.colored_print(lowest_temperature, self.blue_color)
        bar_graph += WeatherMan.colored_print(highest_temperature, self.red_color)
        bar_graph += " " + str(lowest_temperature) + "C - " + str(highest_temperature) + "C"
        print bar_graph

    # Method to draw horizontal bar chart on the console for the highest and lowest temperature on each day
    def display_bar_graph_by_month(self, year, month, path, is_bonus_task):

        file_detail = self.find_and_read_file(year, month, path)

        for single_day in file_detail:
            current_date = parser.parse(single_day[self.pkt])
            highest_temperature = WeatherMan.convert_string_to_int(single_day[self.max_temperature_c])
            lowest_temperature = WeatherMan.convert_string_to_int(single_day[self.min_temperature_c])
            if is_bonus_task:
                self.display_single_graph_per_day(current_date.day, highest_temperature, lowest_temperature)
            else:
                self.display_double_graph_per_day(current_date.day, highest_temperature, lowest_temperature)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-e', nargs=2, dest='highest_lowest_humid')
    arg_parser.add_argument('-a', nargs=2, dest='avg_highest_lowest_temp_humidity')
    arg_parser.add_argument('-c', nargs=2, dest='separate_bar_chart')
    arg_parser.add_argument('-b', nargs=2, dest='joint_bar_chart')
    args = arg_parser.parse_args()

    weatherman = WeatherMan()

    try:
        if args.highest_lowest_humid:
            path = args.highest_lowest_humid.pop()
            date = parser.parse(args.highest_lowest_humid.pop())
            weatherman.highest_lowest_humid(date.year, path)

        elif args.avg_highest_lowest_temp_humidity:
            path = args.avg_highest_lowest_temp_humidity.pop()
            date = parser.parse(args.avg_highest_lowest_temp_humidity.pop())
            weatherman.average_highest_lowest_humid(date.year, date.month, path)

        elif args.separate_bar_chart:
            path = args.separate_bar_chart.pop()
            date = parser.parse(args.separate_bar_chart.pop())
            weatherman.display_bar_graph_by_month(date.year, date.month, path, False)

        elif args.joint_bar_chart:
            path = args.joint_bar_chart.pop()
            date = parser.parse(args.joint_bar_chart.pop())
            weatherman.display_bar_graph_by_month(date.year, date.month, path, True)

    except OSError:
        print("Given arguments are not correct.")


if __name__ == "__main__":
    main()
