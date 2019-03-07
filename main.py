"""
This module prints annual weather data report.
It parses arguments in to required format and prints respective report.
"""

import argparse
import os

from weather_man import WeatherMan

def main():
    """
    Parses arguments in order to print weather data report.

    """
    report_message = 'Report number:\n1-Annual Max/Min Temperature 2-Hottest day of each year'
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('report_type', type=int, choices=[1, 2], help=report_message)
    arg_parser.add_argument('data_dir', type=is_dir, help='Directory containing weather data files')

    try:
        arguments = arg_parser.parse_args()
        print_report(arguments.report_type, arguments.data_dir)

    except argparse.ArgumentTypeError:
        arg_parser.print_help()

def is_dir(dir_name):
    """
    Validates if passed argument is not an empty directory,
    raises exception otherwise.

    Args:
        dir_name <str> : path of the directory

    Returns:
        dir_name (str): path of the directory

    Raises:
        ArgumentTypeError: if directory is empty or does not exist
    """

    if os.path.isdir(dir_name):
        if os.listdir(dir_name):
            return dir_name
        else:
            raise argparse.ArgumentTypeError('No files were found!')
    else:
        raise argparse.ArgumentTypeError('{0} is not a directory'.format(dir_name))

def print_report(report_type, data_dir):
    """
    Generated respective report against report_type and prints it.

    Args:
        report_type <int> : report type
        data_dir <str>: data directory path
    """

    weather_man = WeatherMan(data_dir)

    if report_type == 1:
        weather_man.print_annual_weather_report()
    else:
        weather_man.print_annual_max_temperature_weather_report()

if __name__ == '__main__':
    main()
