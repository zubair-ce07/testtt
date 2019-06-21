import datetime

from ds import YearResults, MonthResults, ChartResults

def year_report(yearresults):
    max_temp_date = datetime.datetime.strptime(yearresults.max_temp_date, "%Y-%m-%d")
    max_temp_month = max_temp_date.strftime("%B")
    max_temp_day = max_temp_date.strftime("%d")
    print("Highest:", end=" ")
    print(yearresults.max_temp, "C on", sep="", end=" ")
    print(max_temp_month, max_temp_day)

    min_temp_date = datetime.datetime.strptime(yearresults.min_temp_date, "%Y-%m-%d")
    min_temp_month = min_temp_date.strftime("%B")
    min_temp_day = min_temp_date.strftime("%d")
    print("Lowest:", end=" ")
    print(yearresults.min_temp, "C on", sep="", end=" ")
    print(min_temp_month, min_temp_day)

    max_humid_date = datetime.datetime.strptime(yearresults.max_humidity_date, "%Y-%m-%d")
    max_humid_month = max_humid_date.strftime("%B")
    max_humid_day = max_humid_date.strftime("%d")
    print("Humidity:", end=" ")
    print(yearresults.max_humidity, "% on", sep="", end=" ")
    print(max_humid_month, max_humid_day)

def month_report(monthresults):
    print("Highest Average: ", monthresults.avg_high_temp, "C", sep="")
    print("Lowest Average: ", monthresults.avg_low_temp, "C", sep="")
    print("Average Mean Humidity: ", monthresults.avg_mean_humidity, "%", sep="")
    

def chart_report(chartresults):
    print(chartresults.month, chartresults.year)
    for i, high_temp in enumerate(chartresults.high_temps):
        split_date = str(chartresults.high_dates[i]).split('-')
        date = split_date[2]
        print('\x1b[3;35m', date, '\x1b[0m', sep="", end = " ")
        for j in range(int(high_temp)):
            print('\x1b[0;31m', "+", '\x1b[0m', sep="", end="")
        print(" ", '\x1b[3;35m', high_temp, "C", '\x1b[0m', sep="")

        print('\x1b[3;35m', date, '\x1b[0m', sep="", end = " ")
        for j in range(int(chartresults.low_temps[i])):
           print('\x1b[0;34m', "+", '\x1b[0m', sep="", end="")
        print(" ", '\x1b[3;35m', chartresults.low_temps[i], "C", '\x1b[0m', sep="")

def chart_bonus_report(chartresults):
    print(chartresults.month, chartresults.year)
    for i, high_temp in enumerate(chartresults.high_temps):
        split_date = str(chartresults.high_dates[i]).split('-')
        date = split_date[2]
        print('\x1b[3;35m', date, '\x1b[0m', sep="", end = " ")
        for j in range(int(chartresults.low_temps[i])):
            print('\x1b[0;34m', "+", '\x1b[0m', sep="", end="")
        for j in range(int(high_temp)):
           print('\x1b[0;31m', "+", '\x1b[0m', sep="", end="")
        print(" ", '\x1b[3;35m', chartresults.low_temps[i], "C - ", high_temp, "C", '\x1b[0m', sep="")
