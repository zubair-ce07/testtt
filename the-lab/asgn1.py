import argparse
import csv
import datetime
import os

import matplotlib.pyplot as plt
import numpy as np

ALL_MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


class EscapeSequence:
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

    def parse_weather_data_file(self):
        """ Reads the file row by row and records mean min/max Temperatures and humidity """
        with open(self.file_path) as csvfile:
            next(csvfile)
            reader = csv.DictReader(csvfile)

            monthly_weather_data = {}

            for row in reader:
                date = row['PKT' if 'PKT' in row.keys() else 'PKST']

                if not self.is_date_valid(date):
                    continue

                weather_attributes = {
                                  'min_temp': self.__to_int(row['Min TemperatureC']),
                                  'max_temp': self.__to_int(row['Max TemperatureC']),
                                  'max_humidity': self.__to_int(row['Max Humidity']),
                                  'min_humidity': self.__to_int(row[' Min Humidity']),
                                  'min_avg_temp': self.__to_int(row['Mean TemperatureC']),
                                  'max_avg_temp': self.__to_int(row['Mean TemperatureC']),
                                  'max_avg_humidity': self.__to_int(row[' Mean Humidity'])
                }

                monthly_weather_data[date] = weather_attributes

            return monthly_weather_data


class WeatherAnalyzer:
    @staticmethod
    def get_monthly_extremum_by_attribute(monthly_weather_data, weather_attribute, extremum='maximum'):

        reverse_sort_order = True if extremum.lower() == 'maximum' else False

        sorted_by_attribute = sorted(monthly_weather_data,
                                     key=lambda x: monthly_weather_data[x][weather_attribute] or -373,
                                     reverse=reverse_sort_order)
        return sorted_by_attribute[0], monthly_weather_data[sorted_by_attribute[0]][weather_attribute]

    @staticmethod
    def get_yearly_extremum_by_attribute(yearly_weather_data, weather_attribute, extremum='maximum'):

        extremum_value = None
        extremum_attribute_date = None

        extremum_function = max if extremum == 'maximum' else extremum

        for monthly_weather_data in yearly_weather_data:
            monthly_extremum = WeatherAnalyzer.get_monthly_extremum_by_attribute(monthly_weather_data,
                                                                               weather_attribute,
                                                                               extremum=extremum)
            try:
                extremum_value = extremum_function(monthly_extremum[1], extremum_value)
                extremum_attribute_date = monthly_extremum[0] if extremum_function(monthly_extremum[1], extremum_value)\
                                                                 == monthly_extremum[1]\
                                                              else extremum_attribute_date

            except TypeError:
                if monthly_extremum[1] is not None:
                    extremum_value = monthly_extremum[1]
                    extremum_attribute_date = monthly_extremum [0]
                else:
                    extremum_value = None

        return extremum_attribute_date, extremum_value


def is_valid_integer(value):
    """ Returns 1 if the input is a valid integer and returns 0 otherwise"""
    if value is not None:
        return 1
    else:
        return 0


def get_month(month_no):
    """Return the name of the month"""
    return ALL_MONTHS[month_no - 1]


def get_file_names_to_be_read(date_param):
    """ Returns the list of all files which need to be read """
    splited_date = date_param.split('/')
    file_name_prefix = 'lahore_weather_'
    file_read_list = []
    if len(splited_date) > 1:
        file_name = file_name_prefix + splited_date[0] + '_' + get_month(int(splited_date[1])) + '.txt'
        file_read_list.append(file_name)
    else:
        file_name_prefix += splited_date[0]
        for month in ALL_MONTHS:
            file_name = file_name_prefix + '_' + month + '.txt'
            file_read_list.append(file_name)

    return file_read_list


def create_bar_chart(daily_weather_data):
    """ Stores the bar chart for min and max temperatures of each day in a PDF file """
    total_days = len(daily_weather_data)
    max_temperatures = []
    min_temperatures = []
    days = []
    count = 1
    for day, day_weather in daily_weather_data.items():
        if day_weather['max_temp']:
            max_temperatures.append(day_weather['max_temp'])
        else:
            max_temperatures.append(0)

        if day_weather['min_temp']:
            min_temperatures.append(day_weather['min_temp'])
        else:
            min_temperatures.append(0)
        days.append(count)
        count += 1

    ind = np.arange(total_days)  # the x locations for the groups
    width = 0.5  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, max_temperatures, width, color='r')
    rects2 = ax.bar(ind + width, min_temperatures, width, color='b')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Temperature (C)')
    ax.set_title('Min/Max temperatures')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(days)

    ax.legend((rects1[0], rects2[0]), ('Max', 'Min'))

    plt.savefig("Graph.pdf")


