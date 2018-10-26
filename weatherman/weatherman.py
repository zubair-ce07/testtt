import argparse
import os.path
import re

from weather_reports import WeatherReports


def main():
    args = validate_argumets()
    weatherman = WeatherReports()

    if args.extreme:
        for date in args.extreme:
            year, month = validate_date(date)
            weatherman.extreme_weather(args.dir, year, month)

    if args.average:
        for date in args.average:
            year, month = validate_date(date)
            weatherman.average_weather(args.dir, year, month)

    if args.charts:
        for date in args.charts:
            year, month = validate_date(date)
            weatherman.weather_charts(args.dir, year, month, 'c')

    if args.charts_bonus:
        for date in args.charts_bonus:
            year, month = validate_date(date)
            weatherman.weather_charts(args.dir, year, month, 'cb')


def arguments_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="Data DIR path", type=str)
    parser.add_argument("-e", "--extreme", nargs="*", type=str)
    parser.add_argument("-a", "--average", nargs="*", type=str)
    parser.add_argument("-c", "--charts", nargs="*", type=str)
    parser.add_argument("-cb", "--charts_bonus", nargs="*", type=str)
    return parser.parse_args()


def validate_argumets():
    parser = arguments_parser()

    if os.path.isdir(parser.dir) is None:
        raise FileNotFoundError('Provide existing path of directory')

    return parser


def validate_date(date):

    if not re.search(r'\d{4}/?\d{0,2}', date):
        raise ValueError('Provide existing path of directory')

    return date.split("/") if "/" in date else [date, None]


if __name__ == "__main__":
    main()
