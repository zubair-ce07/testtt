# -*- coding: utf-8 -*-
"""
This file includes decorators which will help for pre-processing in weather-man-app.
"""
from functools import wraps
import datetime

from app_factory.configs.app_configs import AppConfig


def validate_input(input_function):
    wraps(input_function)

    def case_decorator(*args, **kwargs):
        """
        Validate period input from different command line arguments passed by user, cleansing of input is also done.
        :param args: args passed in input_function
        :param kwargs: kwargs passed in input_function
        """
        validated_input = globals()['validate_{}_args'.format(kwargs.get('category'))](kwargs.get('period'))
        if not validated_input:
            return None
        kwargs['period'] = validated_input
        return input_function(*args, **kwargs)
    return case_decorator


def validate_year(period):
    """
    Validate year passed by the user and checks if this is a valid year or not.
    :param period: year
    :return: validation result: year if year is valid and None if year is invalide.
    """
    year = datetime.datetime.strptime(period, "%Y").date().strftime("%Y")
    current_year = datetime.datetime.today().year
    if int(year) <= current_year:
        return year
    return None


def validate_month(month):
    """
    Checks weather the month is valid or not.
    :param month: Month
    :return: validation result: month if month is valid and None if not.
    """
    if month in range(1, 13):
        return month
    return None


def validate_year_args(period):
    """
    If year results are required, this function validates the year argument and check there is no month in the
    argument and returns cleansed dictionary which can be used by calling function.
    :param period: Period to be checked as a valid year
    :return: Validation result.
    """
    try:
        if validate_year(period):
            return {
                'year': period,
                'month': ""
            }
    except:
        AppConfig.parser.error("Validate input please")


def validate_year_with_month_args(period):
    """
    If a specific month on an year's results are required, this function validates the year and month argument in the
    arguments and returns cleansed dictionary which can be used by calling function.
    :param period: Period to be checked as a valid year and month
    :return: Validation result.
    """
    try:
        year, month = period.split('/')
        if validate_year(year) and validate_month(int(month)):
            return {
                'year': year,
                'month': month
            }
    except:
        AppConfig.parser.error("Validate input please")


def validate_month_bar_chart_args(period):
    """
    If a specific month on an year's results' bar chart, validation will be same done in
    validate_year_with_month_result_args.
    :param period: Period to be checked as a valid year and month
    :return: Validation result from validate_year_with_month_result_args.
    """
    return validate_year_with_month_args(period)


def validate_month_bar_chart_in_one_line_args(period):
    """
    If a specific month on an year's results' bar chart in one line, validation will be same done in
    validate_year_with_month_result_args.
    :param period: Period to be checked as a valid year and month
    :return: Validation result from validate_year_with_month_result_args.
    """
    return validate_year_with_month_args(period)
