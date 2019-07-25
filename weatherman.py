import csv
import sys
import glob
import operator
from datetime import datetime
import argparse

from colorama import init
from colorama import Fore, Style

from filereader import read_file


class WeatherMan:
    def __init__(self, path):
        self.__path = path+'//'

    def year_files(self, year):  # fettching year files
        year_files = []
        directory_files = glob.glob(
            '{}Murree_weather_{}*'.format(self.__path, year))
        for file in directory_files:
            if str(year) in file:
                year_files.append(file)
        return year_files

    def highest_record_in_a_year(self, year):
        max_temperatures = []
        low_temperatures = []
        weather_data_dates = []
        max_humidities = []

        year_files = self.year_files(year)  # given year files
        if len(year_files) == 0:
            print('No Data Found For This Year')
            return
        for file in year_files:  # looping over list of files
            # tuple of list returned
            weather_data = read_file(file)
            max_temperatures += weather_data[0]
            low_temperatures += weather_data[1]
            max_humidities += weather_data[2]
            weather_data_dates += weather_data[4]

        # calculating maximum,minimum and max humidity
        max_temperature = max(max_temperatures)
        low_temperature = min(low_temperatures)
        max_humid = max(max_humidities)

        # prinitng values to console
        print('Highest: {}C on {}'.format(
            str(max_temperature),
            self.get_weather_data_date(
                weather_data_dates,
                max_temperatures,
                max_temperature
            )))
        print('Lowest: {}C on {}'.format(
            str(low_temperature),
            self.get_weather_data_date(
                weather_data_dates,
                low_temperatures,
                low_temperature
            )))
        print('Humid: {}% on {}'.format(
            str(max_humid),
            self.get_weather_data_date(
                weather_data_dates,
                max_humidities,
                max_humid
            )))

    # getting date for a given data and then formating that date to words
    def get_weather_data_date(self, date_list, data_list, data):
        data_date = date_list[data_list.index(data)]
        return datetime.strptime(data_date, '%Y-%m-%d').strftime('%B %d')

    def average_record_in_a_month(self, weather_date):
        date_object = datetime.strptime(weather_date, '%Y/%m')
        month = date_object.strftime('%b')
        year = date_object.strftime('%Y')
        highest_temp_average = 0
        lowest_temp_average = 0
        average_humidity = 0
        highest_temp_count = 0
        lowest_temp_count = 0
        humidity_count = 0
        max_temperatures = []
        low_temperatures = []
        average_humidities = []
        weather_data_dates = []

        file_path = '{}Murree_weather_{}_{}.txt'.format(
            self.__path, year, month)
        weather_data = read_file(file_path)
        max_temperatures += weather_data[0]
        low_temperatures += weather_data[1]
        average_humidities += weather_data[3]
        weather_data_dates += weather_data[4]

        for i in range(len(weather_data_dates)):
                # checkin if the filed is empty and then adding it to the
                # averages for later use
            if max_temperatures[i]:
                highest_temp_average += int(max_temperatures[i])
                highest_temp_count += 1
            if low_temperatures[i]:
                lowest_temp_average += int(low_temperatures[i])
                lowest_temp_count += 1
            if average_humidities[i]:
                average_humidity += int(average_humidities[i])
                humidity_count += 1

        # calculating average
        highest_temp_average = highest_temp_average // highest_temp_count
        lowest_temp_average = lowest_temp_average // lowest_temp_count
        average_humidity = average_humidity // humidity_count
        print('Highest Average: {}C'.format(str(highest_temp_average)))
        print('Lowest Average: {}C'.format(str(lowest_temp_average)))
        print('Average Humidity: {}%'.format(str(average_humidity)))

    def highest_lowest_temprature_of_a_day_two_horisontal_bar_charts(
            self, weather_date):
        date_object = datetime.strptime(weather_date, '%Y/%m')
        # printing date in words
        print(date_object.strftime('%B %Y'))
        month = date_object.strftime('%b')
        year = date_object.strftime('%Y')

        max_temperatures = []
        low_temperatures = []

        file_path = '{}Murree_weather_{}_{}.txt'.format(
            self.__path, year, month)
        weather_data = read_file(file_path)
        max_temperatures += weather_data[0]
        low_temperatures += weather_data[1]
        weather_date = 1
        for i in range(len(max_temperatures)):
                # checkin if the filed is empty and then adding it to the
            if max_temperatures[i]:
                print(weather_date, end=' ')
                print(Fore.RED + '+' * int(max_temperatures[i]), end='')
                print(Fore.WHITE+str(' {}C'.format(max_temperatures[i])))
                print(weather_date, end=' ')
                print(Fore.BLUE + '+' * int(low_temperatures[i]), end='')
                print(Fore.WHITE+str(' {}C'.format(low_temperatures[i])))
                weather_date += 1

    def highest_lowest_temprature_of_a_day_one_horsontal_bar_chart(
            self, weather_date
    ):
        date_object = datetime.strptime(weather_date, '%Y/%m')
        # printing date in words
        print(date_object.strftime('%B %Y'))
        month = date_object.strftime('%b')
        year = date_object.strftime('%Y')

        max_temperatures = []
        low_temperatures = []

        file_path = '{}Murree_weather_{}_{}.txt'.format(
            self.__path, year, month)
        weather_data = read_file(file_path)
        max_temperatures += weather_data[0]
        low_temperatures += weather_data[1]
        weather_date = 1
        for i in range(len(max_temperatures)):
                # checkin if the filed is empty and then adding it to the
            if max_temperatures[i]:
                print(weather_date, end=' ')
                print(Fore.BLUE + '+' * int(low_temperatures[i]), end='')
                print(Fore.RED + '+' * int(max_temperatures[i]), end=' ')
                print(
                    Fore.WHITE+str(' {}C - {}C'.format(
                        low_temperatures[i], max_temperatures[i]
                    )))
                weather_date += 1


def main():

    parser = argparse.ArgumentParser(description='Year for ')
    parser.add_argument('files_path', type=str,
                        help='Path to weather files')
    parser.add_argument(
        '-e', type=int, help='Highest Record of the year  Expected  \
        Value Format: 2014')
    parser.add_argument(
        '-a', type=str, help='Average Highest, Lowest Temp, Humidity  \
        Expected Value Format: 2014/2')
    parser.add_argument(
        '-c', type=str, help='Two horisontal bar charts for Temperature  \
            Expected Value Format: 2014/2')
    parser.add_argument(
        '-d', type=str, help='One horisontal bar charts for Temperature  \
            Expected Value Format: 2014/2')
    args = parser.parse_args()

    path = args.files_path
    weather_man = WeatherMan(path)

    if args.e:
        weather_man.highest_record_in_a_year(args.e)
    if args.a:
        weather_man.average_record_in_a_month(args.a)
    if args.c:
        weather_man.\
            highest_lowest_temprature_of_a_day_two_horisontal_bar_charts(
                args.c)
    if args.d:
        weather_man.highest_lowest_temprature_of_a_day_one_horsontal_bar_chart(
            args.d)


main()
