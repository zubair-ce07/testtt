"""
File for all helper functions
Pylint Score: 10.00
"""

import os
import calendar


def get_dates(dates):
    """Extracts month and day from date"""
    month_day = []
    for date in dates:
        month, day = get_date(date)
        month_day.append('{} {}'.format(month, day))
    return ', '.join(n for n in month_day)


def get_date(date):
    """Extracts month and day from date"""
    month_no = date.split('-')[1]
    day = date.split('-')[2]
    month = calendar.month_name[int(month_no)]
    if int(day) < 10:
        day = '0{}'.format(day)
    return month, day


def get_file(args):
    """Function to find the required file"""
    files = []
    if args.year_month:
        year, month_no = args.year_month.split('/')
    elif args.year_month_graph:
        year, month_no = args.year_month_graph.split('/')
    mon = 'NULL'
    if 0 < int(month_no) <= 12:
        month = calendar.month_name[int(month_no)]
        print(month, year)
        mon = '{:.3}'.format(month)
    for file in os.listdir(args.directory):
        if file.find('{}_{}'.format(year, mon)) != -1:
            files.append(file)
    return files


def get_files(args):
    """Function to find the required files"""
    files = []
    for file in os.listdir(args.directory):
        if file.find(args.year) != -1:
            files.append(file)
    return files
