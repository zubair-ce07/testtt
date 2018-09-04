""" contain functions to display graph and report """

from datetime import datetime
import csv
from statistics import mean
from constants import CRED, CBLUE, CEND


def get_max_temp_entry(record_list):
    """ return element from list contating maximum temperature """
    return max(([y for y in record_list
                 if y and y.get("Max TemperatureC") is not None]),
               key=lambda x: int(x.get("Max TemperatureC")))


def get_min_temp_entry(record_list):
    """ return element from list contating minimum temperature """
    return min(([y for y in record_list
                 if y and y.get("Min TemperatureC") is not None]),
               key=lambda x: int(x.get("Min TemperatureC")))


def get_humidity_entry(record_list):
    """ return element from list contating max humidity """
    return max(([y for y in record_list
                 if y and y.get("Max Humidity") is not None]),
               key=lambda x: int(x.get("Max Humidity")))


def display_bar(range_str, sign, code):
    """helping function for graph """
    for _ in range(int(range_str)):
        print(code + sign + CEND, end="")


def display_extremes(rec_list, year_flag):
    """display report of year and month """
    if len(rec_list) > 0:
        if year_flag:
            max_temp_entry = get_max_temp_entry(rec_list)
            min_temp_entry = get_min_temp_entry(rec_list)
            humidity_entry = get_humidity_entry(rec_list)

            date = datetime.strptime(max_temp_entry.get("PKT"), '%Y-%m-%d')
            highest_temp_date = (date).strftime('%B %d')

            date = datetime.strptime(min_temp_entry.get("PKT"), '%Y-%m-%d')
            lowest_temp_date = (date).strftime('%B %d')

            date = datetime.strptime(humidity_entry.get("PKT"), '%Y-%m-%d')
            humidity_date = (date).strftime('%B %d')

            max_temperature = max_temp_entry.get("Max TemperatureC")
            min_temperature = min_temp_entry.get("Min TemperatureC")
            humidity = humidity_entry.get("Max Humidity")

            print(f"{year}:")
            print(f"Highest: {max_temperature}C on {highest_temp_date}")
            print(f"Lowest: {min_temperature}C on {lowest_temp_date}")
            print(f"Humidity: {humidity}% on {humidity_date}")

        else:
            max_temp_data = [int(y.get("Max TemperatureC")) for y in rec_list
                             if y.get("Max TemperatureC") is not None]
            max_temp_avg = mean(max_temp_data)

            min_temp_data = [int(y.get("Min TemperatureC")) for y in rec_list
                             if y.get("Min TemperatureC") is not None]
            min_temp_avg = mean(min_temp_data)

            humidity_avg_data = [int(y.get(" Mean Humidity")) for y in rec_list
                                 if y.get(" Mean Humidity") is not None]
            humidity_avg = mean(humidity_avg_data)

            print(f"Highest Average: {str(round(max_temp_avg, 2))}C")
            print(f"Lowest Average: {str(round(min_temp_avg, 2))}C")
            print(f"Average Mean Humidity: {str(round(humidity_avg , 2))}%")


def generate_graph(year, month, file_handler):
    """display graph of year and month"""
    if not month:
        print(f"{year}:")
        for cursor in range(12):
            cursor = cursor+1
            month_file = file_handler.get_file_names(year, str(cursor))
            month_list = file_handler.get_list(month_file)
            print(str(cursor).zfill(2), end=" ")
            if len(month_list) > 0:
                max_temperature = get_max_temp_entry(
                    month_list).get("Max TemperatureC")
                min_temperature = get_min_temp_entry(
                    month_list).get("Min TemperatureC")

                if max_temperature and min_temperature:
                    display_bar(max_temperature, "*", CRED)
                    display_bar(min_temperature, "*", CBLUE)
                    print(f" {max_temperature}C - {min_temperature}C")
                else:
                    print(" - ")
    else:
        month_str = datetime.strptime(month, "%m").strftime('%B')
        print(f"{year} {month_str}:")
        month_file = file_handler.get_file_names(year, month)
        month_list = file_handler.get_list(month_file)
        for day in month_list:
            date = datetime.strptime(day.get("PKT"), '%Y-%m-%d').strftime('%d')
            print(date, end=" ")
            max_temperature = day.get("Max TemperatureC")
            if max_temperature:
                display_bar(max_temperature, "+", CRED)
                print(" " + CRED + str(max_temperature) + "C" + CEND)
            print(date, end=" ")
            min_temperature = day.get("Min TemperatureC")
            if min_temperature:
                display_bar(min_temperature, "+", CBLUE)
                print(" " + CBLUE + str(min_temperature) + "C" + CEND)
