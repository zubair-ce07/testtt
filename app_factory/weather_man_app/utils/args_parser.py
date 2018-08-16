# -*- coding: utf-8 -*-
"""
Parser for weathe man application
"""
import datetime

# from parser.args_parser import BaseArgsParser


def validate_year(year):
    """
    Validate year. *** If any exception comes calling parser will handle. ***
    :param year: year
    """
    year = datetime.datetime.strptime(year, "%Y").date().strftime("%Y")
    if int(year) >= datetime.datetime.now().year:
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


class ParserHelper:
    """
    Parser helper will provide utility in providing application specific arguments.
    """
    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            "file_path",
            help="Path to the directory containing weather data.",
        )
        parser.add_argument(
            "-e",
            "--year",
            help="Pass year as argument about which results are required. (Like: -e 2010)",
            type=validate_year
        )
        parser.add_argument(
            "-a",
            "--year_with_month",
            help="Pass year with month as argument about which results are required. (Like: -a 2010/1)",
            type=validate_year_and_month
        )
        parser.add_argument(
            "-c",
            "--month_bar_chart",
            help="input year and month for chart in format of year/month (Like -c 2014/8)",
            type=validate_year_and_month
        )
        parser.add_argument(
            "-m",
            "--month_bar_chart_in_one_line",
            help="input year and month for chart in format of year/month (Like -m 2014/8)",
            type=validate_year_and_month
        )
