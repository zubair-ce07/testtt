"""This module provide the helping functions
"""
from datetime import datetime

def strip_list(lst):
    """strip list of strings, replace spaces with _ and convert it to lowercase
    """
    for index, _ in enumerate(lst):
        lst[index] = lst[index].strip()
        lst[index] = lst[index].replace(" ", "_")
        lst[index] = lst[index].lower()

def parse_date(date):
    """parse the given data and return the start and end date with read_type
    """
    end_date = None
    if "/" in date:
        year, month = date.split("/")
        start_date = datetime(int(year), int(month), 1)
        read_type = "Month"
    else:
        start_date = datetime(int(date), 1, 1)
        end_date = datetime(int(date) + 1, 1, 1)
        read_type = "Year"

    return [start_date, read_type, end_date]
