import argparse
import os
from datetime import datetime

import task1
import task2
import task3
import utils


def valid_date(input_arg, date_format):
    try:
        date = datetime.strptime(input_arg, date_format)
        return date
    except ValueError:
        exception_msg = "Invalid input format, please try again"
        raise argparse.ArgumentTypeError(exception_msg)


def parse_month_input(input_arg):
    date = valid_date(input_arg, "%Y/%m")
    file_name = utils.get_file_name(date)
    if file_name:
        return file_name, date
    print("No data is available for " + input_arg)


def parse_year_input(input_arg):
    date = valid_date(input_arg, "%Y")
    year_files = utils.get_year_files(date.year)
    if len(year_files):
        return year_files
    print("No data is available for " + input_arg)


def check_folder(input_arg):

    if os.path.isdir(input_arg):
        utils.WEATHER_FILES_PATH = input_arg
    else:
        exception_msg = "No folder exists at path : " + input_arg
        raise argparse.ArgumentTypeError(exception_msg)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Description of program')
    parser.add_argument('path',
                        help='path to weather files folder',
                        type=check_folder)
    parser.add_argument('-e', '--task1',
                        help='use for task 1',
                        type=parse_year_input)
    parser.add_argument('-a', '--task2',
                        help='use for task 2',
                        type=parse_month_input)
    parser.add_argument('-c', '--task3',
                        help='use for task 3',
                        type=parse_month_input)

    args = parser.parse_args()

    if args.task1:
        task1.execute_task1(args.task1)
    if args.task2:
        task2.execute_task2(args.task2[0])
    if args.task3:
        task3.execute_task3(args.task3[0], args.task3[1])
