import argparse
import calendar
import os
import sys
from weatherparser import WeatherParser
from weatheranalyzer import WeatherAnalyzer
from weatherreport import WeatherReport


def error_message_exit():
    print('No record found....')
    sys.exit()


def read_monthly_weather(date, directory):
    weather = WeatherParser()
    filename = weather.generate_monthly_filename(date, directory)
    return weather.read_weather_file(filename)


def read_yearly_weather(date, directory):
    weather = WeatherParser()
    yearly_weather = False
    weather_data = []
    filenames = weather.generate_yearly_filename(date, directory)
    for month_wise_files_counter in filenames:
        weather_record = weather.read_weather_file(month_wise_files_counter)
        if weather_record:
            weather_data += weather_record
            yearly_weather = True

    if not yearly_weather:
        error_message_exit()

    weather_analyzer = WeatherAnalyzer(weather_data)
    # weather_analyzer.test()
    # sys.exit()
    return weather_analyzer



def get_yearly_weather(date, directory):
    weather_date = date.split('/')
    weather_report = WeatherReport()
    weather_analyzer = read_yearly_weather(weather_date[0], directory)
    weather_analyzer.calculate_weather_extremes()
    print (weather_analyzer.max_weather)
    print (weather_analyzer.min_weather)
    print (weather_analyzer.max_humidity)


def get_monthly_weather(date, directory):
    monthly_weather = read_monthly_weather(date, directory)

    if monthly_weather is None:
        error_message_exit()

    weather_analyzer = WeatherAnalyzer(monthly_weather)
    weather_analyzer.calculate_weather_extremes()
    # weather_analyzer.test()
    # sys.exit()
    # weather_analyzer.calculat_weather_averages()
    # print (weather_analyzer.max_temp_avrg)
    # print (weather_analyzer.min_temp_avrg)
    # print (weather_analyzer.max_humidity_avrg)
    print (weather_analyzer.max_weather)
    print (weather_analyzer.min_weather)
    print (weather_analyzer.max_humidity)
    return
    weather_report = WeatherReport()
    weather_analyzer.initialize_weather_record(monthly_weather)
    weather_report.display_monthly_weather(weather_analyzer.highest_average,
                                           weather_analyzer.lowest_average,
                                           weather_analyzer.average_mean_humidity)

def get_monthly_graphed_weather(date, directory):
    monthly_weather = read_monthly_weather(date, directory)

    if monthly_weather is None:
        error_message_exit()

    weather_analyzer = WeatherAnalyzer()
    weather_report = WeatherReport()
    weather_analyzer.initialize_weather_record(monthly_weather)
    weather_report.monthly_graph(weather_analyzer.max_temperatures, weather_analyzer.min_temperatures)


def get_day_wise_graphed_weather(date, directory):
    monthly_weather = read_monthly_weather(date, directory)

    if monthly_weather is None:
        error_message_exit()

    weather_analyzer = WeatherAnalyzer()
    weather_report = WeatherReport()
    weather_analyzer.initialize_weather_record(monthly_weather)
    weather_report.merged_graph(weather_analyzer.max_temperatures, weather_analyzer.min_temperatures)


def main ():
    # os.system('clear')
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
