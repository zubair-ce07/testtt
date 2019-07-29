"""Weather Data report Module.

it reads weather data and report max
temp,min temp,max humidity of an year,average max temp,min temp and
humidity of a month, it also plot bar charts for of everyday for max
and min temperature.
"""
import glob
from datetime import datetime
import argparse

from colorama import Fore

from file_reader import read_file
import utils
from weather_data import WeatherData


class WeatherMan:
    """Weatherman class for weather reports.

    This class has 4 methods that prints different reports and
    it store path of the files from where the data is fetched
    """

    def __init__(self, path):
        """Weatherman object initilizer.

        it take path from the arguments and set it to it's instance variable
        """
        self.__path = path+'//'

    def year_files(self, year):  # fettching year files
        """Return year files.

        it take year and fetch that year files and return it
        """
        year_files = []
        directory_files = glob.glob(
            '{}Murree_weather_{}*'.format(self.__path, year))
        for file in directory_files:
            if str(year) in file:
                year_files.append(file)
        return year_files

    def highest_record_in_a_year(self, year):
        """Find Highest,Lowest temperature and most Humidity in a year.

        This method prints highest,lowest tempreture,most humidity of the
        year with month and day
        """
        year_weather_data = []
        year_files = self.year_files(year)  # given year files
        if not year_files:
            print('No Data Found For This Year')
            return
        for file in year_files:  # looping over list of files
            # tuple of list returned
            monthly_weather_data = read_file(file)
            year_weather_data += monthly_weather_data

        # calculating maximum,minimum and max humidity
        max_temperature_object = utils.get_max_temperature(year_weather_data)
        low_temperature_object = utils.get_min_temperature(year_weather_data)
        max_humid_object = utils.get_max_humidity(year_weather_data)
        # prinitng values to console
        print('Highest: {}C on {}'.format(
            str(max_temperature_object.max_temperature),
            max_temperature_object.get_weather_data_date()))
        print('Lowest: {}C on {}'.format(
            str(low_temperature_object.low_temperature),
            low_temperature_object.get_weather_data_date()))
        print('Humid: {}% on {}'.format(
            str(max_humid_object.max_humidity),
            max_humid_object.get_weather_data_date()))

    def average_record_in_a_month(self, weather_date):
        """Find average highest,lowest temperature and average Humidity in a month.

        This method prints average max,min temperature and
        humidity of a month
        """
        weather_date = datetime.strptime(weather_date, '%Y/%m')
        month = weather_date.strftime('%b')
        year = weather_date.strftime('%Y')
        highest_temp_average = 0
        lowest_temp_average = 0
        average_humidity = 0
        highest_temp_average_count = 0
        lowest_temp_average_count = 0
        average_humidity_count = 0

        file_path = '{}Murree_weather_{}_{}.txt'.format(
            self.__path, year, month)
        weather_data = read_file(file_path)

        for weather in weather_data:
            # checkin if the filed is empty and then adding it to the
            # averages for later use
            if weather.max_temperature:
                highest_temp_average += int(weather.max_temperature)
                highest_temp_average_count += 1
            if weather.low_temperature:
                lowest_temp_average += int(weather.low_temperature)
                lowest_temp_average_count += 1
            if weather.average_humidity:
                average_humidity += int(weather.average_humidity)
                average_humidity_count += 1

        # calculating average
        highest_temp_average = highest_temp_average // \
            highest_temp_average_count
        lowest_temp_average = lowest_temp_average // \
            lowest_temp_average_count
        average_humidity = average_humidity // \
            average_humidity_count
        print('Highest Average: {}C'.format(str(highest_temp_average)))
        print('Lowest Average: {}C'.format(str(lowest_temp_average)))
        print('Average Humidity: {}%'.format(str(average_humidity)))

    def highest_lowest_temprature_of_a_day_two_horizontal_bar_charts(
            self, weather_date):
        """Print Highest lowest Temperature in a Horizontal bar chart.

        This method prints max and min temperature seprately
        of each day of a month in horizontal bar chart
        """
        date_object = datetime.strptime(weather_date, '%Y/%m')
        # printing date in words
        print(date_object.strftime('%B %Y'))
        month = date_object.strftime('%b')
        year = date_object.strftime('%Y')
        weather_data = WeatherData()

        file_path = '{}Murree_weather_{}_{}.txt'.format(
            self.__path, year, month)
        weather_data = read_file(file_path)
        weather_date = 1
        for weather in weather_data:
            if weather.max_temperature:
                print(weather_date, end=' ')
                print(Fore.RED + '+' * int(weather.max_temperature), end='')
                print(Fore.WHITE +
                      str(' {}C'.format(weather.max_temperature)))
                print(weather_date, end=' ')
                print(Fore.BLUE + '+' *
                      int(weather.low_temperature), end='')
                print(Fore.WHITE +
                      str(' {}C'.format(weather.low_temperature)))
                weather_date += 1

    def highest_lowest_temprature_of_a_day_one_horzontal_bar_chart(
            self, weather_date
    ):
        """Print Highest,Lowest temperature in a single Horizontal bar chart.

        This method prints max and min temperature
        of each day of a month in one horizontal bar chart
        """
        date_object = datetime.strptime(weather_date, '%Y/%m')
        # printing date in words
        print(date_object.strftime('%B %Y'))
        month = date_object.strftime('%b')
        year = date_object.strftime('%Y')
        weather_date = WeatherData()

        file_path = '{}Murree_weather_{}_{}.txt'.format(
            self.__path, year, month)
        weather_data = read_file(file_path)
        weather_date = 1
        for weather in weather_data:
            # checkin if the filed is empty and then adding it to the
            if weather.max_temperature:
                print(weather_date, end=' ')
                print(Fore.BLUE + '+' *
                      int(weather.low_temperature), end='')
                print(Fore.RED + '+' * int(weather.max_temperature), end=' ')
                print(
                    Fore.WHITE+str(' {}C - {}C'.format(
                        weather.low_temperature,
                        weather.max_temperature
                    )))
                weather_date += 1


def main():
    """Weather man main method.

    main method of the program where arguments are
    evaluated and respective report is generated
    """
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
