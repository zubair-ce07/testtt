"""Start of the application"""

import argparse
from weatherman_application import WeathermanApplication


parser = argparse.ArgumentParser(description="Take path as fist argument to the Weather files folder")
parser.add_argument("path", type=str)
parser.add_argument("-e", type=int, nargs='*')
parser.add_argument("-a", type=str, nargs='*')
parser.add_argument("-c", type=str, nargs="*")
args = parser.parse_args()


if args.e:
    for year in args.e:
        weatherman = WeathermanApplication(args.path)
        weatherman.read_year_files(year)
        weatherman.find_highest_lowest_temperature_and_max_humidity()
if args.a:
    for year_month in args.a:
        year_month = year_month.split('/')
        year_month = [int(year_month[0]), int(year_month[1])]
        weatherman = WeathermanApplication(args.path)
        weatherman.read_month_files(year_month[0],year_month[1])
        weatherman.find_average_max_temp_low_temp_and_mean_humidity()
if args.c:
    for year_month in args.c:
        year_month = year_month.split('/')
        year_month = [int(year_month[0]), int(year_month[1])]
        weatherman = WeathermanApplication(args.path)
        weatherman.read_month_files(year_month[0],year_month[1])
        weatherman.bar_chart_vertically()
        weatherman.bar_chart_horizentally()

