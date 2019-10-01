import argparse

from CalculateResults import WeatherResultsCalculator
from Reports import WeatherReportGenerator
from WeatherFilesParser import WeatherFilesParser


def arg_parser():
    arguments = argparse.ArgumentParser(description='Arguments for weatherman.py')
    arguments.add_argument('Path', metavar='path', type=str, help='the path to the files')
    arguments.add_argument('-e', help='Display Highest, Lowest temperatures and most humid day of given year')
    arguments.add_argument('-a', help='Average highest and lowest temps for given month')
    arguments.add_argument('-c', help='Display bars of temps of warmest and coldest days of given month')
    arguments.add_argument('-d', help='[BONUS] Display bars of temps of warmest and coldest days of given month')
    return arguments.parse_args()


def main():
    args = arg_parser()
    file_parser = WeatherFilesParser()
    result_calculator = WeatherResultsCalculator()
    show_results = WeatherReportGenerator()
    if args.e:
        weather_readings = file_parser.parse_files(args.Path, args.e)
        yearly_temperatures_results = result_calculator.calculate_yearly_high_low_weather(weather_readings)
        show_results.generate_yearly_report(yearly_temperatures_results)

    if args.a:
        weather_readings = file_parser.parse_files(args.Path, args.a)
        monthly_avg_result = result_calculator.calculate_monthly_avg_weather(weather_readings)
        show_results.generate_monthly_avg_report(monthly_avg_result)

    if args.c:
        weather_readings = file_parser.parse_files(args.Path, args.c)
        show_results.generate_monthly_temperatures_report(weather_readings, False)

    if args.d:
        weather_readings = file_parser.parse_files(args.Path, args.d)
        show_results.generate_monthly_temperatures_report(weather_readings, True)


if __name__ == "__main__":
    main()
