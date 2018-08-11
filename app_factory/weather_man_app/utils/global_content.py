# -*- coding: utf-8 -*-
"""
All global constants and helpers are written here to provide utility throughout the application.
"""
import datetime


class AppHelper:
    """
    Application related helpers are written eg application's display name.
    """
    __app_helper_map = {
        'weather-man': 'Weather Man'
    }

    @staticmethod
    def get_app_name(name_for):
        """
        Static method to return application display name given it's key.
        :param name_for: key to be searched
        :return: value present in application helper for a specifc key (if any)
        """
        return AppHelper.__app_helper_map.get(name_for)


class FileGlobalHandler:
    """
    File related global constants
    """
    __global_constants = {
        'FILE_PREFIX': 'Murree_weather',
        'FILE_EXTENTION': 'txt'
    }

    @staticmethod
    def get_file_constant(item):
        """
        Provides file related constants.
        :param item: key to be found eg: FILE_PREFIX
        :return: constant value for a specific key eg: txt for FILE_EXTENTION
        """
        return FileGlobalHandler.__global_constants.get(item)


class ArgsParserCategoryHandler:
    """
    File related global constants
    """
    __args_parser_categories = [
        'year', 'year_with_month', 'month_bar_chart', 'month_bar_chart_in_one_line'
    ]

    @staticmethod
    def get_categories():
        """
        Yield constants which are used throughout the application and are options in args parser for weather data.
        :rtype: str
        """
        for constant in ArgsParserCategoryHandler.__args_parser_categories:
            yield constant


class DateMapper:
    """
    Class to provide methods to help regarding date and month.
    """
    @staticmethod
    def get_month_name(month):
        """
        Get month name given a number
        :param month: Month number eg: 1 is for Jan
        :return:
        """
        return ("" if month is (None or "") else
                datetime.date(1900, MathHelper.parse_int(month), 1).strftime('%b'))

    @staticmethod
    def get_month_full_name_and_day(period):
        """
        Gives month's full name and year given date
        :param period: date eg: 2010-1-12 Year-Month-day
        :return: Month Day
        """
        year, month, day = period.split('-')
        month = datetime.date(1900, MathHelper.parse_int(month), 1).strftime('%B')
        return f"{month} {day}"


class MathHelper:
    """
    Mathematical constants and helpers are written here.
    """
    __helper_dict = {
        'neg-infinity': -99999,
        'pos-infinity': 99999
    }

    @staticmethod
    def get_constant_value(help_key):
        """
        Provide constant values for a mathematical terms, one thing needs to be keep in mind, these constants are
        constants throughout the application otherwise there is not value for neg-infinity or pos-infinity these can
        also be set according to the register size of a system to provide how much big number an architecture can hold,
        similarly other constants like log(10) value will always be constant throughout different architectures as well.
        :param help_key: What is wanted from math helper class.
        :return: Value for a specific key.
        """
        return MathHelper.__helper_dict.get(help_key)

    @staticmethod
    def parse_int(number):
        """
        Checks a value that can not be converted into integer and returns None otherwise convert value to number and
        :returns
        :param number: Candidate to be check as a possible integer.
        :return: None or int number
        """
        return None if number is "" or number is None else int(number)


class ReportsHelper:
    """
    Reports helpers are written here like empty reports and output strings (all for different cantegories)
    """
    __reports_helper_map = {
        AppHelper.get_app_name('weather-man'):
            {
                'years': {
                    'highest_temp': {
                        'value': MathHelper.get_constant_value('neg-infinity'), 'day': None
                    },
                    'lowest_temp': {
                        'value': MathHelper.get_constant_value('pos-infinity'), 'day': None
                    },
                    'highest_humidity': {
                        'value': MathHelper.get_constant_value('neg-infinity'), 'day': None
                    }
                },
                'year_with_month': {
                    'average_highest_temp': {
                        'value': 0, 'total-entries': 0
                    },
                    'average_lowest_temp': {
                        'value': 0, 'total-entries': 0
                    },
                    'average_mean_humidity': {
                        'value': 0, 'day': None, 'total-entries': 0
                    }
                },
                'month_bar_chart': {}
            }
    }
    __reports_output_strings = {
        AppHelper.get_app_name('weather-man'):
            {
                'years': {
                    'highest_temp': "Highest: {}C on {}",
                    'lowest_temp': "Lowest: {}C on {}",
                    'highest_humidity': "Humidity: {}% on {}"
                },
                'year_with_month': {
                    'average_highest_temp': "Highest Average: {:.2f}C",
                    'average_lowest_temp': "Lowest Average: {:.2f}C",
                    'average_mean_humidity': "Average mean Humidity: {:.2f}%"
                },
                'month_bar_chart': {

                }
            }
    }
    
    @staticmethod
    def get_empty_report(app_name, category):
        """
        Returns empty report of a specific category for weather man
        :param app_name: application name eg weather-man
        :param category: category of report eg: year report
        :return: empty report dictionary
        """
        return ReportsHelper.__reports_helper_map.get(AppHelper.get_app_name(app_name)).get(category)

    @staticmethod
    def get_report_output(app_name, category):
        """
        Give output strings that are required to format to make informative after calling.
        :param app_name: application name eg weather-man
        :param category: category of report eg: year report
        :return: dict with keys as sub-categories of report and specific output strings in respective sub-categories.
        """
        return ReportsHelper.__reports_output_strings.get(AppHelper.get_app_name(app_name)).get(category)
