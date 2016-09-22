import argparse
import csv
import datetime
import os
import calendar
import matplotlib.pyplot as plt
import numpy
import collections


class CursorColors:
    BLUE = '\033[94m'
    RED = '\033[91m'
    WHITE = '\033[0m'


class WeatherDataParser(object):
    """ This weather_data_parser class reads a file, and stores the results """

    def __init__(self, file_path):
        """ Class constructor that takes file path as an argument """
        self.file_path = file_path

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

    @staticmethod
    def get_file_read_list(date_param):
        """ Returns the list of all files which need to be read """
        date_components = date_param.split('/')

        file_name_prefix = 'lahore_weather_' + date_components[0]
        file_read_list = []
        if len(date_components)>1:
            month_no_list = [int(date_components[1])]
        else:
            month_no_list = [month_no for month_no in range(1, 13)]
        for month_no in month_no_list:
            file_name = file_name_prefix + '_' + calendar.month_abbr[month_no] + '.txt'
            file_read_list.append(file_name)

        return file_read_list

    @property
    def parse_weather_data_file(self):
        """ Reads the file row by row and records mean min/max Temperatures and humidity """
        with open(self.file_path) as csvfile:
            next(csvfile)
            reader = csv.DictReader(csvfile)
            monthly_weather_data = []
            is_reading_first_row = True

            for row in reader:
                if is_reading_first_row:
                    date_key = 'PKT' if 'PKT' in row.keys() else 'PKST'
                    is_reading_first_row = False
                date_string = row[date_key]

                if not self.is_date_valid(date_string):
                    continue
                weather_data_tuple = collections.namedtuple('weather_data_tuple',
                                                            'date min_temp max_temp max_humidity min_humidity \
                                                             min_avg_temp max_avg_temp max_avg_humidity ')

                weather_data = weather_data_tuple(date=date_string,
                                                  min_temp=self.__to_int(row['Min TemperatureC']),
                                                  max_temp=self.__to_int(row['Max TemperatureC']),
                                                  max_humidity=self.__to_int(row['Max Humidity']),
                                                  min_humidity=self.__to_int(row[' Min Humidity']),
                                                  min_avg_temp=self.__to_int(row['Mean TemperatureC']),
                                                  max_avg_temp=self.__to_int(row['Mean TemperatureC']),
                                                  max_avg_humidity=self.__to_int(row[' Mean Humidity'])
                                                  )
                monthly_weather_data.append(weather_data)
            return monthly_weather_data


class WeatherAnalyzer:
    @staticmethod
    def get_monthly_extremum(monthly_weather_data, weather_attribute, extremum_function=max):
        return extremum_function([data for data in monthly_weather_data if getattr(data, weather_attribute)])


class ChartPrinter:
    @staticmethod
    def print_bar_chart_cmd(data_param, data_directory):
        """ For a given month draws two horizontal bar charts on the console for the highest and
            lowest temperature on each day. Highest in red and lowest in blue """
        files_to_read = WeatherDataParser.get_file_read_list(data_param)
        weather_data_parser = WeatherDataParser(os.path.join(data_directory, files_to_read[0]))
        weather_data_list = weather_data_parser.parse_weather_data_file

        for weather_data in weather_data_list:
            if not weather_data.max_temp:
                weather_data.max_temp = 0
            if not weather_data.min_temp:
                weather_data.min_temp = 0
            day = weather_data.date.split('-')[2]
            print(day, CursorColors.RED + '+' * weather_data.max_temp, weather_data.max_temp, CursorColors.WHITE)
            print(day, CursorColors.BLUE + '+' * weather_data.min_temp, weather_data.min_temp, CursorColors.WHITE)

    @staticmethod
    def print_monthly_stackchart(data_param, data_directory):
        """ For a given month draw one horizontal bar chart on the console for the highest and
            lowest temperature on each day. Highest in red and lowest in blue. """
        files_to_read = WeatherDataParser.get_file_read_list(data_param)
        weather_data_parser = WeatherDataParser(os.path.join(data_directory, files_to_read[0]))
        weather_data_list = weather_data_parser.parse_weather_data_file

        for weather_data in weather_data_list:
            if not weather_data.max_temp:
                weather_data.max_temp = 0
            if not weather_data.min_temp:
                weather_data.min_temp = 0
            print(weather_data.date.split('-')[2], CursorColors.RED + '+' * weather_data.max_temp,
                  CursorColors.BLUE + '+' * weather_data.min_temp,
                  CursorColors.WHITE, weather_data.max_temp, '-', weather_data.min_temp)
        ChartPrinter.print_bar_chart_gui(weather_data_list)

    @staticmethod
    def print_bar_chart_gui(weather_data_list):
        """ Stores the bar chart for min and max temperatures of each day in a PDF file """
        total_days = len(weather_data_list)
        max_temperatures = [k.max_temp if k.max_temp else 0 for k in weather_data_list]
        min_temperatures = [k.min_temp if k.min_temp else 0 for k in weather_data_list]
        days = [k.date for k in weather_data_list]
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


