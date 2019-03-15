# """Module to print reports"""

import weather_record
import argparse
import os


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-e', '--year', type=int,
                            help='Annual Max/Min temperatures. '
                                 'Input format: year')
    arg_parser.add_argument('-a', '--year_month', type=str,
                            help='Average Max/Min temperature & humidity of the month. '
                                 'Input format: year/month')
    arg_parser.add_argument('-c', '--year_month_chart', type=str,
                            help='Report to show bar chart of a month. Input format: year/month')
    arg_parser.add_argument('-b', '--year_month_bonus_chart', type=str,
                            help='Report to show Single bar chart of a month. Input format: year/month')
    arg_parser.add_argument('directory', type=is_dir, help='Files directory path')

    try:
        arguments = arg_parser.parse_args()
        print_report(arguments)
    except argparse.ArgumentTypeError:
        arg_parser.print_help()


def is_dir(dir_name):
    """
    Validates if passed argument is not an empty directory,
    raises exception otherwise.
    """
    if os.path.isdir(dir_name):
        if os.listdir(dir_name):
            return dir_name
        else:
            raise argparse.ArgumentTypeError('No files were found!')
    else:
        raise argparse.ArgumentTypeError('{0} is not a directory'.format(dir_name))


def print_report(arguments):
    w = weather_record.WeatherReport()
    w.parse_file_name(arguments)

    if arguments.year:
        w.calculate_annual_weather_report()
        w.print_annual_report()

    if arguments.year_month:
        w.print_monthly_average_report()


if __name__ == '__main__':
    main()

