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
from weather_data import WeatherData
from file_reader import FileReader



BLUE = "\033[34m"
RED = "\033[31m"
WHITE = "\033[37m"

    #@staticmethod
def validate_date(file_info):
    """
    File year and month check.

    This method returns True if the
    file year and month input is in
    the correct format.
    """
    expression = re.compile(r'^[1-9]\d{3}/((0)?\d|1[0-2])$')
    if expression.search(str(file_info)):
        return file_info
    raise argparse.ArgumentTypeError('File year and month format not correct. Example: 2014/2')
    #exit()

    #@staticmethod
def validate_year(year):
    """
    File Year check.

    This method returns True if
    the file year is in the
    correct format.
    """
    expression = re.compile(r'^[1-9]\d{3}$')
    if expression.search(str(year)):
        return year
    raise argparse.ArgumentTypeError('Year not valid.')
    #return False


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
        self.__path_to_file = '{}//'.format(file_path)


    def year_files(self, year):
        """
        List of files to display data from.

        This method returns the path of
        all files that are to be opened
        inside a list.
        """
        year_files = []
        files = glob.glob('{}Murree_weather_{}*'.format(self.__path_to_file, year))
        year_files = [file for file in files if str(year)]
        return year_files

    @staticmethod
    def graph_print(multiplication_range):
        """
        Graph generator.

        This method returns the graph for
        maximum and minumum temperatures.
        """
        return "+" * int(multiplication_range)



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
        if not year_files:
            print('Data not available.')
            return

        read = FileReader(year_files)
        data = read.read_file()

        weather_date_list = [weather_data.weather_date for weather_data in data]
        max_temp_list = [weather_data.highest_temp for weather_data in data]
        max_temp_value = max(max_temp_list)
        min_temp_list = [weather_data.min_temp for weather_data in data]
        min_temp_value = min(min_temp_list)
        max_humid_list = [weather_data.max_humidity for weather_data in data]
        max_humid_value = max(max_humid_list)

        print('Highest: {}C on {}'.format(
                str(max_temp_value),
                weather_date_list[max_temp_list.index(max_temp_value)].strftime('%B %d')))
        print('Lowest: {}C on {}'.format(
                str(min_temp_value),
                weather_date_list[min_temp_list.index(min_temp_value)].strftime('%B %d')))
        print('Humid: {}% on {}'.format(
                str(max_humid_value),
                weather_date_list[max_humid_list.index(max_humid_value)].strftime('%B %d')))

    def year_month_average_temperature_print(self, file_info):
        """File year/month input command.

        This method runs when the "-a" command
        is run which displays highest, lowest
        average temperatures and average humidity for
        that specific year and month.
        """
        data = []
        weather_reading_date = datetime.strptime(file_info, '%Y/%m')
        month = weather_reading_date.strftime('%b')
        year = weather_reading_date.strftime('%Y')
        file = '{}Murree_weather_{}_{}.txt'.format(self.__path_to_file, year, month)
        read = FileReader([file])
        data = read.read_file()
        highest_temp_sum = 0
        min_temp_sum = 0
        average_humidity_sum = 0
        highest_temp_count = 0
        min_temp_count = 0
        average_humidity_count = 0


        for weather in data:
            if weather.highest_temp:
                highest_temp_sum += weather.highest_temp
                highest_temp_count += 1
            if weather.min_temp:
                min_temp_sum += weather.min_temp
                min_temp_count += 1
            if weather.max_humidity:
                average_humidity_sum += weather.max_humidity
                average_humidity_count += 1


        highest_temp_average = highest_temp_sum // \
            highest_temp_count
        min_temp_average = min_temp_sum// \
            min_temp_count
        average_humidity_average = average_humidity_sum // \
            average_humidity_count

        print("Highest Average: %sC" % highest_temp_average)
        print("Lowest Average: %sC" % min_temp_average)
        print("Average Humidity: {}%".format(average_humidity_average))

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
        file = '{}Murree_weather_{}_{}.txt'.format(self.__path_to_file, year, month)
        read = FileReader([file])
        weather_data = read.read_file()

        for data in weather_data:
            date = data.weather_date
            day = date.strftime('%d')
            if len(day) == 1:
                day = "0%s" % day
            min_temp_graph = ""
            max_temp_graph = ""
            min_display = ""
            max_display = ""
            min_temp_graph = self.graph_print(data.min_temp)
            max_temp_graph = self.graph_print(data.highest_temp)
            if len(str(data.min_temp)) == 1:
                min_display = "0%s" % data.min_temp
            elif str(data.min_temp).find("-") == 0:
                min_display = str(data.min_temp).replace("-", "")
                min_display = "-0%s" % min_display
            if len(str(data.highest_temp)) == 1:
                max_display = "0%s" % data.highest_temp
            else:
                max_display = "%s" % data.highest_temp
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
        '-e', type=validate_year, help='format is  for example = 2014')
    parser.add_argument(
        '-a', type=validate_date, help='format is for example = 2014/02')
    parser.add_argument(
        '-c', type=validate_date, help='format is for example = 2014/02 or 2014/2')
    argument = parser.parse_args()

    path = argument.files_path
    weather_man = WeatherMan(path)

    if argument.e:
        weather_man.year_temperature_print(argument.e)
    if argument.a:
        weather_man.year_month_average_temperature_print(argument.a)
    if argument.c:
        weather_man.horizontal_graph_print(argument.c)


if __name__ == "__main__":
    main()
