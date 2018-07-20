import argparse

from reporter import WeatherReporter
from weatherparser import WeatherParser
from weatheranalyzer import WeatherAnalyzer
from validator import Validator


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('directory_path', action="store", type=Validator.validate_path)

    parser.add_argument('-e', '--extreme', action='append', dest='extreme_query', default=[],
                        type=Validator.validate_year, help='Annual Extremes query')

    parser.add_argument('-c', '--chart', action='append', dest='chart_query', default=[],
                        type=Validator.validate_date, help='Temperatures in month')

    parser.add_argument('-a', '--average', action='append', dest='average_query', default=[],
                        type=Validator.validate_date, help='Average Temperature query')

    return parser.parse_args()


def main():
    arguments = parse_arguments()

    weather_parser = WeatherParser()

    weather_readings = weather_parser.parse(arguments.directory_path)

    if not weather_readings:
        print('Error:: No Record was found')
        return

    weather_analyzer = WeatherAnalyzer(weather_readings)

    if arguments.chart_query:
        for date in arguments.chart_query:
            WeatherReporter.display_chart(weather_analyzer.filter_readings(date))

    if arguments.average_query:
        for date in arguments.average_query:
            WeatherReporter.display_monthly_weather(weather_analyzer.monthly_average(date))

    if arguments.extreme_query:
        for date in arguments.extreme_query:
            WeatherReporter.display_annual_weather(weather_analyzer.annual_extremes(date))


if __name__ == "__main__":
    main()
