"""
Weatherman Module for displaying weather data.

This module has the main method for project
weatherman to run console commands and print
the appropriate result.
"""
import re
import glob
import argparse
from datetime import datetime
from file_reader import FileReader
from utils import Utils
from weather_data import WeatherData


BLUE = "\033[34m"
RED = "\033[31m"
WHITE = "\033[37m"


class WeatherMan:
    """
    WeatherMan Class.

    This class has all the required
    methods to display the correct information.
    """

    def __init__(self, file_path):
        """
        Iniatilising attributes required.

        This function takes file path as
        an input.
        """
        self.__path = file_path + '//'

    @staticmethod
    def check_file_info(file_info):
        """
        File year and month check.

        This method returns True if the
        file year and month input is in
        the correct format.
        """
        expression = re.compile(r'^[1-2][0-9]{3}/((0)?[1-9]|1[0-2])$')
        if expression.search(str(file_info)):
            return
        print('File year and month format not correct. Example: 2014/2')
        exit()

    @staticmethod
    def check_year_info(year):
        """
        File Year check.

        This method returns True if
        the file year is in the
        correct format.
        """
        expression = re.compile(r'^[1-2][0-9]{3}$')
        if expression.search(str(year)):
            return True
        return False

    def year_files(self, year):
        """
        List of files to display data from.

        This method returns the path of
        all files that are to be opened
        inside a list.
        """
        year_files = []
        directory_files = glob.glob('{}Murree_weather_{}*'.format(self.__path, year))
        for file in directory_files:
            if str(year) in file:
                year_files.append(file)
        return year_files

    @staticmethod
    def graph_print(multiplication_range):
        """
        Graph generator.

        This method returns the graph for
        maximum and minumum temperatures.
        """
        return "+" * int(multiplication_range)

    @staticmethod
    def check_data(data):
        """Check if data is empty return error."""
        if data == "File not found Error.":
            print("File not found Error.")
            exit()


    def year_temperature_print(self, year):
        """
        File year input command.

        This method runs when the "-e" command
        is run which displays highest, lowest
        temperatures and highest humidity for all
        months in that year.
        """
        data = []
        year_files = self.year_files(year)

        read = FileReader(year_files)
        data = read.read_file()
        WeatherMan.check_data(data)

        max_temp_value = Utils.get_max_temperature(data.highest_temp)
        min_temp_value = Utils.get_min_temperature(data.min_temp)
        max_humid_value = Utils.get_max_humidity(data.max_humidity)

        print('Highest: {}C on {}'.format(
            str(max_temp_value),
            WeatherData.format_date(
                data.date[data.highest_temp.index(max_temp_value)])))
        print('Lowest: {}C on {}'.format(
            str(min_temp_value),
            WeatherData.format_date(
                data.date[data.min_temp.index(min_temp_value)])))
        print('Humid: {}% on {}'.format(
            str(max_humid_value),
            WeatherData.format_date(
                data.date[data.max_humidity.index(max_humid_value)])))

    def year_month_average_temperature_print(self, file_info):
        """File year/month input command.

        This method runs when the "-a" command
        is run which displays highest, lowest
        average temperatures and average humidity for
        that specific year and month.
        """
        data = []
        file_info = datetime.strptime(file_info, '%Y/%m')
        month = file_info.strftime('%b')
        year = file_info.strftime('%Y')
        file = '{}Murree_weather_{}_{}.txt'.format(self.__path, year, month)
        read = FileReader([file])
        data = read.read_file()
        WeatherMan.check_data(data)
        print(
            "Highest Average: %sC" % Utils.get_average(data.highest_temp))
        print("Lowest Average: %sC" % Utils.get_average(data.min_temp))
        print("Average Humidity: {}%".format(Utils.get_average(data.max_humidity)))

    def horizontal_graph_print(self, file_info):
        """File year/month input command.

        This method runs when the "-c" command
        is run which displays highest, lowest
        temperature graphs for all days
        of that year and month.
        """
        data = []
        date = datetime.strptime(file_info, '%Y/%m')
        print(date.strftime('%B %Y'))
        month = date.strftime('%b')
        year = date.strftime('%Y')
        file = '{}Murree_weather_{}_{}.txt'.format(self.__path, year, month)
        read = FileReader([file])
        data = read.read_file()
        WeatherMan.check_data(data)

        for day in range(len(data.date)):
            date = data.date[day]
            date = date.split('-')[2]
            if len(date) == 1:
                date = "0%s" % date
            min_temp_graph = ""
            max_temp_graph = ""
            min_display = ""
            max_display = ""
            min_temp_graph = self.graph_print(data.min_temp[day])
            max_temp_graph = self.graph_print(data.highest_temp[day])
            if len(str(data.min_temp[day])) == 1:
                min_display = "0%s" % data.min_temp[day]
            elif str(data.min_temp[day]).find("-") == 0:
                min_display = str(data.min_temp[day]).replace("-", "")
                min_display = "-0%s" % min_display
            if len(str(data.highest_temp[day])) == 1:
                max_display = "0%s" % data.highest_temp[day]
            else:
                max_display = "%s" % data.highest_temp[day]
            if file_info.split("/")[1][0] == "0":
                print("%s %s%s%s%sC" % (str(day), RED, max_temp_graph, WHITE, max_display))
                print("%s %s%s%s%sC" % (str(day), BLUE, min_temp_graph, WHITE, min_display))
            else:
                print("%s %s%s%s%s%s%sC-%sC" % (str(day), BLUE, min_temp_graph, RED,
                                                max_temp_graph, WHITE, min_display,
                                                max_display))

def main():
    """
    To run commands for weatherman class.

    This method takes in input commands from
    console and calls the appropriate method
    accordingly.
    """
    parser = argparse.ArgumentParser(description='Year for ')
    parser.add_argument('files_path', type=str,
                        help='File path')
    parser.add_argument(
        '-e', type=int, help='format is  for example = 2014')
    parser.add_argument(
        '-a', type=str, help='format is for example = 2014/02')
    parser.add_argument(
        '-c', type=str, help='format is for example = 2014/02 or 2014/2')
    argument = parser.parse_args()

    path = argument.files_path
    weather_man = WeatherMan(path)

    if argument.e:
        if weather_man.check_year_info(argument.e):
            weather_man.year_temperature_print(argument.e)
        else:
            print('Year format is not correct.')
    if argument.a:
        weather_man.check_file_info(argument.a)
        weather_man.year_month_average_temperature_print(argument.a)
    if argument.c:
        weather_man.check_file_info(argument.c)
        weather_man.horizontal_graph_print(argument.c)


if __name__ == "__main__":
    main()
