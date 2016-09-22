import argparse
import csv
import datetime
import os
import calendar
import matplotlib.pyplot as plt
import numpy
import collections
import operator

WeatherData = collections.namedtuple('WeatherData',
                                     'date min_temp max_temp max_humidity min_humidity \
                                             min_avg_temp max_avg_temp max_avg_humidity ')


class CursorColors:
    BLUE = '\033[94m'
    RED = '\033[91m'
    WHITE = '\033[0m'


class WeatherDataReader(object):
    """ This weather_data_parser class reads a file, and stores the results """

    def __init__(self, report_date, weather_data_dir):
        """ Class constructor that takes file path as an argument """
        self.file_read_list = []
        self.report_date = report_date
        self.weather_data_dir = weather_data_dir

    @staticmethod
    def __to_int(string):
        if string:
            return int(string)

    @staticmethod
    def is_date_valid(date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    @property
    def __update_file_read_list(self):
        """ Returns the list of all files which need to be read """
        date_components = self.report_date.split('/')

        file_name_prefix = 'lahore_weather_' + date_components[0]
        self.file_read_list = []
        month_no_list = [int(date_components[1])] if len(date_components) > 1 else [month_no for month_no in
                                                                                    range(1, 13)]
        for month_no in month_no_list:
            file_name = os.path.join(self.weather_data_dir,
                                     file_name_prefix + '_' + calendar.month_abbr[month_no] + '.txt')
            self.file_read_list.append(file_name)

    @property
    def read_weather_data_file(self):
        """ Reads the file row by row and records mean min/max Temperatures and humidity """
        self.__update_file_read_list
        weather_data = []

        for file_path in self.file_read_list:
            with open(file_path) as csvfile:
                next(csvfile)
                reader = csv.DictReader(csvfile)
                monthly_weather_data = []
                date_key = 'PKT' if 'PKT' in reader.fieldnames else 'PKST'

                for row in reader:
                    date_string = row[date_key]

                    if not self.is_date_valid(date_string):
                        continue

                    weather_data_obj = WeatherData(date=date_string,
                                                   min_temp=self.__to_int(row['Min TemperatureC']),
                                                   max_temp=self.__to_int(row['Max TemperatureC']),
                                                   max_humidity=self.__to_int(row['Max Humidity']),
                                                   min_humidity=self.__to_int(row[' Min Humidity']),
                                                   min_avg_temp=self.__to_int(row['Mean TemperatureC']),
                                                   max_avg_temp=self.__to_int(row['Mean TemperatureC']),
                                                   max_avg_humidity=self.__to_int(row[' Mean Humidity'])
                                                   )
                    monthly_weather_data.append(weather_data_obj)
                weather_data = weather_data + monthly_weather_data
        return weather_data


class Charts:
    @staticmethod
    def print_bar_chart_cmd(report_date, data_directory):
        """ For a given month draws two horizontal bar charts on the console for the highest and
            lowest temperature on each day. Highest in red and lowest in blue """
        weather_data_list = WeatherReports.get_chart_data(report_date, data_directory)
        for weather_data in weather_data_list:
            if not weather_data.max_temp:
                weather_data.max_temp = 0
            if not weather_data.min_temp:
                weather_data.min_temp = 0
            day = weather_data.date.split('-')[2]
            print(day, CursorColors.RED + '+' * weather_data.max_temp, weather_data.max_temp, CursorColors.WHITE)
            print(day, CursorColors.BLUE + '+' * weather_data.min_temp, weather_data.min_temp, CursorColors.WHITE)

    @staticmethod
    def print_monthly_stackchart(report_date, data_directory):
        """ For a given month draw one horizontal bar chart on the console for the highest and
            lowest temperature on each day. Highest in red and lowest in blue. """
        weather_data_list = WeatherReports.get_chart_data(report_date, data_directory)

        for weather_data in weather_data_list:
            if not weather_data.max_temp:
                weather_data.max_temp = 0
            if not weather_data.min_temp:
                weather_data.min_temp = 0
            print(weather_data.date.split('-')[2], CursorColors.RED + '+' * weather_data.max_temp,
                  CursorColors.BLUE + '+' * weather_data.min_temp,
                  CursorColors.WHITE, weather_data.max_temp, '-', weather_data.min_temp)

    @staticmethod
    def print_bar_chart_gui(report_date, data_directory):
        """ Stores the bar chart for min and max temperatures of each day in a PDF file """
        max_temperatures, min_temperatures, days = WeatherReports.get_gui_stack_chart(report_date, data_directory)
        total_days = len(days)
        index = numpy.arange(total_days)  # the x locations for the groups
        width = 0.5  # the width of the bars
        figure, graph_axis = plt.subplots()
        max_temperature_rect = graph_axis.bar(index, max_temperatures, width, color='r')
        min_temperature_rect = graph_axis.bar(index + width, min_temperatures, width, color='b')

        # add some text for labels, title and axes ticks
        graph_axis.set_ylabel('Temperature (C)')
        graph_axis.set_title('Min/Max temperatures')
        graph_axis.set_xticks(index + width)
        graph_axis.set_xticklabels(days)
        graph_axis.legend((max_temperature_rect[0], min_temperature_rect[0]), ('Max', 'Min'))

        plt.savefig("Graph.pdf")


class WeatherReports:
    @staticmethod
    def get_extremum(weather_data, attribute, extremum_function=max):
        return extremum_function([data for data in weather_data if getattr(data, attribute)],
                              key=operator.attrgetter(attribute))

    @staticmethod
    def get_chart_data(report_date, data_directory):
        weather_data_reader = WeatherDataReader(report_date, data_directory)
        return weather_data_reader.read_weather_data_file

    @staticmethod
    def get_gui_stack_chart(report_date, data_directory):
        weather_data_list = WeatherReports.get_chart_data(report_date, data_directory)
        max_temperatures = [k.max_temp if k.max_temp else 0 for k in weather_data_list]
        min_temperatures = [k.min_temp if k.min_temp else 0 for k in weather_data_list]
        days = [k.date.split('-')[2] for k in weather_data_list]

        return max_temperatures, min_temperatures, days

    @staticmethod
    def get_monthly_averages(report_date, data_directory):
        weather_data_reader = WeatherDataReader(report_date, data_directory)
        monthly_data = weather_data_reader.read_weather_data_file

        max_avg = WeatherReports.get_extremum(monthly_data, 'max_avg_temp', extremum_function=max)
        least_avg = WeatherReports.get_extremum(monthly_data, 'min_avg_temp', extremum_function=min)
        max_humidity = WeatherReports.get_extremum(monthly_data, 'max_avg_humidity', extremum_function=max)
        return max_avg, least_avg, max_humidity

    @staticmethod
    def get_annual_extrema(report_date, data_directory):
        weather_data_reader = WeatherDataReader(report_date, data_directory)
        weather_data = weather_data_reader.read_weather_data_file
        max_temp = WeatherReports.get_extremum(weather_data, 'max_temp', extremum_function=max)
        min_temp = WeatherReports.get_extremum(weather_data, 'min_temp', extremum_function=min)
        max_humidity = WeatherReports.get_extremum(weather_data, 'max_humidity', extremum_function=max)
        min_humidity = WeatherReports.get_extremum(weather_data, 'min_humidity', extremum_function=min)

        return max_temp, min_temp, max_humidity, min_humidity


class ReportPrinter:
    @staticmethod
    def print_monthly_averages(report_date, data_directory):
        """ Prints the mean min/max temperatures and humidity """
        max_avg, least_avg, max_humidity = WeatherReports.get_monthly_averages(report_date, data_directory)
        print("Highest Average Temperature:", max_avg.max_avg_temp, "C")
        print("Lowest Average Temperature:", least_avg.min_avg_temp, "C")
        print("Highest Average Humidity:", max_humidity.max_avg_humidity, "%")

    @staticmethod
    def print_annual_extrema(report_date, data_directory):
        """For a given year display the highest temperature and day, lowest temperature and
            day, most humid day and humidity."""
        max_temp, min_temp, max_humidity, min_humidity = WeatherReports.get_annual_extrema(report_date, data_directory)

        print('Highest Temperature: ', max_temp.max_temp, 'C on ' + max_temp.date.replace('-', '/'))
        print('Lowest Temperature: ', min_temp.min_temp, 'C on ' + min_temp.date.replace('-', '/'))
        print('Most Humid: ', max_humidity.max_humidity, '% on ' + max_humidity.date.replace('-', '/'))
        print('Least Humid: ', min_humidity.min_humidity, '% on ' + min_humidity.date.replace('-', '/'))


def main():
    """ Main Function """
    # Read Command Line arguments and proceed if the arguments are valid.
    parser = argparse.ArgumentParser(description='A utility for processing weather data of Lahore.')
    parser.add_argument('-e',
                        help='Sets the year for the annual report')
    parser.add_argument('-a',
                        help="Sets the month for average highest temperature, average " +
                             "lowest temperature, average humidity.")
    parser.add_argument('-c',
                        help="Sets the month for bar charts for daily highest and lowest temperatures")
    parser.add_argument('-s',
                        help="Sets the month for stack chart for daily highest and lowest temperatures")
    parser.add_argument('-b',
                        help="Sets the month for graphical bar chart for daily highest and lowest temperatures")
    parser.add_argument('data_dir', action="store",
                        help='Path of directory containing weather data files')

    args = parser.parse_args()
    data_folder_path = args.data_dir

    if not os.path.isdir(data_folder_path):
        exit('Specified directory does not exist')
    if args.e:
        ReportPrinter.print_annual_extrema(args.e, data_folder_path)
    if args.a:
        ReportPrinter.print_monthly_averages(args.a, data_folder_path)
    if args.c:
        Charts.print_bar_chart_cmd(args.c, data_folder_path)
    if args.s:
        Charts.print_monthly_stackchart(args.s, data_folder_path)
    if args.b:
        Charts.print_bar_chart_gui(args.b, data_folder_path)


if __name__ == "__main__":
    main()
