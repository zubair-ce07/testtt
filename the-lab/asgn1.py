from os import listdir
from os.path import isfile, join
import argparse
import csv

"""	This weather_data_parser class reads a file, and stores the results """


class weather_data_parser(object):
    """ Class constructor that takes file path as an argument """

    def __init__(self, file_path):
        self.file_path = file_path

    @staticmethod
    def __extract_year(str):
        return str.split('-')[0]

    @staticmethod
    def __to_int(string):
        if string:
            return int(string)

    """ Reads the file row by row and records min/max Temperatures, HUmidities and hottest days """

    def parse_file(self):
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

                    if 'PKT' in row.keys():

                        date_key = 'PKT'
                    else:

                        date_key = 'PKST'

                    hottest_day = row[date_key]
                    year = self.__extract_year(row[date_key])

                    min_humidity = self.__to_int(row[' Min Humidity'])
                    max_humidity = self.__to_int(row['Max Humidity'])

                val = self.__to_int(row['Max TemperatureC'])
                if val is not None and (max_temp is None or val > max_temp):
                    max_temp = val
                    hottest_day = row[date_key]
                    year = self.__extract_year(row[date_key])

                val = self.__to_int(row['Max Humidity'])
                if val is not None and (max_humidity is None or val > max_temp):
                    max_humidity = val

                val = self.__to_int(row[' Min Humidity'])
                if val is not None and (min_humidity is None or val < min_humidity):
                    min_humidity = val

                val = self.__to_int(row['Min TemperatureC'])
                if val is not None and (min_temp is None or val < min_temp):
                    min_temp = val

            self.min_temp = min_temp
            self.max_temp = max_temp
            self.min_humidity = min_humidity
            self.max_humidity = max_humidity
            self.hottest_day = hottest_day
            self.year = year


# <------------- END OF CLASS ---------------->


""" Returns 1 if the input is a valid integer and returns 0 otherwise"""


def isValidInt(value):
    if value is not None:

        return 1
    else:

        return 0


""" Finds annual min/max Temperatures, min/max Humidities and hottest days """


def generate_annual_report(parsed_data_list):
    annual_dictionary = {}

    for parsedData in parsed_data_list:

        if not parsedData.year in annual_dictionary.keys():
            # Set starting values for min/max Temperatures and min/max Humidity
            annual_dictionary[parsedData.year] = {}
            annual_dictionary[parsedData.year]['min_temp'] = parsedData.min_temp
            annual_dictionary[parsedData.year]['max_temp'] = parsedData.max_temp
            annual_dictionary[parsedData.year]['min_humidity'] = parsedData.min_humidity
            annual_dictionary[parsedData.year]['max_humidity'] = parsedData.max_humidity
            annual_dictionary[parsedData.year]['hottest_day'] = parsedData.hottest_day
            annual_dictionary[parsedData.year]['year'] = parsedData.year
        else:
            # Update the min/max temperatures and Humidities if required

            val = parsedData.max_temp
            if isValidInt(val) and (
                            annual_dictionary[parsedData.year]['max_temp'] is None or
                            val > annual_dictionary[parsedData.year]['max_temp']):
                # Update max temperature, hottest day and the current year

                annual_dictionary[parsedData.year]['max_temp'] = val
                annual_dictionary[parsedData.year]['hottest_day'] = parsedData.hottest_day
                annual_dictionary[parsedData.year]['year'] = parsedData.year

            val = parsedData.max_humidity
            if isValidInt(val) and (
                            annual_dictionary[parsedData.year]['max_humidity'] is None or
                            val > annual_dictionary[parsedData.year]['max_humidity']):
                # Update the max Humidity

                annual_dictionary[parsedData.year]['max_humidity'] = val

            val = parsedData.min_temp
            if isValidInt(val) and (
                            annual_dictionary[parsedData.year]['min_temp'] is None or
                            val < annual_dictionary[parsedData.year]['min_temp']):
                # Update the minimum Temperature

                annual_dictionary[parsedData.year]['min_temp'] = val

            val = parsedData.min_humidity
            if isValidInt(val) and (
                            annual_dictionary[parsedData.year]['min_humidity'] is None or
                            val < annual_dictionary[parsedData.year]['min_humidity']):
                # Update min humidity

                annual_dictionary[parsedData.year]['min_humidity'] = val

    return annual_dictionary


""" Prints annual report with Year, MAX Temp, MIN Temp, MAX Humidity and Min Humidity """


def print_annual_weather_report(parsed_data_list):
    print ('Year\t\tMAX Temp\tMIN Temp\tMAX Humidity\t  Min Humidity')
    print ('-----------------------------------------------------------------------------')
    count = 0
    annual_dictionary = generate_annual_report(parsed_data_list)
    for year, yearData in annual_dictionary.items():
        print (
        yearData['year'], '\t\t', yearData['max_temp'], '\t\t', yearData['min_temp'], '\t\t', yearData['max_humidity'],
        '\t\t', yearData['min_humidity'])


""" Prints yearly hottest days and the corresponding maximum temperatures """


def print_hottest_days(parsed_data_list):
    print ('Hottest days of each year')
    print ('Year\tDate\t\tTemp')
    annual_dictionary = generate_annual_report(parsed_data_list)
    for year, yearData in annual_dictionary.items():
        print (yearData['year'], '\t', yearData['hottest_day'].replace('-', '/'), '\t', yearData['max_temp'])


""" Format the path of the file """


def format_file_path(directory_path, file_name):
    formatted_file_path = ''

    if directory_path[len(directory_path) - 1] != '/':

        formatted_file_path = directory_path + '/' + file_name
    else:

        formatted_file_path = directory_path + file_name

    return formatted_file_path


""" Main Function """


def main():
    # Read Command Line arguments and proceed if the arguments are valid. 

    parser = argparse.ArgumentParser(description='Example with non-optional arguments')

    parser.add_argument('reportID', help='Use 1 for Annual Max/Min Temperature and 2 for Hottest day of each year',
                        action="store", type=int)
    parser.add_argument('data_dir', action="store",
                        help='Path of directory containing weather data files')

    args = parser.parse_args()

    data_folder_path = args.data_dir

    try:
        all_file_names = [f for f in listdir(data_folder_path) if isfile(join(data_folder_path, f))]

    except OSError as err:
        all_file_names = []
        print("OS error: {0}".format(err))
        exit()

    parsed_file_data_list = []

    for file_name in all_file_names:
        __weather_data_parser = weather_data_parser(format_file_path(data_folder_path, file_name))
        __weather_data_parser.parse_file()
        parsed_file_data_list.append(__weather_data_parser)

    if args.reportID == 1:

        print_annual_weather_report(parsed_file_data_list)
    else:

        print_hottest_days(parsed_file_data_list)


if __name__ == "__main__":
    main()
