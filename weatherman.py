import argparse

from constants import ReportTypes
from report_generator import ReportGenerator
from validators import validate_arg_as_date, validate_arg_as_dir, validate_arg_as_year
from weather_data_analyzer import WeatherDataAnalyzer
from weather_data_parser import WeatherDataParser


def main():

    args = initialize_arguments()

    weather_readings = WeatherDataParser(args.dir_path).fetch_records()

    if args.e:
        show_extreme_stats(weather_readings, args.e)

    if args.a:
        show_mean_stats(weather_readings, args.a.month, args.a.year)

    if args.c:
        show_graphs(weather_readings, args.c.month, args.c.year)


def show_extreme_stats(weather_readings, year):

    results = WeatherDataAnalyzer(weather_readings, year=year).calculate_extremes()

    if results:
        report_generator = ReportGenerator(results)
        report_generator.generate(ReportTypes.SHOW_EXTREMES)


def show_mean_stats(weather_readings, month, year):
    results = WeatherDataAnalyzer(weather_readings, month=month, year=year).calculate_averages()

    if results:
        report_generator = ReportGenerator(results)
        report_generator.generate(ReportTypes.SHOW_MEANS)


def show_graphs(weather_readings, month, year):
    results = WeatherDataAnalyzer(weather_readings).fetch_records_of_month(month, year)

    if results:
        report_generator = ReportGenerator(results)
        report_generator.generate(ReportTypes.SHOW_GRAPHS)


def initialize_arguments():
    description = 'This is weather reports generation tool, which generates different types of reports depending ' \
                  'upon arguments.'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('dir_path',
                        type=validate_arg_as_dir,
                        help='Path to the directory of data files')

    parser.add_argument('-e',
                        type=validate_arg_as_year,
                        help='For a given year display the highest temperature and day, lowest temperature and day, '
                             'most humid day and humidity.')
    parser.add_argument('-a',
                        type=validate_arg_as_date,
                        help='For a given month, it displays the average highest temperature, average lowest '
                             'temperature, average mean humidity.')

    parser.add_argument('-c',
                        type=validate_arg_as_date,
                        help='For a given month, it draws two horizontal bar charts on the console for the highest and '
                             'lowest temperature on each day. Highest in red and lowest in blue.')

    return parser.parse_args()


if __name__ == '__main__':
    main()
