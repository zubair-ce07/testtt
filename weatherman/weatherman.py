"""This script use to run the waetherman app
it tasks command line arguments to differntiate
that wether it prints the YEAR,MONTH and DAY report"""
import re
import calendar
from cla_parser import validate_argumets
from year_report import YearReport
from month_report import MonthReport
from eachday_report import EachDayReport
from constants import MONTHS,DATA_COL
from file_reading import file_reading



cla = validate_argumets()

if cla.yearly:
    year_report = YearReport()
    for month in MONTHS:
        FILE_READER = file_reading(cla.dir,month,cla.date_str)
        if FILE_READER:
            for line in FILE_READER:
                if len(line.strip()) == 16:
                    continue
                zipList = zip(DATA_COL, line.split(","))
                dictOfWeather = dict(zipList)
                year_report.set_accurate_date(dictOfWeather)
                dictOfWeather.clear()
    print(
    "----------Weather Report of " + cla.date_str +
    "-----------"
    )
    year_report.print_year_report()

elif cla.monthly:
    month_report = MonthReport()
    if not re.search(r'\d{4}/{0,1}\d{0,2}',cla.date_str):
        print("Enter the correct format of date")
        exit(0)
    YEAR_MONTH = cla.date_str.split("/")
    FILE_READER = file_reading(cla.dir,MONTHS[int(YEAR_MONTH[1])-1],YEAR_MONTH[0])
    if FILE_READER:
        for line in FILE_READER:
            if len(line.strip()) == 16:
                continue
            zipList = zip(DATA_COL, line.split(","))
            dictOfWeather = dict(zipList)
            month_report.cal_sum_of_data(dictOfWeather)
            dictOfWeather.clear()
        month_report.take_avg_of_data()
        print(
            "--------------Weather Report of " +
            calendar.month_name[int(YEAR_MONTH[1])] + " " +
            YEAR_MONTH[0] + "-----------------"
            )
        month_report.print_month_report()
    else:
        print("No data found")

elif cla.monthly_eachday:
    each_day_report = EachDayReport()
    if not re.search(r'\d{4}/{0,1}\d{0,2}',cla.date_str):
        print("Enter the correct format of date")
        exit(0)
    YEAR_MONTH = cla.date_str.split("/")
    FILE_READER = file_reading(cla.dir,MONTHS[int(YEAR_MONTH[1])-1],YEAR_MONTH[0])
    if FILE_READER:
        print(
            "--------------Weather Report of " +
            calendar.month_name[int(YEAR_MONTH[1])] + " " +
            YEAR_MONTH[0] + "-----------------"
        )
        for line in FILE_READER:
            if len(line.strip()) == 16:
                continue
            zipList = zip(DATA_COL, line.split(","))
            dictOfWeather = dict(zipList)
            each_day_report.print_eachday_report(dictOfWeather)
            each_day_report.print_eachday_report(dictOfWeather)
            dictOfWeather.clear()
    else:
        print("No data found")
    
elif cla.monthly_bonus:
    each_day_report = EachDayReport()
    if not re.search(r'\d{4}/{0,1}\d{0,2}',cla.date_str):
        print("Enter the correct format of date")
        exit(0)
    YEAR_MONTH = cla.date_str.split("/")
    FILE_READER = file_reading(cla.dir,MONTHS[int(YEAR_MONTH[1])-1],YEAR_MONTH[0])
    if FILE_READER:
        print(
            "--------------Weather Report of " +
            calendar.month_name[int(YEAR_MONTH[1])] + " " +
            YEAR_MONTH[0] + "-----------------"
        )
        for line in FILE_READER:
            if len(line.strip()) == 16:
                continue
            zipList = zip(DATA_COL, line.split(","))
            dictOfWeather = dict(zipList)
            each_day_report.print_eachday_report(dictOfWeather)
            each_day_report.print_eachday_report_bonus(dictOfWeather)
            dictOfWeather.clear()
    else:
        print("No data found")
