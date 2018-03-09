""" File for all constants
Pylint Score: 10.00
"""

from constants import MONTHS


def get_day(date):
    """Extracts the day from date"""
    first_dash = date.find('-')
    date = date[first_dash + 1:]
    second_dash = date.find('-')
    day = date[second_dash + 1:]
    if int(day) < 10:
        day = '0' + day
    return day


def get_month(date):
    """Extracts the month from date"""
    first_dash = date.find('-')
    date = date[first_dash + 1:]
    second_dash = date.find('-')
    month = MONTHS[int(date[:second_dash])]
    return month


def get_average(data, head_row, col, no):
    """Calculates averages"""
    total = 0
    for k in range(head_row + 1, len(data) - 1):
        if data[k][col] != '':
            total += int(data[k][col])
    avg = total // no
    return avg


def get_averages(data, head_row, max_temp_col, min_temp_col, mean_humid_col, total_no):
    """Calculates averages"""
    max_temp_sum = 0
    min_temp_sum = 0
    mean_humid_sum = 0

    # getting required data
    for k in range(head_row + 1, len(data) - 1):
        if data[k][max_temp_col] != '':
            max_temp_sum += int(data[k][max_temp_col])
        if data[k][min_temp_col] != '':
            min_temp_sum += int(data[k][min_temp_col])
        if data[k][mean_humid_col] != '':
            mean_humid_sum += int(data[k][mean_humid_col])

    avg_max_temp = max_temp_sum // total_no
    avg_min_temp = min_temp_sum // total_no
    avg_mean_humid = mean_humid_sum // total_no

    return [avg_max_temp, avg_min_temp, avg_mean_humid]


def locate(data):
    for row_no, row in enumerate(data):
        for col_no, item in enumerate(row):
            if item.find('Max TemperatureC') != -1:
                head_row = row_no
                max_temp_col = col_no
            if item.find('Min TemperatureC') != -1:
                min_temp_col = col_no
            if item.find('Max Humidity') != -1:
                max_humid_col = col_no
            if item.find('Mean Humidity') != -1:
                mean_humid_col = col_no
            if item.find('PKT') != -1 or item.find('PKST') != -1:
                time_col = col_no

    return [head_row, time_col, max_temp_col, min_temp_col, max_humid_col, mean_humid_col]
