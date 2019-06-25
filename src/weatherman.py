import os
import sys
import calendar

import calc
import terminalfunctions as tf
import reportgen as rg

from ds import YearReading, MonthReading, YearResults, MonthResults, ChartResults

arguments_list = list(sys.argv)
arguments = iter(sys.argv)

if tf.validate_arguments(arguments_list) == True:
    next(arguments)
    next(arguments)
    report_count = int((len(arguments_list)/2) - 1)

    for i in range(report_count):
        print()
        flag = str(next(arguments))
        value = str(next(arguments))
        if flag == "-e":
            if value.isdigit():
                if not int(value) < 2004 and not int(value) > 2016:
                    year = YearReading(arguments_list[1], value)
                    year_results = calc.yearly_calc(year)
                    rg.year_report(year_results)
                else:
                    print(f"Data for the year {value} does not exist")
            else:
                print(f"Invalid value of year: {value}")
        else:
            split_date = value.split('/')
            month_num = int(split_date[1])
            if not month_num < 1 and not month_num > 12:
                month_name = calendar.month_abbr[month_num]
                file_path = f"{str(arguments_list[1])}/Murree_weather_{split_date[0]}_{month_name}.txt"
                if os.path.exists(file_path):
                    month = MonthReading(file_path, split_date[0])
                    if flag == "-a":
                        month_results = calc.monthly_calc(month)
                        rg.month_report(month_results)
                    if flag == "-c":
                        chart_results = calc.bar_chart(month)
                        rg.chart_report(chart_results)
                    if flag == "-b":
                        bonus_results = calc.bar_chart(month)
                        rg.chart_bonus_report(bonus_results)
                else:
                    print(f"Data for {month_name} {split_date[0]} does not exist")
            else:
                print(f"Invalid value of month: {month_num}")
    print()
else:
    tf.print_usage()
