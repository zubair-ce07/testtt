"""This is module is about weather data, it reads weather data and report max
    temp,min temp,max humidity of an year,average max temp,min temp and
    humidity of a month, it also plot bar charts for of everyday for max
    and min temperature."""
import glob
from datetime import datetime
import argparse

from colorama import Fore

from file_reader import read_file
import utils


class WeatherMan:
    """This class has 4 emthod that prints differnet report and
    it store path of the files from where the data is fetched"""

    def __init__(self, path):
        self.__path = path+'//'

    def year_files(self, year):  # fettching year files
        """This method fecth files for given year"""
        year_files = []
        directory_files = glob.glob(
            '{}Murree_weather_{}*'.format(self.__path, year))
        for file in directory_files:
            if str(year) in file:
                year_files.append(file)
        return year_files

    def highest_record_in_a_year(self, year):
        """This method prints highest,lowest tempreture,most humidity of the
        year with month and day"""
        max_temperatures = []
        low_temperatures = []
        weather_data_dates = []
        max_humidities = []

        year_files = self.year_files(year)  # given year files
        if not year_files:
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
            utils.get_weather_data_date(
                weather_data_dates,
                max_temperatures,
                max_temperature
            )))
        print('Lowest: {}C on {}'.format(
            str(low_temperature),
            utils.get_weather_data_date(
                weather_data_dates,
                low_temperatures,
                low_temperature
            )))
        print('Humid: {}% on {}'.format(
            str(max_humid),
            utils.get_weather_data_date(
                weather_data_dates,
                max_humidities,
                max_humid
            )))

    def average_record_in_a_month(self, weather_date):
        """This method prints average max,min temperature and
         humidity of a month"""
        weather_date = datetime.strptime(weather_date, '%Y/%m')
        month = weather_date.strftime('%b')
        year = weather_date.strftime('%Y')
        highest_temp_average = 0
        lowest_temp_average = 0
        average_humidity = 0
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
            if len(max_temperatures) > i:
                highest_temp_average += int(max_temperatures[i])
            if len(low_temperatures) > i:
                lowest_temp_average += int(low_temperatures[i])
            if len(average_humidities) > i:
                average_humidity += int(average_humidities[i])

        # calculating average
        highest_temp_average = highest_temp_average // len(max_temperatures)
        lowest_temp_average = lowest_temp_average // len(low_temperatures)
        average_humidity = average_humidity // len(average_humidities)
        print('Highest Average: {}C'.format(str(highest_temp_average)))
        print('Lowest Average: {}C'.format(str(lowest_temp_average)))
        print('Average Humidity: {}%'.format(str(average_humidity)))

    def highest_lowest_temprature_of_a_day_two_horizontal_bar_charts(
            self, weather_date):
        """This method prints max and min temperature seprately
        of each day of a month in horizontal bar chart"""
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
        for i, max_temp in enumerate(max_temperatures):
            print(weather_date, end=' ')
            print(Fore.RED + '+' * int(max_temp), end='')
            print(Fore.WHITE+str(' {}C'.format(max_temperatures[i])))
            print(weather_date, end=' ')
            print(Fore.BLUE + '+' * int(low_temperatures[i]), end='')
            print(Fore.WHITE+str(' {}C'.format(low_temperatures[i])))
            weather_date += 1

    def highest_lowest_temprature_of_a_day_one_horzontal_bar_chart(
            self, weather_date
    ):
        """This method prints max and min temperature
        of each day of a month in one horizontal bar chart"""
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
        for i, max_temp in enumerate(max_temperatures):
            # checkin if the filed is empty and then adding it to the
            if max_temperatures[i]:
                print(weather_date, end=' ')
                print(Fore.BLUE + '+' * int(low_temperatures[i]), end='')
                print(Fore.RED + '+' * int(max_temp), end=' ')
                print(
                    Fore.WHITE+str(' {}C - {}C'.format(
                        low_temperatures[i], max_temperatures[i]
                    )))
                weather_date += 1


def main():
    """main method of the program where arguments are
    evaluated and respective report is generated"""

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
        '-c', type=str, help='Two horizontal bar charts for Temperature  \
            Expected Value Format: 2014/2')
    parser.add_argument(
        '-d', type=str, help='One horizontal bar charts for Temperature  \
            Expected Value Format: 2014/2')
    args = parser.parse_args()

    path = args.files_path
    weather_man = WeatherMan(path)

    if args.e:
        if utils.year_validation(args.e):
            weather_man.highest_record_in_a_year(args.e)
        else:
            print('Enter a valid year')
    if args.a:
        utils.date_validation(args.a)
        weather_man.average_record_in_a_month(args.a)
    if args.c:
        utils.date_validation(args.c)
        weather_man. \
            highest_lowest_temprature_of_a_day_two_horizontal_bar_charts(
                args.c)
    if args.d:
        utils.date_validation(args.d)
        weather_man.highest_lowest_temprature_of_a_day_one_horzontal_bar_chart(
            args.d)


if __name__ == "__main__":
    main()
