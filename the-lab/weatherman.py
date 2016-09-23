import argparse
import csv
import datetime
import os
import calendar
import matplotlib.pyplot as plt
import numpy
import collections
import operator
from enum import Enum

WeatherData = collections.namedtuple("WeatherData",
                                     'date min_temp max_temp max_humidity '
                                     'min_humidity min_avg_temp '
                                     'max_avg_temp max_avg_humidty')


class CursorColors(Enum):
    BLUE = '\033[94m'
    RED = '\033[91m'
    WHITE = '\033[0m'


class WeatherDataReader(object):
    """ This weather_data_parser class reads a file,
        and stores the results """
    def __init__(self, report_date, weather_data_dir):
        """ Class constructor that takes file path as an argument """
        self.report_date = report_date
        self.weather_data_dir = weather_data_dir

    def __to_int(self, string):
        if string:
            return int(string)

    def is_date_valid(self, date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def __get_weather_files(self):
        """ Returns the list of all files which need to be read """
        date_components = self.report_date.split('/')

        file_name_prefix = 'lahore_weather_' + date_components[0]
        month_nos = [int(date_components[1])] if len(date_components) > 1 \
            else list(range(1, 13))
        for month_no in month_nos:
            file_name = os.path.join(self.weather_data_dir,
                                     file_name_prefix + '_' +
                                     calendar.month_abbr[month_no] + '.txt')
            yield file_name

    def get_weather_data(self):
        """ Reads the file row by row and records mean min/max
        Temperatures and humidity """
        weather_files = self.__get_weather_files()
        weather_data = []

        for file_path in weather_files:
            with open(file_path) as csvfile:
                # Skipping the first blank line of the file
                next(csvfile)
                csv_reader = csv.DictReader(csvfile)
                monthly_weather_data = []
                date_key = 'PKT' if 'PKT' in csv_reader.fieldnames else 'PKST'

                for row in csv_reader:
                    date_string = row[date_key]
                    if not self.is_date_valid(date_string):
                        continue
                    weather_params = WeatherData(date=date_string,
                                                 min_temp=self.__to_int(
                                                     row['Min TemperatureC']),
                                                 max_temp=self.__to_int(
                                                     row['Max TemperatureC']),
                                                 max_humidity=self.__to_int(
                                                     row['Max Humidity']),
                                                 min_humidity=self.__to_int(
                                                     row[' Min Humidity']),
                                                 min_avg_temp=self.__to_int(
                                                     row['Mean TemperatureC']),
                                                 max_avg_temp=self.__to_int(
                                                     row['Mean TemperatureC']),
                                                 max_avg_humidty=self.__to_int(
                                                     row[' Mean Humidity'])
                                                 )
                    monthly_weather_data.append(weather_params)
                weather_data.extend(monthly_weather_data)
        return weather_data


class Chart:
    default_color_array = [CursorColors.RED, CursorColors.BLUE]

    @staticmethod
    def show_barchart(chart_bars, indices, color_array=[]):
        chart = ""
        color_array = Chart.default_color_array if len(color_array) == 0 \
            else color_array

        for y_axis in range(len(indices)):
            for index, stack in enumerate(chart_bars):
                chart += str(indices[y_axis]) + " " + color_array[index].value
                chart += '+' * stack[int(y_axis) - 1]
                chart += ' '+ str(stack[int(y_axis) - 1])
                chart += CursorColors.WHITE.value
                chart += "\n"

        print(chart)

    @staticmethod
    def show_stackchart(chart_bars, indices, color_array=[]):
        chart = ""
        color_array = Chart.default_color_array if len(color_array) == 0 \
            else color_array

        for y_axis in range(len(indices)):
            chart += indices[y_axis] + " "
            for index, stack in enumerate(chart_bars):
                chart += color_array[index].value + '+' * stack[int(y_axis)
                                                                - 1] + \
                         CursorColors.WHITE.value
            chart += " "
            for index, stack in enumerate(chart_bars):
                chart += str(stack[int(y_axis) - 1])
                chart += "-" if index != len(chart_bars) - 1 else ""
            chart += "\n"
        print(chart)

    @staticmethod
    def show_gui_barchart(max_temperatures, min_temperatures, days):
        total_days = len(days)

        indices = numpy.array(list(range(total_days)), numpy.int32)
        width = 0.5  # the width of the bars
        figure, graph_axis = plt.subplots()
        max_temperature_rect = graph_axis.bar(indices, max_temperatures, width,
                                              color='r')
        min_temperature_rect = graph_axis.bar(indices + width,
                                              min_temperatures,
                                              width, color='b')
        # add some text for labels, title and axes ticks
        graph_axis.set_ylabel('Temperature (C)')
        graph_axis.set_title('Min/Max temperatures')
        graph_axis.set_xticks(indices + width)
        graph_axis.set_xticklabels(days)
        graph_axis.legend((max_temperature_rect[0], min_temperature_rect[0]),
                          ('Max', 'Min'))
        plt.savefig("Graph.pdf")


class ReportPrinter:
    @staticmethod
    def averages(max_avg, least_avg, max_humidity):
        """ Prints the mean min/max temperatures and humidity """
        print("Highest Average Temperature:", max_avg.max_avg_temp, "C")
        print("Lowest Average Temperature:", least_avg.min_avg_temp, "C")
        print("Highest Average Humidity:", max_humidity.max_avg_humidty, "%")

    @staticmethod
    def extrema(max_temp, min_temp, max_humidity, min_humidity):
        """For a given year display the highest temperature and day, lowest
        temperature and day, most humid day and humidity."""
        print('Highest Temperature: ', max_temp.max_temp,
              'C on ' + max_temp.date.replace('-', '/'))
        print('Lowest Temperature: ', min_temp.min_temp,
              'C on ' + min_temp.date.replace('-', '/'))
        print('Most Humid: ', max_humidity.max_humidity,
              '% on ' + max_humidity.date.replace('-', '/'))
        print('Least Humid: ', min_humidity.min_humidity,
              '% on ' + min_humidity.date.replace('-', '/'))


class WeatherReports:
    @staticmethod
    def __get_extremum(weather_data, attribute, extremum_function=max):
        return extremum_function(
            [data for data in weather_data if getattr(data, attribute)],
            key=operator.attrgetter(attribute))

    @staticmethod
    def __parse_to_chart_data(report_date, data_directory):
        weather_data_reader = WeatherDataReader(report_date, data_directory)
        weather_data = weather_data_reader.get_weather_data()
        for weather_params in weather_data:
            if not weather_params.max_temp:
                weather_params.max_temp = 0
            if not weather_params.min_temp:
                weather_params.min_temp = 0

        max_temp_bar = [weather_param.max_temp for weather_param in
                        weather_data]
        min_temp_bar = [weather_param.min_temp for weather_param in
                        weather_data]
        indices = [k.date.split('-')[2] for k in weather_data]

        return [max_temp_bar, min_temp_bar], indices

    @staticmethod
    def monthly_bar_chart_cmd(report_date, data_directory):
        chart_bars, indices = WeatherReports.__parse_to_chart_data(
            report_date, data_directory)
        Chart.show_barchart(chart_bars, indices)

    @staticmethod
    def monthly_stack_chart(report_date, data_directory):
        chart_bars, indices = WeatherReports.__parse_to_chart_data(
            report_date, data_directory)
        Chart.show_stackchart(chart_bars, indices)

    @staticmethod
    def monthly_bar_chart_gui(report_date, data_directory):
        chart_bars, indices = WeatherReports.__parse_to_chart_data(
            report_date, data_directory)
        Chart.show_gui_barchart(chart_bars[0], chart_bars [1], indices)

    @staticmethod
    def monthly_averages(report_date, data_directory):
        weather_data_reader = WeatherDataReader(report_date, data_directory)
        weather_data = weather_data_reader.get_weather_data()

        max_avg = WeatherReports.__get_extremum(weather_data, 'max_avg_temp',
                                                extremum_function=max)
        least_avg = WeatherReports.__get_extremum(weather_data, 'min_avg_temp',
                                                  extremum_function=min)
        max_humidity = WeatherReports.__get_extremum(weather_data,
                                                     'max_avg_humidty',
                                                     extremum_function=max)
        ReportPrinter.averages(max_avg, least_avg, max_humidity)

    @staticmethod
    def annual_extrema(report_date, data_directory):
        weather_data_reader = WeatherDataReader(report_date, data_directory)
        weather_data = weather_data_reader.get_weather_data()
        max_temp = WeatherReports.__get_extremum(weather_data, 'max_temp',
                                                 extremum_function=max)
        min_temp = WeatherReports.__get_extremum(weather_data, 'min_temp',
                                                 extremum_function=min)
        max_humidity = WeatherReports.__get_extremum(weather_data,
                                                     'max_humidity',
                                                     extremum_function=max)
        min_humidity = WeatherReports.__get_extremum(weather_data,
                                                     'min_humidity',
                                                     extremum_function=min)

        ReportPrinter.extrema(max_temp, min_temp, max_humidity, min_humidity)


def main():
    """ Main Function """
    # Read Command Line arguments and proceed if the arguments are valid.
    parser = argparse.ArgumentParser(
        description='A utility for processing weather data of Lahore.')
    parser.add_argument('-e',
                        help='Sets the year for the annual report')
    parser.add_argument('-a',
                        help="Sets the month for average highest "
                             "temperature,\ average lowest temperature,"
                             "average humidity.")
    parser.add_argument('-c',
                        help="Sets the month for bar charts for daily "
                             "highest and lowest temperatures")
    parser.add_argument('-s',
                        help="Sets the month for stack chart for daily "
                             "highest and lowest temperatures")
    parser.add_argument('-b',
                        help="Sets the month for graphical bar chart for "
                             "daily highest and lowest temperatures")
    parser.add_argument('data_dir', action="store",
                        help='Path of directory containing weather data files')

    args = parser.parse_args()
    data_directory_path = args.data_dir

    if not os.path.isdir(data_directory_path):
        exit('Specified directory does not exist')
    if args.e:
        WeatherReports.annual_extrema(args.e, data_directory_path)
    if args.a:
        WeatherReports.monthly_averages(args.a, data_directory_path)
    if args.c:
        WeatherReports.monthly_bar_chart_cmd(args.c, data_directory_path)
    if args.s:
        WeatherReports.monthly_stack_chart(args.s, data_directory_path)
    if args.b:
        WeatherReports.monthly_bar_chart_gui(args.b, data_directory_path)


if __name__ == "__main__":
    main()
