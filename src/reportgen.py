import datetime

from ds import YearResults, MonthResults, ChartResults

def year_report(yearresults):
    print(yearresults.year)
    max_temp_date = datetime.datetime.strptime(yearresults.max_temp_date, "%Y-%m-%d")
    print("Highest:", end=" ")
    print(yearresults.max_temp, "C on", sep="", end=" ")
    print(f"{max_temp_date:%B} {max_temp_date:%d}")

    min_temp_date = datetime.datetime.strptime(yearresults.min_temp_date, "%Y-%m-%d")
    print("Lowest:", end=" ")
    print(yearresults.min_temp, "C on", sep="", end=" ")
    print(f"{min_temp_date:%B} {min_temp_date:%d}")

    max_humid_date = datetime.datetime.strptime(yearresults.max_humidity_date, "%Y-%m-%d")
    print("Humidity:", end=" ")
    print(yearresults.max_humidity, "% on", sep="", end=" ")
    print(f"{max_humid_date:%B} {max_humid_date:%d}")

def month_report(monthresults):
    print(monthresults.month, monthresults.year)
    print("Highest Average: ", monthresults.avg_high_temp, "C", sep="")
    print("Lowest Average: ", monthresults.avg_low_temp, "C", sep="")
    print("Average Mean Humidity: ", monthresults.avg_mean_humidity, "%", sep="")
    

def chart_report(chartresults):
    print(chartresults.month, chartresults.year)
    for day in chartresults.results:
        date = datetime.datetime.strptime(day[0], "%Y-%m-%d")
        
        print('\x1b[3;35m', date.strftime("%d"), '\x1b[0m', sep="", end = " ")
        for _ in range(day[1]):
            print('\x1b[0;31m', "+", '\x1b[0m', sep="", end="")
        print(" ", '\x1b[3;35m', day[1], "C", '\x1b[0m', sep="")

        print('\x1b[3;35m', date.strftime("%d"), '\x1b[0m', sep="", end = " ")
        for _ in range(day[2]):
            print('\x1b[0;34m', "+", '\x1b[0m', sep="", end="")
        print(" ", '\x1b[3;35m', day[2], "C", '\x1b[0m', sep="")

def chart_bonus_report(chartresults):
    print(chartresults.month, chartresults.year)
    for day in chartresults.results:
        date = datetime.datetime.strptime(day[0], "%Y-%m-%d")
        print('\x1b[3;35m', date.strftime("%d"), '\x1b[0m', sep="", end = " ")
        for _ in range(day[2]):
            print('\x1b[0;34m', "+", '\x1b[0m', sep="", end="")
        for _ in range(day[1]):
            print('\x1b[0;31m', "+", '\x1b[0m', sep="", end="")
        print(" ", '\x1b[3;35m', day[2], "C - ", day[1], "C", '\x1b[0m', sep="")
