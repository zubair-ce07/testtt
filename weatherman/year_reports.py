""" contain all functions to display reports """
import csv
from classes import YearReport
from constants import CRED, CBLUE, CEND, FILE_MONTHS
from general_func import (get_month_data_in_year_list,
                          get_path_file)


def display_oneline_graph_of_month(max_temp, min_temp, cursor):
    """ display one line graph from of single month report
        for year graph"""
    print(str(cursor).zfill(2), end=" ")
    if max_temp != -1000 and min_temp != 1000:
        for _ in range(max_temp):
            print(CRED + "*" + CEND, end="")
        for _ in range(min_temp):
            print(CBLUE + "*" + CEND, end="")
        print(" ", str(max_temp)+"C",
              "-", str(min_temp) + "C")
    else:
        print("-")


def display_oneline_year_graph(year_record_list, year, path):
    """ display one line year graph """
    cursor = 1
    print("\n" + str(year), " Graph")
    for month in FILE_MONTHS:
        file_name = get_path_file(path, year, month)
        get_month_data_in_year_list(file_name, year_record_list, False)

        if year_record_list is not None and len(year_record_list) > 0:
            max_temp_entry = max(([y for y in year_record_list
                                   if y and y.temp.max_temp is not None]),
                                 key=lambda x: x.temp.max_temp)
            min_temp_entry = min(([y for y in year_record_list
                                  if y and y.temp.min_temp is not None]),
                                 key=lambda x: x.temp.min_temp)
            display_oneline_graph_of_month(max_temp_entry.temp.max_temp,
                                           min_temp_entry.temp.min_temp,
                                           cursor)
        else:
            display_oneline_graph_of_month(-1000, 1000, cursor)
        cursor = cursor + 1
        year_record_list = []
    print("")


def calculate_year_report_from_list(year_record_list):
    """ Form year report of max temp min temp and humidity"""
    max_temp_entry = max(([y for y in year_record_list
                           if y and y.temp.max_temp is not None]),
                         key=lambda x: x.temp.max_temp)
    min_temp_entry = min(([y for y in year_record_list
                           if y and  y.temp.min_temp is not None]),
                         key=lambda x: x.temp.min_temp)
    humidity_entry = max(([y for y in year_record_list
                           if y and y.humidity.max_humidity is not None]),
                         key=lambda x: x.humidity.max_humidity)

    year_report = YearReport(max_temp_entry.temp.max_temp, max_temp_entry.date,
                             min_temp_entry.temp.min_temp, min_temp_entry.date,
                             humidity_entry.humidity.max_humidity,
                             humidity_entry.date)
    return year_report


def display_year_report(path, year, graph):
    """ read line from given path and then display year report or
        year grap on the bases of graph flag """
    year_record_list = []
    if graph is False:
        for month in FILE_MONTHS:
            file_name = get_path_file(path, year, month)
            get_month_data_in_year_list(file_name, year_record_list, False)
        if year_record_list is not None and len(year_record_list) > 0:
            year_report = calculate_year_report_from_list(year_record_list)
            year_report.display()
        else:
            print("\n<< Data is not avialbe for given year." +
                  " [Required: year]\n")
    else:
        display_oneline_year_graph(year_record_list, year, path)
