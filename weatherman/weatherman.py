import re
import calendar
import argparse
import os.path

from weatherman_class import WeathermanClass
from file_reading import data_reading


def main():
    cmd_args = validate_argumets()
    weatherman = WeathermanClass()
    if cmd_args.year:
        for year in cmd_args.year:
            weather_data = data_reading(cmd_args.dir, None, year)
            if weather_data:
                print("---------Weather Report of " + year + "---------")
                weatherman.max_temp_min_temp_max_humidity(weather_data)
            else:
                print("Data not found")
    if cmd_args.month:
        for month in cmd_args.month:
            year_month = date_format(month)
            weather_data = data_reading(
                cmd_args.dir, year_month[1], year_month[0])
            if weather_data:
                print("--------------Weather Report of " +
                      calendar.month_name[int(year_month[1])] + " " +
                      year_month[0] + "-----------------")
                weatherman.average_max_min_temp_mean_himidity(weather_data)
            else:
                print("Data not found")
    if cmd_args.month_eachday:
        for month in cmd_args.month_eachday:
            year_month = date_format(month)
            weather_data = data_reading(
                cmd_args.dir, year_month[1], year_month[0])
            if weather_data:
                print("--------------Weather Report of " +
                      calendar.month_name[int(year_month[1])] + " " +
                      year_month[0] + "-----------------")
                weatherman.each_day_bar(weather_data, 'c')
            else:
                print("Data not found")
    if cmd_args.month_eachday_bonus:
        for month in cmd_args.month_eachday_bonus:
            year_month = date_format(month)
            weather_data = data_reading(
                cmd_args.dir, year_month[1], year_month[0])
            if weather_data:
                print("--------------Weather Report of " +
                      calendar.month_name[int(year_month[1])] + " " +
                      year_month[0] + "-----------------")
                weatherman.each_day_bar(weather_data, 'cb')
            else:
                print("Data not found")


def arguments_parser():
    cla_parser = argparse.ArgumentParser()
    cla_parser.add_argument("dir", help="Data DIR path", type=str)
    cla_parser.add_argument("-e", "--year", help="For Year weather report",
                            nargs="*", type=str)
    cla_parser.add_argument("-a", "--month", help="For maonth weather report",
                            nargs="*", type=str)
    cla_parser.add_argument("-c", "--month_eachday", help="For eachday report",
                            nargs="*", type=str)
    cla_parser.add_argument("-cb", "--month_eachday_bonus",
                            help="For eachday report(bonus)", nargs="*",
                            type=str)
    return cla_parser.parse_args()


def validate_argumets():
    cmd_line_args = arguments_parser()
    if not os.path.exists(cmd_line_args.dir):
        print("Provide existing path of directory")
        exit(0)
    return cmd_line_args


def date_format(date):
    if not re.search(r'\d{4}/\d{0,2}', date):
        print("Enter the correct format of date")
        exit(0)
    return date.split("/")


if __name__ == "__main__":
    main()
