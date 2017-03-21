import argparse
from dateutil import parser
from dataoperations import DataOperations
from weatherdatareader import WeatherDataReader
from textreports import TextReports
from chartreports import ChartReports


class WeatherMan:
    __PKT = 'PKT'
    __MAX_TEMPERATURE = 'Max TemperatureC'
    __MIN_TEMPERATURE = 'Min TemperatureC'
    __MAX_HUMIDITY = 'Max Humidity'
    __MEAN_HUMIDITY = ' Mean Humidity'

    # Method to Display highest temperature and day, lowest temperature and day
    # And most humid day and humidity.
    @staticmethod
    def yearly_text_report(path, year):
        weather_records = WeatherDataReader.read_files(path, year, '')

        highest_temperature = DataOperations.find_max(
            weather_records, WeatherMan.__MAX_TEMPERATURE)
        lowest_temperature = DataOperations.find_min(
            weather_records, WeatherMan.__MIN_TEMPERATURE)
        most_humidity = DataOperations.find_max(
            weather_records, WeatherMan.__MAX_HUMIDITY)

        TextReports.yearly_report(
            highest_temperature, lowest_temperature, most_humidity)

    # Method to display the average highest temperature
    # And average lowest temperature, average humidity.
    @staticmethod
    def monthly_text_report(path, year, month):
        file_detail = WeatherDataReader.read_files(path, year, month)

        avg_max_temperature = DataOperations.average(
            file_detail, WeatherMan.__MAX_TEMPERATURE)
        avg_min_temperature = DataOperations.average(
            file_detail, WeatherMan.__MIN_TEMPERATURE)
        avg_mean_humidity = DataOperations.average(
            file_detail, WeatherMan.__MEAN_HUMIDITY)

        TextReports.monthly_report(
            avg_max_temperature, avg_min_temperature, avg_mean_humidity)

    # Method to draw horizontal bar chart on the console for the highest
    #  And lowest temperature on each day
    @staticmethod
    def monthly_chart_report(path, year, month, is_bonus_task):

        weather_records = WeatherDataReader.read_files(path, year, month)
        for single_day in weather_records:
            current_date = single_day[WeatherMan.__PKT]
            highest_temperature = single_day[WeatherMan.__MAX_TEMPERATURE]
            lowest_temperature = single_day[WeatherMan.__MIN_TEMPERATURE]
            if is_bonus_task:
                ChartReports.daily_stacked_bar_chart(
                    current_date.day, highest_temperature, lowest_temperature)
            else:
                ChartReports.daily_bar_chart(
                    current_date.day, highest_temperature, lowest_temperature)


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

    path = args.path
    date = parser.parse(args.date)

    if args.yearly_report:
        WeatherMan.yearly_text_report(path, date.year)
    elif args.monthly_report:
        WeatherMan.monthly_text_report(path, date.year, date.month)
    elif args.bar_chart:
        WeatherMan.monthly_chart_report(path, date.year, date.month, False)
    elif args.stacked_bar_chart:
        WeatherMan.monthly_chart_report(path, date.year, date.month, True)


if __name__ == "__main__":
    main()
