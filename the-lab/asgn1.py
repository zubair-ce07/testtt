from os import listdir
from os.path import isfile, join
import os
import argparse
import csv

ALL_MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


class EscapeSequence:
    BLUE = '\033[94m'
    RED = '\033[91m'
    WHITE = '\033[0m'


class WeatherDataParser(object):
    """	This weather_data_parser class reads a file, and stores the results """

    def __init__(self, file_path):
        """ Class constructor that takes file path as an argument """
        self.file_path = file_path

    @staticmethod
    def __extract_year(str):
        return str.split('-')[0]

    @staticmethod
    def __to_int(string):
        if string:
            return int(string)

    """ Reads the file row by row and records min/max Temperatures, Humidities and hottest days """

    def parse_extreme_weather_data(self):
        with open(self.file_path) as csvfile:
            reading_first_row = 1
            csvfile.seek(0)
            next(csvfile)
            reader = csv.DictReader(csvfile)

            for row in reader:

                if reading_first_row == 1:

                    reading_first_row = 0
                    min_temp = self.__to_int(row['Min TemperatureC'])
                    max_temp = self.__to_int(row['Max TemperatureC'])
                    max_humidity = self.__to_int(row['Max Humidity'])
                    min_humidity = self.__to_int(row[' Min Humidity'])

                    if 'PKT' in row.keys():
                        date_key = 'PKT'
                    else:
                        date_key = 'PKST'

                    most_humid_day = row[date_key]
                    hottest_day = row[date_key]
                    coolest_day = row[date_key]
                    least_humid_day = row[date_key]
                    year = self.__extract_year(row[date_key])

                val = self.__to_int(row['Max TemperatureC'])

                if val is not None and (max_temp is None or val > max_temp):
                    max_temp = val
                    hottest_day = row[date_key]
                    year = self.__extract_year(row[date_key])

                val = self.__to_int(row['Max Humidity'])
                if val is not None and (max_humidity is None or val > max_temp):
                    max_humidity = val
                    most_humid_day = row[date_key]

                val = self.__to_int(row['Min TemperatureC'])
                if val is not None and (min_temp is None or val < min_temp):
                    min_temp = val
                    coolest_day = row[date_key]

                val = self.__to_int(row[' Min Humidity'])
                if val is not None and (min_humidity is None or val < min_humidity):
                    min_humidity = val
                    least_humid_day = row[date_key]

            self.min_temp = min_temp
            self.max_temp = max_temp
            self.max_humidity = max_humidity
            self.min_humidity = min_humidity

            self.hottest_day = hottest_day
            self.most_humid_day = most_humid_day
            self.coolest_day = coolest_day
            self.least_humid_day = least_humid_day

            self.year = year

    def parse_average_weather_data(self):
        with open(self.file_path) as csvfile:
            reading_first_row = 1
            csvfile.seek(0)
            next(csvfile)
            reader = csv.DictReader(csvfile)

            for row in reader:

                if reading_first_row == 1:

                    reading_first_row = 0
                    min_avg_temp = self.__to_int(row['Mean TemperatureC'])
                    max_avg_temp = self.__to_int(row['Mean TemperatureC'])
                    max_avg_humidity = self.__to_int(row[' Mean Humidity'])

                    if 'PKT' in row.keys():
                        date_key = 'PKT'
                    else:
                        date_key = 'PKST'

                    year = self.__extract_year(row[date_key])

                val = self.__to_int(row['Mean TemperatureC'])

                if val is not None and (max_avg_temp is None or val > max_avg_temp):
                    max_avg_temp = val
                    year = self.__extract_year(row[date_key])

                val = self.__to_int(row[' Mean Humidity'])
                if val is not None and (max_avg_humidity is None or val > max_avg_temp):
                    max_avg_humidity = val

                val = self.__to_int(row['Mean TemperatureC'])
                if val is not None and (min_avg_temp is None or val < min_avg_temp):
                    min_avg_temp = val

            self.min_avg_temp = min_avg_temp
            self.max_avg_temp = max_avg_temp
            self.max_avg_humidity = max_avg_humidity

    def parse_daily_weather_data(self):
        __daily_weather_dictionary = []

        with open(self.file_path) as csvfile:
            csvfile.seek(0)
            next(csvfile)
            reader = csv.DictReader(csvfile)
            day = 1
            for row in reader:
                if day < 32:
                    __daily_weather_dictionary.append({'max_temp': self.__to_int(row['Max TemperatureC']),
                                                   'min_temp': self.__to_int(row['Min TemperatureC'])})
                    day += 1

        return __daily_weather_dictionary
