"""
this module has all the utility functions of program
"""
import argparse
import calendar
import re
import glob
import os.path
from datetime import datetime


def create_arguments_parser():
    """
    this function creates the commandline arguments required
    for our program
    :return:
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-e", "--yearly",
                       help="For a given year display the highest "
                            "temperature and day, lowest temperature "
                            "and day, most humid day and humidity.",
                       action="store_true")
    group.add_argument("-a", "--monthly",
                       help="For a given month display the average"
                            " highest temperature, average lowest "
                            "temperature, average humidity.",
                       action="store_true")
    group.add_argument("-c", "--monthly_chart",
                       help="For a given month draw two horizontal "
                            "bar charts on the console for the highest "
                            "and lowest temperature on each day. Highest"
                            "in red and lowest in blue.",
                       action="store_true")
    # '-b' is for bar chart
    group.add_argument("-b", "--monthly_chart_one",
                       help="For a given month draw one horizontal "
                            "bar charts on the console for the highest "
                            "and lowest temperature on each day. Highest"
                            "in red and lowest in blue.",
                       action="store_true")
    parser.add_argument("date_string",
                        help="Date must be in the form 'YYYY' OR 'YYYY/MM'",
                        type=str)
    parser.add_argument("dir_path",
                        help="Path of Data Directory",
                        type=str)
    return parser.parse_args()


def validate_date_str(date_str, option):
    """
    this functon validates date string that we get from input
    :param date_str:
    :param option:
    :return:
    """
    # for comparing date string of the form 'YYYY' OR 'YYYY/MM'
    if option == 0:
        if bool(re.search("^\d{4}(([/])(0?[1-9]|1[012]))?$", date_str)) is False:
            return False
    # for comparing date string of the form 'YYYY/MM' only
    elif option == 1:
        if bool(re.search("^\d{4}([/])(0?[1-9]|1[012])$", date_str)) is False:
            return False
    return True


def get_formatted_date(date_str):
    """
    This function accepts a string and return a required formatted sate string
    """
    formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %d")
    return formatted_date


def get_month_name(month_num):
    """
    this function gets month number and return its name
    :param month_num:
    :return: month name
    """
    return calendar.month_name[month_num]


def get_month_abbr(month_num):
    """
        this function gets month number and return its abbreviation
        :param month_num:
        :return: month abrreviation
        """
    return calendar.month_abbr[month_num]


def get_file_path(dir_path, year, month):
    """
    this function use glob to find the files in a directory
    :param dir_path:
    :param year:
    :param month:
    :return: file names
    """
    return glob.glob(dir_path + "/*_" + year + "_" + month + "*")


def validate_path(dir_or_file_path):
    """
    this function checks wheter a path is vaid or not
    :param dir_or_file_path:
    :return: boolean
    """
    return os.path.exists(dir_or_file_path)
