# -*- coding: utf-8 -*-
"""
Parser for weathe man application
"""
import datetime
import argparse
import sys


def validate_year(year):
    """
    Validate year. *** If any exception comes calling parser will handle. ***
    :param year: year
    """
    year_test = datetime.datetime.strptime(year, "%Y").date().strftime("%Y")
    if int(year_test) >= datetime.datetime.now().year:
        raise ValueError
    return year


def validate_month(month):
    """
    Checks weather the month is valid or not.
    :param month: Month
    :return: validation result: month if month is valid and None if not.
    """
    datetime.date(1900, int(month), 1).strftime('%m')
    return month


def validate_year_and_month(period):
    """
    Validate year and month input. *** If any exception comes calling parser will handle. ***
    :param period: year/month
    """
    year, month = period.split('/')
    if validate_year(year) and validate_month(month):
        return period


class WeatherManArgsParser(argparse.ArgumentParser):
    """
    Application specific parsers will inherit from this base parser in which error handling and basic parsing is set.
    """
    def __init__(self, *args, **kwargs):
        super(WeatherManArgsParser, self).__init__(*args, **kwargs)
        self.add_arguments()

    def error(self, message):
        """
        When an error will occur in any app's args this function will print help for that specific parser.
        :param message: Error message
        """
        sys.stderr.write(f'Error: {message}\n')
        self.print_help()
        sys.exit(2)

    def add_arguments(self):
        self.add_argument(
            "file_path",
            help="Path to the directory containing weather data.",
        )
        self.add_argument(
            "-e",
            "--year",
            help="Pass year as argument about which results are required. (Like: -e 2010)",
            type=validate_year
        )
        self.add_argument(
            "-a",
            "--year_with_month",
            help="Pass year with month as argument about which results are required. (Like: -a 2010/1)",
            type=validate_year_and_month
        )
        self.add_argument(
            "-c",
            "--month_bar_chart",
            help="input year and month for chart in format of year/month (Like -c 2014/8)",
            type=validate_year_and_month
        )
        self.add_argument(
            "-m",
            "--month_bar_chart_in_one_line",
            help="input year and month for chart in format of year/month (Like -m 2014/8)",
            type=validate_year_and_month
        )