def print_average_monthly_weather_values(data_param, data_directory):
    """ Prints the mean min/max temperatures and humidity """
    files_to_read = get_file_names_to_be_read(data_param)
    if len(files_to_read) == 1:
        weather_data_parser = WeatherDataParser(os.path.join(data_directory, files_to_read[0]))
        monthly_data = weather_data_parser.parse_weather_data_file()

        max_avg = WeatherAnalyzer.get_monthly_extremum_by_attribute(monthly_data, 'max_avg_temp', extremum='maximum')
        least_avg = WeatherAnalyzer.get_monthly_extremum_by_attribute(monthly_data, 'min_avg_temp', extremum='minimum')
        max_humidity = WeatherAnalyzer.get_monthly_extremum_by_attribute(monthly_data, 'max_avg_humidity', extremum='minimum')
        print("Highest Average Temperature:", max_avg[1], "C")
        print("Lowest Average Temperature:", least_avg[1], "C")
        print("Highest Average Humidity:", max_humidity[1], "%")


def print_monthly_weather_chart(data_param, data_directory):
    """ For a given month draws two horizontal bar charts on the console for the highest and
        lowest temperature on each day. Highest in red and lowest in blue """
    files_to_read = get_file_names_to_be_read(data_param)
    if len(files_to_read) == 1:
        weather_data_parser = WeatherDataParser(os.path.join(data_directory, files_to_read[0]))
        daily_weather_data = weather_data_parser.parse_weather_data_file()

        red_marker = EscapeSequence.RED + "+" + EscapeSequence.WHITE
        blue_marker = EscapeSequence.BLUE + "+" + EscapeSequence.WHITE

        for date, day_weather in daily_weather_data.items():

            # If the min/max temperatures are None set them to 0
            if not day_weather['max_temp']:
                day_weather['max_temp'] = 0
            if not day_weather['min_temp']:
                day_weather['min_temp'] = 0

            day = date.split('-')[2]
            print(day, red_marker * day_weather['max_temp'], day_weather['max_temp'])
            print(day, blue_marker * day_weather['min_temp'], day_weather['min_temp'])


def print_monthly_weather_combined_chart(data_param, data_directory):
    """ For a given month draw one horizontal bar chart on the console for the highest and
        lowest temperature on each day. Highest in red and lowest in blue. """
    files_to_read = get_file_names_to_be_read(data_param)
    if len(files_to_read) == 1:

        weather_data_parser = WeatherDataParser(os.path.join(data_directory, files_to_read[0]))
        daily_weather_data = weather_data_parser.parse_weather_data_file()

        red_marker = EscapeSequence.RED + "+" + EscapeSequence.WHITE
        blue_marker = EscapeSequence.BLUE + "+" + EscapeSequence.WHITE
        for date, day_weather in daily_weather_data.items():

            # If the min/max temperatures are None set them to 0
            if not day_weather['max_temp']:
                day_weather['max_temp'] = 0
            if not day_weather['min_temp']:
                day_weather['min_temp'] = 0

            print(date.split('-')[2], red_marker * day_weather['max_temp'], blue_marker * day_weather['min_temp'],
                  day_weather['max_temp'], '-', day_weather['min_temp'])

        create_bar_chart(daily_weather_data)


def print_extreme_weather_values(date_param, data_directory):
    """For a given year display the highest temperature and day, lowest temperature and
        day, most humid day and humidity."""
    files_to_read = get_file_names_to_be_read(date_param)
    parsed_file_data_list = []

    for file_name in files_to_read:
        weather_data_parser = WeatherDataParser(os.path.join(data_directory, file_name))
        parsed_monthly_data = weather_data_parser.parse_weather_data_file()
        parsed_file_data_list.append(parsed_monthly_data)

    annual_max_temp = WeatherAnalyzer.get_yearly_extremum_by_attribute(parsed_file_data_list, 'max_temp', extremum='maximum')
    annual_min_temp = WeatherAnalyzer.get_yearly_extremum_by_attribute(parsed_file_data_list, 'min_temp', extremum='minimum')
    annual_max_humidity = WeatherAnalyzer.get_yearly_extremum_by_attribute(parsed_file_data_list, 'max_humidity', extremum='maximum')
    annual_min_humidity = WeatherAnalyzer.get_yearly_extremum_by_attribute(parsed_file_data_list, 'min_humidity', extremum='minimum')

    print('Highest Temperature: ', annual_max_temp[1], 'C on ' + annual_max_temp[0].replace('-', '/'))
    print('Lowest Temperature: ', annual_min_temp[1], 'C on ' + annual_min_temp[0].replace('-', '/'))
    print('Most Humid: ', annual_max_humidity[1], '% on ' + annual_max_humidity[0].replace('-', '/'))
    print('Least Humid: ', annual_min_humidity[1], '% on ' + annual_min_humidity[0].replace('-', '/'))


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
        print('Specified director does not exist')
        print('Exiting')
        exit()

    if args.e:
        print_extreme_weather_values(args.e, data_folder_path)

    if args.a:
        print_average_monthly_weather_values(args.a, data_folder_path)

    if args.c:
        print_monthly_weather_chart(args.c, data_folder_path)

    if args.cc:
        print_monthly_weather_combined_chart(args.cc, data_folder_path)

if __name__ == "__main__":
    main()