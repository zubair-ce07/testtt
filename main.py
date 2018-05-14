import argparse
import sys
from weatherparser import WeatherParser
from weatheranalyzer import WeatherAnalyzer
from weatherreport import WeatherReport


def error_message_exit():
    print('No record found....')
    sys.exit()


def read_monthly_weather(date, directory):
    weather_parser = WeatherParser()
    return weather_parser.read_weather_file(date, directory)


def read_yearly_weather(date, directory):
    weather_parser = WeatherParser()
    yearly_weather = weather_parser.read_weather_file(date, directory)
    if not yearly_weather:
        error_message_exit()
    weather_analyzer = WeatherAnalyzer(yearly_weather)
    return weather_analyzer


def get_yearly_weather(date, directory):
    weather_date = date.split('/')
    weather_report = WeatherReport()
    weather_analyzer = read_yearly_weather(weather_date[0], directory)
    weather_analyzer.calculate_weather_extremes()
    weather_report.display_yearly_weather(weather_analyzer.max_weather,
                                          weather_analyzer.min_weather,
                                          weather_analyzer.max_humidity)


def get_monthly_weather(date, directory):
    monthly_weather = read_monthly_weather(date, directory)
    if monthly_weather is None:
        error_message_exit()
    weather_analyzer = WeatherAnalyzer(monthly_weather)
    weather_analyzer.calculate_weather_averages()
    weather_report = WeatherReport()
    weather_report.display_monthly_weather(weather_analyzer.max_temp_avrg,
                                           weather_analyzer.min_temp_avrg,
                                           weather_analyzer.max_humidity_avrg)


def get_monthly_graphed_weather(date, directory):
    monthly_weather = read_monthly_weather(date, directory)
    if monthly_weather is None:
        error_message_exit()
    weather_report = WeatherReport()
    weather_report.monthly_graph(monthly_weather)


def get_day_wise_graphed_weather(date, directory):
    monthly_weather = read_monthly_weather(date, directory)
    if monthly_weather is None:
        error_message_exit()
    weather_report = WeatherReport()
    weather_report.merged_graph(monthly_weather)


def weather_date(date):
    monthly_date = date.split('/')
    if len(monthly_date) < 2:
        print ('Invalid Input')
        sys.exit()
    if not 1 <= int(monthly_date[1]) <= 12:
        print ('Invalid Input')
        sys.exit()
    return date


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory')
    parser.add_argument('-e', type=int)
    parser.add_argument('-a', type=weather_date)
    parser.add_argument('-c', type=weather_date)
    parser.add_argument('-g', type=weather_date)
    args = parser.parse_args()

    if args.a:
        get_monthly_weather(args.a, args.directory)
    if args.e:
        get_yearly_weather(str(args.e), args.directory)
    if args.c:
        get_monthly_graphed_weather(args.c, args.directory)
    if args.g:
        get_day_wise_graphed_weather(args.g, args.directory)


if __name__ == "__main__":
    main()
