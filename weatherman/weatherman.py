import argparse
import calendar
import os

from termcolor import colored

from results import ComputeResult
from csvparser import CsvParser


class WeatherReports:
    """Generate Weather Reports"""
    def __init__(self):
        self.results_dict = {}

    @staticmethod
    def extreme_weather(file_dir, year, month=None):
        """print extreme weather report"""
        weather = ComputeResult()
        weather.compute_extreme_weather(file_dir, year, month)

        max_temp_obj = weather.results_dict['max_temp']
        min_temp_obj = weather.results_dict['min_temp']
        max_humidity_obj = weather.results_dict['max_humidity']

        print('Highest Temp : {0}C on {1}'.format(max_temp_obj.max_temp,
                                                  max_temp_obj.date.strftime('%B %d')
                                                  )
              )
        print('lowest Temp : {0}C on {1}'.format(min_temp_obj.min_temp,
                                                 min_temp_obj.date.strftime('%B %d')
                                                 )
              )
        print('Max Humidity : {}% on {}'.format(max_humidity_obj.max_humidity,
                                                max_humidity_obj.date.strftime('%B %d')
                                                )
              )

    @staticmethod
    def average_weather(file_dir, year, month):
        """print avg weather report"""
        weather = ComputeResult()
        weather.compute_average_weather(file_dir, year, month)

        print('Avg Highest Temp : {0}C'.format(weather.results_dict['max_temp']))
        print('Avg lowest Temp : {0}C'.format(weather.results_dict['min_temp']))
        print('Avg Mean Humidity : {0}%'.format(weather.results_dict['mean_humidity']))

    @staticmethod
    def weather_charts(file_dir, year, month=None):
        """print weather charts """
        csv_parser = CsvParser(file_dir, year, month)

        for data_row in csv_parser.data_set:
            current_date = data_row.date.strftime('%d')

            print(current_date,
                  colored('+' * int(data_row.max_temp), 'red'),
                  '{0}C'.format(data_row.max_temp)
                  )
            print(current_date,
                  colored('+' * int(data_row.min_temp), 'blue'),
                  '{0}C'.format(data_row.min_temp)
                  )

    @staticmethod
    def weather_charts_merged(file_dir, year, month=None):
        """BONUS TASK: print weather charts on same line"""
        csv_parser = CsvParser(file_dir, year, month)

        for data_row in csv_parser.data_set:
            current_date = data_row.date.strftime('%d')
            red_chart = colored('+' * data_row.max_temp, 'blue')
            blue_chart = colored('+' * data_row.min_temp, 'red')
            charts = blue_chart + red_chart
            print(current_date,
                  charts,
                  '{0}C - {1}C'.format(data_row.max_temp, data_row.min_temp)
                  )


def validate_date(date_str):
    year, month = date_str('/')
    year = int(year)
    month = int(month)
    if month in range(1, len(calendar.month_name)):
        month = calendar.month_abbr[int(month)]
    else:
        raise ValueError('Month number not valid')
    return [year, month]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--extreme',
                        help='Generate highest lowest Temperature and Humidity Reports'
                        )

    parser.add_argument('-a', '--average',
                        help='Generate Avg Temperature and Humidity Reports'
                        )

    parser.add_argument('-c', '--charts',
                        help='Generate Charts high and low Temperature Reports'
                        )

    parser.add_argument('-b', '--bonus',
                        help='Generate Charts high and low Temperature Reports'
                        )

    parser.add_argument('file_dir',
                        help='Directory to files, use relative path like dir/to/files')

    args = parser.parse_args()
    if os.path.isdir(args.files_dir) is not None:
        raise FileNotFoundError('The directory doesn\'t exist')

    if args.extreme:
        year = int(args.extreme)
        WeatherReports.extreme_weather(args.file_dir, year)

    if args.average:
        year, month = validate_date(args.average)
        WeatherReports.average_weather(args.file_dir, year, month)

    if args.charts:
        year, month = validate_date(args.charts)
        WeatherReports.weather_charts(args.file_dir, year, month)

    if args.bonus:
        year, month = validate_date(args.bonus)
        WeatherReports.weather_charts_merged(args.file_dir, year, month)


if __name__ == "__main__":
    main()
