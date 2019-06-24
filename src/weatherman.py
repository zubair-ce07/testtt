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
            year = YearReading(arguments_list[1], value)
            if year.check != -1:
                year_results = calc.yearly_calc(year)
                rg.year_report(year_results)
            else:
                print("Invalid path")
                tf.print_usage
        else:
            split_date = value.split('/')
            month_num = int(split_date[1])
            month_name = calendar.month_abbr[month_num]
            file_path = f"{str(arguments_list[1])}/Murree_weather_{split_date[0]}_{month_name}.txt"
            month = MonthReading(file_path)
            if month.check != -1:
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
                print("Invalid path")
                tf.print_usage
    print()
else:
    tf.print_usage()
