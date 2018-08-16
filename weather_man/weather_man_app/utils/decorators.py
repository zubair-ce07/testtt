# -*- coding: utf-8 -*-
"""
This file includes decorators which will help for pre-processing in weather-man-app.
"""
from functools import wraps


def prepare_input(input_function):
    wraps(input_function)

    def case_decorator(*args, **kwargs):
        """
        Validate period input from different command line arguments passed by user, cleansing of input is also done.
        :param args: args passed in input_function
        :param kwargs: kwargs passed in input_function
        """
        kwargs['period'] = globals()['prepare_{}_args'.format(kwargs.get('category'))](kwargs.get('period'))
        return input_function(*args, **kwargs)
    return case_decorator


def prepare_year_args(period):
    """
    Prepare parameter for year's result execution
    :param period: Period to be checked as a valid year
    :return: Prepared parameter.
    """
    return {
        'year': period,
        'month': ""
    }


def prepare_year_with_month_args(period):
    """
    Prepare parameter for month of an year's result execution
    :param period: Period from which year and month needs to be fetched
    :return: Prepared parameter.
    """
    year, month = period.split('/')
    return {
        'year': year,
        'month': month
    }


def prepare_month_bar_chart_args(period):
    """
    If a specific month on an year's results' bar chart, preparation will be same as
    validate_year_with_month_result_args
    :param period: Period from which year and month needs to be fetched
    :return: Result from validate_year_with_month_result_args.
    """
    return prepare_year_with_month_args(period)


def prepare_month_bar_chart_in_one_line_args(period):
    """
    If a specific month on an year's results' bar chart, preparation will be same as
    validate_year_with_month_result_args
    :param period: Period from which year and month needs to be fetched
    :return: Result from validate_year_with_month_result_args.
    """
    return prepare_year_with_month_args(period)
