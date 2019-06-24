import logging
import os

from ChartResult import ChartResult
from WeatherDS import WeatherDS
from MonthlyResult import MonthlyResult
from YearlyResult import YearlyResult
import csv


"""This function will receive a pth+filename and returns a list of weather obj of that file
    if the file isn't found, it will log a warning. """


def read_file(pth):
    lst = list()
    try:
        with open(pth) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_reader.__next__()  # Skip 1st row (Column Names)
            for row in csv_reader:
                # row[0] = Date, row[1] = highest, row[3] = Lowest, row[7] = max_humidity, row[8] = mean_humidity
                ds = WeatherDS((row[0]), int(0 if not row[1] else row[1]), int(0 if not row[3] else row[3]),
                               int(0 if not row[7] else row[7]), int(0 if not row[8] else row[8]))
                lst.append(ds)
    except IOError:
        logging.warning(pth + ' Not found')
    return lst


"""This function will receive a list of weather obj of a month and returns the DS for monthly report. """


def calculate_monthly_report(wlst):
    if wlst is None:
        return None
    highest_avg = 0
    lowest_avg = 0
    humidity_avg = 0
    for item in wlst:
        highest_avg += item.highest
        lowest_avg += item.lowest
        humidity_avg += item.mean_humidity
    highest_avg /= len(wlst)
    lowest_avg /= len(wlst)
    humidity_avg /= len(wlst)
    return MonthlyResult(highest_avg, lowest_avg, humidity_avg)


"""This function will receive a list of weather obj of a year and returns the DS for Yearly report. """


def calculate_yearly_report(wlst):
    highest = wlst[0]
    lowest = wlst[0]
    humidity = wlst[0]

    for item in wlst:
        if item.highest > highest.highest:
            highest = item
        if item.lowest < lowest.lowest:
            lowest = item
        if item.max_humidity > humidity.max_humidity:
            humidity = item
    return YearlyResult(highest, lowest, humidity)


"""This function will receive a list of weather obj of a month and returns the DS for Chart report. """


def calculate_chart_report(wlst):
    highest = wlst[0]
    lowest = wlst[0]
    for item in wlst:
        if item.highest > highest.highest:
            highest = item
        if item.lowest < lowest.lowest:
            lowest = item
    return ChartResult(highest, lowest)


""" This function will recieve sys.argv and checks if user has entered:
    Minimum  no of valid arg,
    correct path
    If either of the condition isn't satisfied, it will return false.
"""


def validate_arg(arg):
    if len(arg) < 4:
        return False
    if not os.path.exists(arg[1]):
        return False
    return True
