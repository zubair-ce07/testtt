import argparse
import calendar
import csv
import glob
from dateutil import parser
from termcolor import colored


class WeatherDataReader:
    def __init__(self):
        self.months = calendar.month_name

        self.pkt = 'PKT'
        self.max_temperature_c = 'Max TemperatureC'
        self.min_temperature_c = 'Min TemperatureC'
        self.max_humidity = 'Max Humidity'
        self.mean_humidity = 'Mean Humidity'

        self.data_fields = ['PKT', 'Max TemperatureC', 'Mean TemperatureC',
                            'Min TemperatureC', 'Dew PointC',
                            'MeanDew PointC', 'Min DewpointC', 'Max Humidity',
                            'Mean Humidity', 'Min Humidity',
                            'Max Sea Level PressurehPa',
                            'Mean Sea Level PressurehPa',
                            'Min Sea Level PressurehPa', 'Max VisibilityKm',
                            'Mean VisibilityKm', 'Min VisibilitykM',
                            'Max Wind SpeedKm/h', 'Mean Wind SpeedKm/h',
                            'Max Gust SpeedKm/h', 'PrecipitationCm',
                            'CloudCover', 'Events', 'WindDirDegrees'
                            ]

    def read_single_file(self, file_path):
        with open(file_path) as weather_record_file:
            # Read File as List of Dictionaries
            weather_record_reader = csv.DictReader(
                weather_record_file, self.data_fields)
            next(weather_record_reader)  # Skip Header
            file_details = list(weather_record_reader)
            file_details.pop()  # Skip Footer

            for index, cols in enumerate(file_details[0:], 0):
                file_details[index][self.pkt] = \
                    parser.parse(cols[self.pkt])
                file_details[index][self.max_temperature_c] = \
                    int(cols[self.max_temperature_c])
                file_details[index][self.min_temperature_c] = \
                    int(cols[self.min_temperature_c])
                file_details[index][self.max_humidity] = \
                    int(cols[self.max_humidity])
                file_details[index][self.mean_humidity] = \
                    int(cols[self.mean_humidity])

            return file_details

    def find_and_read_file(self, year, month, path):
        month = self.months[month]

        files = glob.glob('{path}/*{year}*{month}*.txt'.format(
            path=path, year=year, month=month[:3]))

        file_detail = []

        # Find all files that matches the given pattern
        for file_name in files:
            file_detail.extend(self.read_single_file(file_name))

        return file_detail


