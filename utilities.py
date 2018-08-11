import argparse
import calendar
import re
from datetime import datetime


def create_arguments_parser():
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
    parser.add_argument("file_path",
                        help="Path of Data Directory",
                        type=str)
    return parser.parse_args()

def validate_date_str(date_str, option):
    #for comparing date string of the form 'YYYY' OR 'YYYY/MM'
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
    return calendar.month_name[month_num]

def get_month_abbr(month_num):
    return calendar.month_abbr[month_num]
