import datetime

from ds import YearResults
from ds import MonthResults
from ds import ChartResults

def yearReport(yearresults):
    max_t_date_split = str(yearresults.max_temp_date).split('-')
    max_t_date_formatted = datetime.datetime(int(max_t_date_split[0]), int(max_t_date_split[1]), int(max_t_date_split[2]))
    max_t_month = max_t_date_formatted.strftime("%B")
    max_t_day = max_t_date_formatted.strftime("%d")
    print("Highest:", end=" ")
    print(yearresults.max_temp, "C on", sep="", end=" ")
    print(max_t_month, max_t_day)

    min_t_date_split = str(yearresults.min_temp_date).split('-')
    min_t_date_formatted = datetime.datetime(int(min_t_date_split[0]), int(min_t_date_split[1]), int(min_t_date_split[2]))
    min_t_month = min_t_date_formatted.strftime("%B")
    min_t_day = min_t_date_formatted.strftime("%d")
    print("Lowest:", end=" ")
    print(yearresults.min_temp, "C on", sep="", end=" ")
    print(min_t_month, min_t_day)

    max_h_date_split = str(yearresults.max_humidity_date).split('-')
    max_h_date_formatted = datetime.datetime(int(max_h_date_split[0]), int(max_h_date_split[1]), int(max_h_date_split[2]))
    max_h_month = max_h_date_formatted.strftime("%B")
    max_h_day = max_h_date_formatted.strftime("%d")
    print("Humidity:", end=" ")
    print(yearresults.max_humidity, "% on", sep="", end=" ")
    print(max_h_month, max_h_day)

def monthReport(monthresults):
    print("Highest Average: ", monthresults.avg_high_temp, "C", sep="")
    print("Lowest Average: ", monthresults.avg_low_temp, "C", sep="")
    print("Average Mean Humidity: ", monthresults.avg_mean_humidity, "%", sep="")
    

def chartReport(chartresults):
    print(chartresults.month, chartresults.year)
    for i in range(len(chartresults.high_temps)):
        split_date = str(chartresults.high_dates[i]).split('-')
        date = split_date[2]
        print('\x1b[3;35m', date, '\x1b[0m', sep="", end = " ")
        for j in range(int(chartresults.high_temps[i])):
            print('\x1b[0;31m', "+", '\x1b[0m', sep="", end="")
        print(" ", '\x1b[3;35m', chartresults.high_temps[i], "C", '\x1b[0m', sep="")

        print('\x1b[3;35m', date, '\x1b[0m', sep="", end = " ")
        for j in range(int(chartresults.low_temps[i])):
           print('\x1b[0;34m', "+", '\x1b[0m', sep="", end="")
        print(" ", '\x1b[3;35m', chartresults.low_temps[i], "C", '\x1b[0m', sep="")

def chartBonusReport(chartresults):
    print(chartresults.month, chartresults.year)
    for i in range(len(chartresults.high_temps)):
        split_date = str(chartresults.high_dates[i]).split('-')
        date = split_date[2]
        print('\x1b[3;35m', date, '\x1b[0m', sep="", end = " ")
        for j in range(int(chartresults.low_temps[i])):
            print('\x1b[0;34m', "+", '\x1b[0m', sep="", end="")
        for j in range(int(chartresults.high_temps[i])):
           print('\x1b[0;31m', "+", '\x1b[0m', sep="", end="")
        print(" ", '\x1b[3;35m', chartresults.low_temps[i], "C - ", chartresults.high_temps[i], "C", '\x1b[0m', sep="")
                