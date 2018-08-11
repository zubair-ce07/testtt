# -*- coding: utf-8 -*-
"""
Parser for weathe man application
"""
import datetime

# from app_factory.parser.args_parser import BaseArgsParser


def validate_year(year):
    """
    Validate year. *** If any exception comes calling parser will handle. ***
    :param year: year
    """
    datetime.datetime.strptime(year, "%Y").date().strftime("%Y")
    return year


def validate_month(month):
    """
    Checks weather the month is valid or not.
    :param month: Month
    :return: validation result: month if month is valid and None if not.
    """
    if not int(month) in range(1, 13):
        raise ValueError
    return month


def validate_year_and_month(period):
    """
    Validate year and month input. *** If any exception comes calling parser will handle. ***
    :param period: year/month
    """
    year, month = period.split('/')
    if validate_year(year) and validate_month(month):
        return period


class ParserHelper:

    @staticmethod
    def add_arguments(parser):
        weather_man_parser = parser.add_parser(
            'weather-man',
            help='The program is design to generate Murree Weather Data reporting. (Use -h for help)'
        )
        weather_man_parser.add_argument(
            "file_path",
            help="Path to the directory containing weather data.",
        )
        weather_man_parser.add_argument(
            "-e",
            "--year",
            help="Pass year as argument about which results are required. (Like: -e 2010)",
            type=validate_year
        )
        weather_man_parser.add_argument(
            "-a",
            "--year_with_month",
            help="Pass year with month as argument about which results are required. (Like: -a 2010/1)",
            type=validate_year_and_month
        )
        weather_man_parser.add_argument(
            "-c",
            "--month_bar_chart",
            help="input year and month for chart in format of year/month (Like -c 2014/8)",
            type=validate_year_and_month
        )
        weather_man_parser.add_argument(
            "-m",
            "--month_bar_chart_in_one_line",
            help="input year and month for chart in format of year/month (Like -m 2014/8)",
            type=validate_year_and_month
        )
