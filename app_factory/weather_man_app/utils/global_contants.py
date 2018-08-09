# -*- coding: utf-8 -*-
"""
All global constants and helpers are written here to provide utility throughout the application.
"""


class AppsHelper(object):
    __app_helper_map = {
        'weather-man': 'Weather Man'
    }

    @staticmethod
    def get_app_name(name_for):
        return AppsHelper.__app_helper_map.get(name_for)


class FileGlobals(object):
    """
    File related global constants
    """
    __global_constants = {
        'FILE_PREFIX': 'Murree_weather',
        'FILE_EXTENTION': 'txt'
    }

    @staticmethod
    def get(item):
        return FileGlobals.__global_constants.get(item)


class ArgsParserCategories(object):
    """
    File related global constants
    """
    __args_parser_categories = [
        'year', 'year_with_month', 'month_bar_chart', 'month_bar_chart_in_one_line'
    ]

    @staticmethod
    def get_categories():
        for constant in ArgsParserCategories.__args_parser_categories:
            yield constant


class DateMapper(object):
    """
    Months mapper used to return numeric months to str prefix
    """
    __months_map = {
        1: 'Jan',
        2: 'Feb',
        3: 'Mar',
        4: 'Apr',
        5: 'May',
        6: 'Jun',
        7: 'Jul',
        8: 'Aug',
        9: 'Sep',
        10: 'Oct',
        11: 'Nov',
        12: 'Dec'
    }
    __months_map_full_name = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }

    @staticmethod
    def get_month_name(month):
        return "" if month is (None or "") else DateMapper.__months_map.get(MathHelper.parse_int(month))

    @staticmethod
    def get_month_full_name(month):
        year, month, day = month.split('-')
        month = DateMapper.__months_map_full_name.get(MathHelper.parse_int(month))
        return f"{month} {day}"


class MathHelper(object):
    """
    Mathematical constants and helpers are written here.
    """
    __helper_dict = {
        'neg-infinity': -99999,
        'pos-infinity': 99999
    }

    @staticmethod
    def get(item):
        return MathHelper.__helper_dict.get(item)

    @staticmethod
    def parse_int(number):
        return None if number is "" or number is None else int(number)


class ReportsHelper(object):
    """
    Reports helpers are written here like empty reports and output strings (all for different cantegories)
    """
    __reports_helper_map = {
        AppsHelper.get_app_name('weather-man'):
            {
                'years': {
                    'highest_temp': {
                        'value': MathHelper.get('neg-infinity'), 'day': None
                    },
                    'lowest_temp': {
                        'value': MathHelper.get('pos-infinity'), 'day': None
                    },
                    'highest_humidity': {
                        'value': MathHelper.get('neg-infinity'), 'day': None
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
        AppsHelper.get_app_name('weather-man'):
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
        return ReportsHelper.__reports_helper_map.get(AppsHelper.get_app_name(app_name)).get(category)

    @staticmethod
    def get_report_output(app_name, category):
        return ReportsHelper.__reports_output_strings.get(AppsHelper.get_app_name(app_name)).get(category)
