import argparse
from dateutil import parser
from dataoperations import DataOperations
from weatherdatareader import WeatherDataReader
from textreports import TextReports
from chartreports import ChartReports


class WeatherMan:
    def __init__(self):
        pass

    PKT = 'PKT'
    MAX_TEMPERATURE = 'Max TemperatureC'
    MIN_TEMPERATURE = 'Min TemperatureC'
    MAX_HUMIDITY = 'Max Humidity'
    MEAN_HUMIDITY = ' Mean Humidity'

    # Method to Display highest temperature and day, lowest temperature and day
    # And most humid day and humidity.
    @staticmethod
    def yearly_text_report(path, year):

        highest_temperature = {'key': 0, 'month': 0, 'day': 0}
        lowest_temperature = {'key': 100, 'month': 0, 'day': 0}
        most_humidity = {'key': 0, 'month': 0, 'day': 0}

        files = WeatherDataReader.find_files(path, year, '')

        for file_name in files:
            weather_records = WeatherDataReader.read_single_file(file_name)

            highest_temperature = DataOperations.find_max(
                highest_temperature, weather_records, WeatherMan.MAX_TEMPERATURE)

            lowest_temperature = DataOperations.find_min(
                lowest_temperature, weather_records, WeatherMan.MIN_TEMPERATURE)

            most_humidity = DataOperations.find_max(
                most_humidity, weather_records, WeatherMan.MAX_HUMIDITY)

        TextReports.display_yearly_report(
            highest_temperature, lowest_temperature, most_humidity)

    # Method to display the average highest temperature
    # And average lowest temperature, average humidity.
    def monthly_text_report(self, path, year, month):
        file_detail = WeatherDataReader.read_file(path, year, month)

        avg_max_temperature = DataOperations.calculate_average(
            file_detail, self.MAX_TEMPERATURE)
        avg_min_temperature = DataOperations.calculate_average(
            file_detail, self.MIN_TEMPERATURE)
        avg_mean_humidity = DataOperations.calculate_average(
            file_detail, self.MEAN_HUMIDITY)

        TextReports.display_monthly_report(
            avg_max_temperature, avg_min_temperature, avg_mean_humidity)

    @staticmethod
    def monthly_chart_report(path, year, month, is_bonus_task):

        weather_records = WeatherDataReader.read_file(path, year, month)
        ChartReports.display_monthly_report(weather_records, is_bonus_task)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-e', action='store_true',
                            dest='yearly_report',
                            help='Highest,Lowest Temperature and Humidity')
    arg_parser.add_argument('-a', action='store_true',
                            dest='monthly_report',
                            help='Average Temperature and Humidity')
    arg_parser.add_argument('-c', action='store_true',
                            dest='bar_chart',
                            help='Two Bar Chart per Day')
    arg_parser.add_argument('-b', action='store_true',
                            dest='stacked_bar_chart',
                            help='One Bar Chart per Day')
    arg_parser.add_argument('date', type=str, help='date argument')
    arg_parser.add_argument('path', type=str, help='path to files')
    args = arg_parser.parse_args()

    weatherman = WeatherMan()

    path = args.path
    date = parser.parse(args.date)

    if args.yearly_report:
        WeatherMan.yearly_text_report(path, date.year)
    elif args.monthly_report:
        weatherman.monthly_text_report(path, date.year, date.month)

    elif args.bar_chart:
        weatherman.monthly_chart_report(path, date.year, date.month, False)

    elif args.stacked_bar_chart:
        weatherman.monthly_chart_report(path, date.year, date.month, True)


if __name__ == "__main__":
    main()
