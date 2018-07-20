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

    parser.add_argument("file_path", help="This arg stores the path to all weather data files",
                                     type=validate_path)
    parser.add_argument("-e", help="This command will give you the highest and "
                                   "lowest temperature and highest humidity with "
                                   "respective days for given year", type=valid_year)
    parser.add_argument("-a", help="This command will give you the highest and "
                                   "lowest avg temperature and Mean avg Humidity"
                                   "for a given month", type=valid_year_month)
    parser.add_argument("-c", help="For a given month this command will draw two "
                                   "horizontal bar charts on the console for the "
                                   "highest and lowest temperature on each day. "
                                   "Highest in red and lowest in blue.", type=valid_year_month)
    parser.add_argument("-b", help="For a given month this command will draw one "
                                   "horizontal bar charts on the console for the "
                                   "highest and lowest temperature on each day. "
                                   "Highest in red and lowest in blue.", type=valid_year_month)

    return parser.parse_args()


def main(commandline_arguments):
    file_path = commandline_arguments.file_path

    if commandline_arguments.e:
        weather_record_parser = WeatherDataParser()
        parsed_weather_records = weather_record_parser.parse(file_path)
        weather_result = WeatherAnalyzer.get_result(parsed_weather_records, commandline_arguments.e)
        WeatherReporter.print_annual_report(weather_result)

    if commandline_arguments.a:
        year, month = commandline_arguments.a
        weather_record_parser = WeatherDataParser()
        parsed_weather_records = weather_record_parser.parse(file_path)
        weather_result = WeatherAnalyzer.get_result(parsed_weather_records, year, month)
        WeatherReporter.print_monthly_report(weather_result)

    if commandline_arguments.c:
        year, month = commandline_arguments.c
        weather_record_parser = WeatherDataParser()
        parsed_weather_records = weather_record_parser.parse(file_path)
        weather_result = WeatherAnalyzer.get_result(parsed_weather_records, year, month)
        WeatherReporter.print_charts_for_extremes(weather_result)

    if commandline_arguments.b:
        year, month = commandline_arguments.b
        weather_record_parser = WeatherDataParser()
        parsed_weather_records = weather_record_parser.parse(file_path)
        weather_result = WeatherAnalyzer.get_result(parsed_weather_records, year, month)
        WeatherReporter.print_mixed_chart_for_extremes(weather_result)


if __name__ == "__main__":
    commandline_arguments = parse_arguments()
    main(commandline_arguments)