# <------------- END OF CLASS ---------------->


def is_valid_point(value):
    """ Returns 1 if the input is a valid integer and returns 0 otherwise"""
    if value is not None:
        return 1
    else:
        return 0


def generate_annual_report(parsed_data_list):
    """ Finds annual min/max Temperatures, min/max Humidities and hottest days """
    annual_dictionary = {}

    for parsedData in parsed_data_list:

        if not parsedData.year in annual_dictionary.keys():
            # Set starting values for min/max Temperatures and min/max Humidity
            annual_dictionary[parsedData.year] = {}
            annual_dictionary[parsedData.year]['min_temp'] = parsedData.min_temp
            annual_dictionary[parsedData.year]['max_temp'] = parsedData.max_temp
            annual_dictionary[parsedData.year]['max_humidity'] = parsedData.max_humidity
            annual_dictionary[parsedData.year]['min_humidity'] = parsedData.min_humidity

            annual_dictionary[parsedData.year]['hottest_day'] = parsedData.hottest_day
            annual_dictionary[parsedData.year]['coolest_day'] = parsedData.coolest_day
            annual_dictionary[parsedData.year]['most_humid_day'] = parsedData.most_humid_day
            annual_dictionary[parsedData.year]['least_humid_day'] = parsedData.least_humid_day

            annual_dictionary[parsedData.year]['year'] = parsedData.year
        else:
            # Update the min/max temperatures and Humidities if required

            val = parsedData.max_temp
            if is_valid_point(val) and (
                            annual_dictionary[parsedData.year]['max_temp'] is None or
                            val > annual_dictionary[parsedData.year]['max_temp']):
                # Update max temperature, hottest day and the current year

                annual_dictionary[parsedData.year]['max_temp'] = val
                annual_dictionary[parsedData.year]['hottest_day'] = parsedData.hottest_day
                annual_dictionary[parsedData.year]['year'] = parsedData.year

            val = parsedData.max_humidity
            if is_valid_point(val) and (
                            annual_dictionary[parsedData.year]['max_humidity'] is None or
                            val > annual_dictionary[parsedData.year]['max_humidity']):
                # Update the max Humidity
                annual_dictionary[parsedData.year]['most_humid_day'] = parsedData.most_humid_day
                annual_dictionary[parsedData.year]['max_humidity'] = val

            val = parsedData.min_temp
            if is_valid_point(val) and (
                            annual_dictionary[parsedData.year]['min_temp'] is None or
                            val < annual_dictionary[parsedData.year]['min_temp']):
                # Update the minimum Temperature
                annual_dictionary[parsedData.year]['coolest_day'] = parsedData.coolest_day
                annual_dictionary[parsedData.year]['min_temp'] = val

            val = parsedData.min_humidity
            if is_valid_point(val) and (
                            annual_dictionary[parsedData.year]['min_humidity'] is None or
                            val < annual_dictionary[parsedData.year]['min_humidity']):
                # Update the minimum Temperature
                annual_dictionary[parsedData.year]['least_humid_day'] = parsedData.least_humid_day
                annual_dictionary[parsedData.year]['min_humidity'] = val

    return annual_dictionary


def get_month(month_no):
    # Return the name of the month
    return ALL_MONTHS[month_no - 1]


def get_file_read_list(date_param):
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


