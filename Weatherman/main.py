import os
import argparse
import calendar
import warnings

from weather_readings_reader import WeatherReadingsReader
from report_generator import ReportGenerator


def validate_month(argument):
    try:
        year, month = argument.split('/')
    except Exception:
        raise argparse.ArgumentTypeError("Argument Type Error. Enter in the form of int/int")
    if not int(year) or not int(month) in range(1, 13):
        raise argparse.ArgumentTypeError("Year should be an integer month should be an integer from 1-12")
    return argument


def validate_directory(path):
    if os.path.isdir(path):
        return path
    raise argparse.ArgumentTypeError(f"Invalid directory path")


def month_argument_reader(argument):
    year, month = argument.split('/')
    return int(year), calendar.month_abbr[int(month)]


def run(args):
    my_path = args.directory
    if args.type_e:
        weather_readings = WeatherReadingsReader.read_readings(my_path, args.type_e)
        if weather_readings:
            ReportGenerator.get_annual_report(weather_readings)
        else:
            warnings.warn(f'Could not find Any Data for {args.type_e}')
    if args.type_a:
        year, month_name = month_argument_reader(args.type_a)
        weather_readings = WeatherReadingsReader.read_readings(my_path, year, month_name)
        if weather_readings:
            ReportGenerator.get_month_report(month_name, year, weather_readings)
        else:
            warnings.warn(f'Could not find Any Data for {args.type_a}')
    if args.type_c:
        year, month_name = month_argument_reader(args.type_c)
        weather_readings = WeatherReadingsReader.read_readings(my_path, year, month_name)
        if weather_readings:
            ReportGenerator.get_bar_report('c', args.type_c, weather_readings)
        else:
            warnings.warn(f'Could not find Any Data for {args.type_c}')
    if args.type_d:
        year, month_name = month_argument_reader(args.type_d)
        weather_readings = WeatherReadingsReader.read_readings(my_path, year, month_name)
        if weather_readings:
            ReportGenerator.get_bar_report('d', args.type_d, weather_readings)
        else:
            warnings.warn(f'Could not find Any Data for {args.type_d}')


def main():
    parser = argparse.ArgumentParser(description='Report will be generated according to the Arguments')
    parser.add_argument('directory', type=validate_directory, help='Enter the directory')
    parser.add_argument('-e', '--type_e', type=int, help='Annual Report')
    parser.add_argument('-a', '--type_a', type=validate_month, help='Monthly Report year/month')
    parser.add_argument('-c', '--type_c', type=validate_month, help='Dual Bar Chart year/month')
    parser.add_argument('-d', '--type_d', type=validate_month, help='Single Bar Chart year/month')
    args = parser.parse_args()
    run(args)


if __name__ == '__main__':
    main()
