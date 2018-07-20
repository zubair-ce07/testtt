import argparse
import datetime
import os

from weather_record_parser import WeatherDataParser
from weather_analyzer import WeatherAnalyzer
from weather_reporter import WeatherReporter


def valid_year(year):
    if int(year) > datetime.date.today().year:
        raise argparse.ArgumentTypeError(f"Max year is {datetime.date.today().year}")
    return int(year)


def valid_year_month(date):
    try:
        date = datetime.datetime.strptime(date, '%Y/%m')
    except ValueError:
        raise argparse.ArgumentTypeError(f"The Date is not valid")

    return valid_year(date.year), date.month


def validate_path(file_path):
    if os.path.isdir(file_path):
        return file_path
    raise argparse.ArgumentTypeError(f"The given directory does not exist")


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("file_path", help="Get the path to all weather data files", type=validate_path)
    parser.add_argument("-e", help="Get the highest and lowest temperature and highest humidity "
                                   "with respective days for given year", type=valid_year)
    parser.add_argument("-a", help="Get the highest and lowest avg temperature and Mean avg "
                                   "Humidity for a given month", type=valid_year_month)
    parser.add_argument("-c", help="For a given month get two horizontal bar charts on the console "
                                   "for the highest and lowest temperature on each day. "
                                   "Highest in red and lowest in blue.", type=valid_year_month)
    parser.add_argument("-b", help="For a given month get one horizontal bar charts on the console "
                                   "for the highest and lowest temperature on each day. "
                                   "Highest in red and lowest in blue.", type=valid_year_month)

    return parser.parse_args()


def main(cli_arguments):
    file_path = cli_arguments.file_path
    weather_record_parser = WeatherDataParser()
    parsed_weather_records = weather_record_parser.parse(file_path)

    if cli_arguments.e:
        weather_result = WeatherAnalyzer.get_result(parsed_weather_records, cli_arguments.e)
        WeatherReporter.print_annual_report(weather_result)

    if cli_arguments.a:
        year, month = cli_arguments.a
        weather_result = WeatherAnalyzer.get_result(parsed_weather_records, year, month)
        WeatherReporter.print_monthly_report(weather_result)

    if cli_arguments.c:
        year, month = cli_arguments.c
        weather_result = WeatherAnalyzer.get_result(parsed_weather_records, year, month)
        WeatherReporter.print_charts_for_extremes(weather_result, 'c')

    if cli_arguments.b:
        year, month = cli_arguments.b
        weather_result = WeatherAnalyzer.get_result(parsed_weather_records, year, month)
        WeatherReporter.print_charts_for_extremes(weather_result, 'b')


if __name__ == "__main__":
    commandline_arguments = parse_arguments()
    main(commandline_arguments)