class ReportPrinter:
    @staticmethod
    def print_monthly_averages(data_param, data_directory):
        """ Prints the mean min/max temperatures and humidity """
        files_to_read = WeatherDataParser.get_file_read_list(data_param)
        weather_data_parser = WeatherDataParser(os.path.join(data_directory, files_to_read[0]))
        monthly_data = weather_data_parser.parse_weather_data_file

        max_avg = WeatherAnalyzer.get_monthly_extremum(monthly_data, 'max_avg_temp', extremum_function=max)
        least_avg = WeatherAnalyzer.get_monthly_extremum(monthly_data, 'min_avg_temp',
                                                                      extremum_function=min)
        max_humidity = WeatherAnalyzer.get_monthly_extremum(monthly_data, 'max_avg_humidity',
                                                                         extremum_function=max)
        print("Highest Average Temperature:", max_avg.max_avg_temp, "C")
        print("Lowest Average Temperature:", least_avg.min_avg_temp, "C")
        print("Highest Average Humidity:", max_humidity.max_avg_humidity, "%")

    @staticmethod
    def print_monthly_extremums(date_param, data_directory):
        """For a given year display the highest temperature and day, lowest temperature and
            day, most humid day and humidity."""
        files_to_read = WeatherDataParser.get_file_read_list(date_param)
        parsed_file_data_list = []

        for file_name in files_to_read:
            weather_data_parser = WeatherDataParser(os.path.join(data_directory, file_name))
            parsed_monthly_data = weather_data_parser.parse_weather_data_file
            parsed_file_data_list = parsed_file_data_list + parsed_monthly_data

        annual_max_temp = WeatherAnalyzer.get_monthly_extremum(parsed_file_data_list, 'max_temp',
                                                                            extremum_function=max)
        annual_min_temp = WeatherAnalyzer.get_monthly_extremum(parsed_file_data_list, 'min_temp',
                                                                            extremum_function=min)
        annual_max_humidity = WeatherAnalyzer.get_monthly_extremum(parsed_file_data_list, 'max_humidity',
                                                                                extremum_function=max)
        annual_min_humidity = WeatherAnalyzer.get_monthly_extremum(parsed_file_data_list, 'min_humidity',
                                                                                extremum_function=min)

        print('Highest Temperature: ', annual_max_temp.max_temp, 'C on ' + annual_max_temp.date.replace('-', '/'))
        print('Lowest Temperature: ', annual_min_temp.min_temp, 'C on ' + annual_min_temp.date.replace('-', '/'))
        print('Most Humid: ', annual_max_humidity.max_humidity, '% on ' + annual_max_humidity.date.replace('-', '/'))
        print('Least Humid: ', annual_min_humidity.min_humidity, '% on ' + annual_min_humidity.date.replace('-', '/'))


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
    parser.add_argument('-cc',
                        help="Sets the month for combined bar chart for daily highest and lowest temperatures")
    parser.add_argument('data_dir', action="store",
                        help='Path of directory containing weather data files')

    args = parser.parse_args()
    data_folder_path = args.data_dir

    if not os.path.isdir(data_folder_path):
        exit('Specified directory does not exist')
    if args.e:
        ReportPrinter.print_monthly_extremums(args.e, data_folder_path)
    if args.a:
        ReportPrinter.print_monthly_averages(args.a, data_folder_path)
    if args.c:
        ChartPrinter.print_bar_chart_cmd(args.c, data_folder_path)
    if args.cc:
        ChartPrinter.print_monthly_stackchart(args.cc, data_folder_path)

if __name__ == "__main__":
    main()
