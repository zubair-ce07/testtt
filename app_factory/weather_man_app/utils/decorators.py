# -*- coding: utf-8 -*-
"""
This file includes decorators which will help for pre-processing in weather-man-app.
"""
from functools import wraps
import datetime

from app_factory.configs.app_configs import AppConfigs


def validate_input(fn):
    wraps(fn)

    def case_decorator(*args, **kwargs):
        validated_input = globals()['validate_{}_args'.format(fn.__name__)](kwargs.get('period'))
        if not validated_input:
            return None
        kwargs['period'] = validated_input
        return fn(*args, **kwargs)
    return case_decorator


def validate_year(period):
    year = datetime.datetime.strptime(period, "%Y").date().strftime("%Y")
    current_year = datetime.datetime.today().year
    if int(year) <= current_year:
        return year
    return None


def validate_month(month):
    if 0 < int(month) < 13:
        return month
    return None


def validate_year_result_args(period):
    try:
        if validate_year(period):
            return {
                'year': period,
                'month': ""
            }
    except:
        AppConfigs.parser.error("Validate input please")


def validate_year_with_month_result_args(period):
    try:
        year, month = period.split('/')
        if validate_year(year) and validate_month(month):
            return {
                'year': year,
                'month': month
            }
    except:
        AppConfigs.parser.error("Validate input please")


def validate_month_bar_chart_result_args(period):
    return validate_year_with_month_result_args(period)


def validate_month_bar_chart_in_one_line_result_args(period):
    return validate_year_with_month_result_args(period)
