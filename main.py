import argparse
import calendar
import os
import sys
from weatherparser import WeatherParser
from weatheranalyzer import WeatherAnalyzer
from weatherreport import WeatherReport


def generate_yearly_filename(year, directory):
    return [directory + '/Murree_weather_' + year + '_' + calendar.month_abbr[int(months_count)] \
            + '.txt' for months_count in range(12)]


def generate_monthly_filename(date, directory):
    weather_date = date.split("/")
    filename = directory + '/Murree_weather_' + weather_date[0] + '_' \
               + calendar.month_abbr[int(weather_date[1])] + '.txt'
    return filename


def error_message_exit(input=True, record=True):
    if not input:
        print('Invalid Input')
    elif not record:
        print('No record found....')
    sys.exit()


def read_monthly_weather(filepath):
    weather = WeatherParser()
    return weather.read_weather_file(filepath)


def read_yearly_weather(filenames):
    weather_analyzer = WeatherAnalyzer()
    yearly_weather = False

    for month_wise_files_counter in filenames:
        weather_record = read_monthly_weather(month_wise_files_counter)
        if weather_record:
            weather_analyzer.initialize_weather_record(weather_record)
            yearly_weather = True

    if not yearly_weather:
        error_message_exit(True, False)

    return weather_analyzer


def get_yearly_weather(date, directory):
    weather_date = date.split('/')
    filenames = generate_yearly_filename(weather_date[0], directory)
    weather_report = WeatherReport()
    weather_analyzer = read_yearly_weather(filenames)

    weather_report.display_yearly_weather(weather_analyzer.highest_temperature,
                                          weather_analyzer.hightest_temperature_date,
                                          weather_analyzer.lowest_temperature,
                                          weather_analyzer.lowest_temperature_date,
                                          weather_analyzer.highest_humidity,
                                          weather_analyzer.highest_humidity_date)


def get_monthly_weather(date, directory):
    filepath = generate_monthly_filename(date, directory)
    monthly_weather = read_monthly_weather(filepath)

    if not monthly_weather:
        error_message_exit(True, False)

    weather_analyzer = WeatherAnalyzer()
    weather_report = WeatherReport()
    weather_analyzer.initialize_weather_record(monthly_weather)
    weather_report.display_monthly_weather(weather_analyzer.highest_average,
                                           weather_analyzer.lowest_average,
                                           weather_analyzer.average_mean_humidity)


def get_monthly_graphed_weather(date, directory):
    filepath = generate_monthly_filename(date, directory)
    monthly_weather = read_monthly_weather(filepath)

    if not monthly_weather:
        error_message_exit(True, False)

    weather_analyzer = WeatherAnalyzer()
    weather_report = WeatherReport()
    weather_analyzer.initialize_weather_record(monthly_weather)
    weather_report.monthly_graph(weather_analyzer.max_temperatures, weather_analyzer.min_temperatures)


def get_day_wise_graphed_weather(date, directory):
    filepath = generate_monthly_filename(date, directory)
    monthly_weather = read_monthly_weather(filepath)

    if not monthly_weather:
        error_message_exit(True, False)

    weather_analyzer = WeatherAnalyzer()
    weather_report = WeatherReport()
    weather_analyzer.initialize_weather_record(monthly_weather)
    weather_report.merged_graph(weather_analyzer.max_temperatures, weather_analyzer.min_temperatures)


def main ():
    os.system('clear')
    parser = argparse.ArgumentParser()
    parser.add_argument('directory')
    parser.add_argument('-e', type=int)
    parser.add_argument('-a')
    parser.add_argument('-c')
    parser.add_argument('-g')
    args = parser.parse_args()

    if args.a is not None:
        get_monthly_weather(args.a, args.directory)
    if args.e is not None:
        get_yearly_weather(str(args.e), args.directory)
    if args.c is not None:
        get_monthly_graphed_weather(args.c, args.directory)
    if args.g is not None:
        get_day_wise_graphed_weather(args.g, args.directory)


if __name__== "__main__":
    main()