class WeatherMan:
    def __init__(self):
        self.months = calendar.month_name

        self.pkt = 'PKT'
        self.max_temperature_c = 'Max TemperatureC'
        self.min_temperature_c = 'Min TemperatureC'
        self.max_humidity = 'Max Humidity'
        self.mean_humidity = 'Mean Humidity'

        self.red_color = 'red'
        self.blue_color = 'blue'

    # Method to Display highest temperature and day, lowest temperature and day
    # And most humid day and humidity.
    def highest_lowest_humid(self, year, path):
        highest_temperature = 0
        highest_temperature_day_month = 0
        highest_temperature_day = 0
        lowest_temperature = 100
        lowest_temperature_day_month = 0
        lowest_temperature_day = 0
        most_humidity = 0
        most_humid_day_month = 0
        most_humid_day = 0

        files = glob.glob('{path}/*{year}*.txt'.format(path=path, year=year))

        for file_name in files:
            weather_data_reader = WeatherDataReader()
            file_detail = weather_data_reader.read_single_file(file_name)

            index = max(xrange(
                len(file_detail)),
                key=lambda day: file_detail[day][self.max_temperature_c])
            tmp_highest_temperature = \
                file_detail[index][self.max_temperature_c]

            # Finding Highest Max Temperature
            if tmp_highest_temperature > highest_temperature:
                highest_temperature = tmp_highest_temperature
                highest_temperature_day_month = \
                    file_detail[index][self.pkt].month
                highest_temperature_day = file_detail[index][self.pkt].day

            index = min(xrange(
                len(file_detail)),
                key=lambda day: file_detail[day][self.min_temperature_c])
            tmp_lowest_temperature = \
                file_detail[index][self.min_temperature_c]

            # Finding Lowest Min Temperature
            if tmp_lowest_temperature < lowest_temperature:
                lowest_temperature = tmp_lowest_temperature
                lowest_temperature_day_month = \
                    file_detail[index][self.pkt].month
                lowest_temperature_day = file_detail[index][self.pkt].day

            index = max(xrange(len(file_detail)),
                        key=lambda day: file_detail[day][self.max_humidity])
            tmp_most_humidity = file_detail[index][self.max_humidity]

            # Finding Highest Max Temperature
            if tmp_most_humidity > most_humidity:
                most_humidity = tmp_most_humidity
                most_humid_day_month = file_detail[index][self.pkt].month
                most_humid_day = file_detail[index][self.pkt].day

        print 'Highest: {temp}C on {month} {day}'.format(
            temp=highest_temperature,
            month=self.months[highest_temperature_day_month],
            day=highest_temperature_day)
        print 'Lowest: {temp}C on {month} {day}'.format(
            temp=lowest_temperature,
            month=self.months[lowest_temperature_day_month],
            day=lowest_temperature_day)
        print "Humid: {humidity}% on {month} {day}".format(
            humidity=most_humidity,
            month=self.months[most_humid_day_month], day=most_humid_day)

    @staticmethod
    def calculate_average(weather_parameter, file_detail):
        sum_weather_parameter = sum(
            single_day[weather_parameter] for single_day in file_detail)
        return sum_weather_parameter / len(file_detail)

    # Method to display the average highest temperature
    # And average lowest temperature, average humidity.
    def average_highest_lowest_humid(self, year, month, path):
        weather_data_reader = WeatherDataReader()
        file_detail = weather_data_reader.find_and_read_file(year, month, path)

        avg_max_temperature_c = WeatherMan.calculate_average(
            self.max_temperature_c, file_detail)
        avg_min_temperature_c = WeatherMan.calculate_average(
            self.min_temperature_c, file_detail)
        avg_mean_humidity = WeatherMan.calculate_average(
            self.mean_humidity, file_detail)

        print 'Highest Average: {avg_max_temperature_c}C'.format(
            avg_max_temperature_c=avg_max_temperature_c)
        print 'Lowest Average: {avg_min_temperature_c}C'.format(
            avg_min_temperature_c=avg_min_temperature_c)
        print 'Average Humidity: {avg_mean_humidity}%'.format(
            avg_mean_humidity=avg_mean_humidity)

    @staticmethod
    def colored_print(temperature, color):
        bar_chart = ""
        for index in range(int(temperature)):
            bar_chart += colored('+', color)
        return bar_chart

    @staticmethod
    def display_bar_chart(current_day, temperature, color):
        bar_chart = ""
        bar_chart += str(current_day) + " "
        bar_chart += WeatherMan.colored_print(temperature, color)
        bar_chart += " " + str(temperature) + "C"
        print bar_chart

    def display_double_chart_per_day(
            self, current_day, highest_temperature, lowest_temperature):
        WeatherMan.display_bar_chart(
            current_day, highest_temperature, self.red_color)
        WeatherMan.display_bar_chart(
            current_day, lowest_temperature, self.blue_color)

    def display_single_chart_per_day(
            self, current_day, highest_temperature, lowest_temperature):
        bar_chart = ""
        bar_chart += str(current_day) + " "
        bar_chart += WeatherMan.colored_print(
            lowest_temperature, self.blue_color)
        bar_chart += WeatherMan.colored_print(
            highest_temperature, self.red_color)
        bar_chart += " " + str(lowest_temperature) + "C - "
        bar_chart += str(highest_temperature) + "C"
        print bar_chart

    # Method to draw horizontal bar chart on the console for the highest
    # And lowest temperature on each day
    def display_bar_chart_by_month(self, year, month, path, is_bonus_task):

        weather_data_reader = WeatherDataReader()
        file_detail = weather_data_reader.find_and_read_file(year, month, path)

        for single_day in file_detail:
            current_date = single_day[self.pkt]
            highest_temperature = single_day[self.max_temperature_c]
            lowest_temperature = single_day[self.min_temperature_c]
            if is_bonus_task:
                self.display_single_chart_per_day(
                    current_date.day, highest_temperature, lowest_temperature)
            else:
                self.display_double_chart_per_day(
                    current_date.day, highest_temperature, lowest_temperature)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-e', action='store_true',
                            dest='highest_lowest_temp_humid',
                            help='Highest,Lowest Temperature and Humidity')
    arg_parser.add_argument('-a', action='store_true',
                            dest='avg_highest_lowest_temp_humidity',
                            help='Average Temperature and Humidity')
    arg_parser.add_argument('-c', action='store_true',
                            dest='separate_bar_chart',
                            help='Two Bar Chart per Day')
    arg_parser.add_argument('-b', action='store_true',
                            dest='joint_bar_chart',
                            help='One Bar Chart per Day')
    arg_parser.add_argument('date', type=str, help='date argument')
    arg_parser.add_argument('path', type=str, help='path to files')
    args = arg_parser.parse_args()

    weatherman = WeatherMan()

    path = args.path
    date = parser.parse(args.date)

    try:
        if args.highest_lowest_temp_humid:
            weatherman.highest_lowest_humid(date.year, path)

        elif args.avg_highest_lowest_temp_humidity:
            weatherman.average_highest_lowest_humid(
                date.year, date.month, path)

        elif args.separate_bar_chart:
            weatherman.display_bar_chart_by_month(
                date.year, date.month, path, False)

        elif args.joint_bar_chart:
            weatherman.display_bar_chart_by_month(
                date.year, date.month, path, True)
        else:
            print ("You have not provide option kindly help")

    except OSError:
        print("Given arguments are not correct.")


if __name__ == "__main__":
    main()
