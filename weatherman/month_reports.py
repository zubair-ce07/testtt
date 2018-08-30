""" contain all functions to display reports """
from statistics import mean

from datetime import datetime
import csv
from classes import MonthAvgReport
from constants import CRED, CBLUE, CEND
from general_func import (read_single_line_record,
                          get_month_data_in_year_list,
                          get_path_file)


def month_display_graph_file(filename, rec_list):
    """ read line from given file and display graph report of month """
    try:
        with open(filename, mode='r') as reader:
            csv_reader = csv.DictReader(reader, delimiter=',')
            for row in csv_reader:
                day_record = read_single_line_record(row)
                if day_record is not None:
                    print((day_record.date).strftime('%d'), end=" ")
                    if day_record.temp.max_temp:
                        for _ in range(day_record.temp.max_temp):
                            print(CRED+"+"+CEND, end="")
                        print(" "+CRED+str(day_record.temp.max_temp)+"C"+CEND)
                    print((day_record.date).strftime('%d'), end=" ")
                    if day_record.temp.min_temp:
                        for _ in range(day_record.temp.min_temp):
                            print(CBLUE+"+"+CEND, end="")
                        print(" "+CBLUE+str(day_record.temp.min_temp)+"C"+CEND)
                    rec_list.append(day_record)
            print("")
    except IOError as err:
        print(f"\n<< I/O error({err.errno}: {err.strerror})")


def calculate_month_avg_file(filename, rec_list, month_str):
    """ calculate and return month average report """
    get_month_data_in_year_list(filename, rec_list, True)
    if rec_list is not None and len(rec_list) > 0:
        max_temp_data = [y.temp.max_temp for y in rec_list
                         if y.temp.max_temp is not None]
        max_temp_avg = mean(max_temp_data)

        min_temp_data = [y.temp.min_temp for y in rec_list
                         if y.temp.min_temp is not None]
        min_temp_avg = mean(min_temp_data)

        humidity_avg_data = [y.humidity.mean_humidity for y in rec_list
                             if y.humidity.mean_humidity is not None]
        humidity_avg = mean(humidity_avg_data)
        avg_report = MonthAvgReport(max_temp_avg, min_temp_avg,
                                    humidity_avg, month_str)
        if avg_report is not None:
            avg_report.display()


def display_month_report(path, year_month, graph):
    """ handle 2 modules of month (display graph, month report) with graph
        flag """
    try:
        [year, month] = year_month.split('/')
        month = int(month)
        month = month - 1
        if month > -1 and month < 12:
            month_str = (datetime.strptime(str(month+1),'%m')).strftime('%b')
            file_name = get_path_file(path, year, month_str)
            month_record_list = []
            if graph is False:
                month_str = datetime.strptime(year_month,
                                              "%Y/%m").strftime('%B %Y')

                calculate_month_avg_file(file_name,
                                         month_record_list,
                                         month_str)
            else:
                print("")
                print(datetime.strptime(year_month,
                                        "%Y/%m").strftime('%B %Y'))
                month_display_graph_file(file_name, month_record_list)
        else:
            print("\n<< Invalid input: month value is not in range\n")

    except ValueError:
        print("\n<< Invalid month or year [required: year/month]\n")
