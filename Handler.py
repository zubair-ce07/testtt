import logging
import os
from ChartResult import ChartResult
from WeatherReading import WeatherReading
from MonthlyResult import MonthlyResult
from YearlyResult import YearlyResult
import csv


def read_file(path):
    """This function will receive a pth+filename and returns a list of weather obj of that file
    if the file isn't found, it will log a warning.
    """
    lst = list()
    try:
        with open(path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                reading = WeatherReading(
                    (row['PKST' if 'PKST' in row.keys() else 'PKT']),
                    int(0 if not row['Max TemperatureC'] else row['Max TemperatureC']),
                    int(0 if not row['Min TemperatureC'] else row['Min TemperatureC']),
                    int(0 if not row['Max Humidity'] else row['Max Humidity']),
                    int(0 if not row[' Mean Humidity'] else row[' Mean Humidity']))
                lst.append(reading)
    except IOError:
        logging.warning(path + ' Not found')
    return lst


def calculate_monthly_report(reading_list):
    """This function will receive a list of weather obj of a month and returns the DS for monthly report. """
    if not reading_list:
        return None
    highest_avg = 0
    lowest_avg = 0
    humidity_avg = 0
    for item in reading_list:
        highest_avg += item.highest
        lowest_avg += item.lowest
        humidity_avg += item.mean_humidity
    highest_avg /= len(reading_list)
    lowest_avg /= len(reading_list)
    humidity_avg /= len(reading_list)
    return MonthlyResult(highest_avg, lowest_avg, humidity_avg)


def calculate_yearly_report(reading_list):
    """This function will receive a list of weather obj of a year and returns the DS for Yearly report. """
    if not reading_list:
        return None
    highest = reading_list[0]
    lowest = reading_list[0]
    humidity = reading_list[0]

    for item in reading_list:
        if item.highest > highest.highest:
            highest = item
        if item.lowest < lowest.lowest:
            lowest = item
        if item.max_humidity > humidity.max_humidity:
            humidity = item
    return YearlyResult(highest, lowest, humidity)


def calculate_chart_report(reading_list):
    """This function will receive a list of weather obj of a month and returns the DS for Chart report. """
    if not reading_list:
        return None
    highest = reading_list[0]
    lowest = reading_list[0]
    for item in reading_list:
        if item.highest > highest.highest:
            highest = item
        if item.lowest < lowest.lowest:
            lowest = item
    return ChartResult(highest, lowest)


def validate_arg(arg):
    """ This function will receive sys.argv and checks if user has entered:
        Minimum  no of valid arg,
        correct path
        If either of the condition isn't satisfied, it will return false.
    """
    if len(arg) < 4:
        return False
    if not os.path.exists(arg[1]):
        return False
    return True