def print_average_monthly_weather_values(data_param, data_directory):
    files_to_read = get_file_read_list(data_param)
    if len(files_to_read) == 1:
        __weather_data_parser = WeatherDataParser(format_file_path(data_directory, files_to_read[0]))
        __weather_data_parser.parse_average_weather_data()
        print("Highest Average: " + str(__weather_data_parser.max_avg_temp) + "C")
        print("Lowest Average: " + str(__weather_data_parser.min_avg_temp) + "C")
        print("Highest Average Humidity: " + str(__weather_data_parser.max_avg_humidity) + "%")


def print_monthly_weather_chart(data_param, data_directory):
    files_to_read = get_file_read_list(data_param)
    if len(files_to_read) == 1:
        __weather_data_parser = WeatherDataParser(format_file_path(data_directory, files_to_read[0]))
        daily_weather_data = __weather_data_parser.parse_daily_weather_data()

        day = 1
        for day_weather in daily_weather_data:
            __red_marker = EscapeSequence.RED + "+" + EscapeSequence.WHITE
            __blue_marker = EscapeSequence.BLUE + "+" + EscapeSequence.WHITE
            print(str(day), __red_marker * day_weather['max_temp'])
            print(str(day), __blue_marker * day_weather['min_temp'], day_weather['min_temp'])
            day += 1


def print_monthly_weather_combined_chart(data_param, data_directory):
    files_to_read = get_file_read_list(data_param)
    if len(files_to_read) == 1:
        __weather_data_parser = WeatherDataParser(format_file_path(data_directory, files_to_read[0]))
        daily_weather_data = __weather_data_parser.parse_daily_weather_data()

        day = 1
        for day_weather in daily_weather_data:
            __red_marker = EscapeSequence.RED + "+" + EscapeSequence.WHITE
            __blue_marker = EscapeSequence.BLUE + "+" + EscapeSequence.WHITE
            print(str(day), __red_marker * day_weather['max_temp'], __blue_marker * day_weather['min_temp'], day_weather['max_temp'], '-', day_weather['min_temp'])
            day += 1


def print_extreme_weather_values(date_param, data_directory):
    files_to_read = get_file_read_list(date_param)
    __parsed_file_data_list = []

    for file_name in files_to_read:
        __weather_data_parser = WeatherDataParser(format_file_path(data_directory, file_name))
        __weather_data_parser.parse_extreme_weather_data()
        __parsed_file_data_list.append(__weather_data_parser)

    annual_report_dict = generate_annual_report(__parsed_file_data_list)

    for year, yearData in annual_report_dict.items():
        print('Highest Temperature: ' + str(yearData['max_temp']) + 'C on ' + yearData['hottest_day'].replace('-', '/'))
        print('Lowest Temperature: ' + str(yearData['min_temp']) + 'C on ' + yearData['coolest_day'].replace('-', '/'))
        print('Most Humid: ' + str(yearData['max_humidity']) + 'C on ' + yearData['most_humid_day'].replace('-', '/'))
        print('Least Humid: ' + str(yearData['min_humidity']) + 'C on ' + yearData['least_humid_day'].replace('-', '/'))


def format_file_path(directory_path, file_name):
    """ Format the path of the file """

    if directory_path[len(directory_path) - 1] != '/':
        formatted_file_path = directory_path + '/' + file_name
    else:
        formatted_file_path = directory_path + file_name

    return formatted_file_path


def main():
    """ Main Function """
    # Read Command Line arguments and proceed if the arguments are valid.

    parser = argparse.ArgumentParser(description='Example with non-optional arguments')

    parser.add_argument('-e',
                        help='Display the highest temperature and day, lowest temperature and day, most humid day.')
    parser.add_argument('-a',
                        help="For a given month display the average highest temperature, average " +
                             "lowest temperature, average humidity.")
    parser.add_argument('-c',
                        help="For a given month draw two horizontal bar charts for the highest and" +
                             "lowest temperature on each day.")
    parser.add_argument('-cc',
                        help="For a given month draw a combined horizontal bar chart for the highest and lowest" +
                             "temperature on each day. Highest in red and lowest in blue.")
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
        print_monthly_weather_combined_chart (args.cc, data_folder_path)

if __name__ == "__main__":
    main()
