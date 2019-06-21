import sys
import calendar

import calc
import terminalfunctions as tf
import reportgen as rg

from ds import YearReading, MonthReading, YearResults, MonthResults, ChartResults

arguments_list = list(sys.argv)
arguments = iter(sys.argv)

if tf.validateArguments(arguments_list) == False:
    tf.printUsage()
    sys.exit(1)

next(arguments)
next(arguments)
report_count = int((len(arguments_list)/2) - 1)

for i in range(report_count):
    print()
    flag = str(next(arguments))
    value = str(next(arguments))
    if flag == "-e":
        year = YearReading(arguments_list[1], value)
        yresults = calc.yearly_calc(year)
        rg.year_report(yresults)
    else:
        ym_split = value.split('/')
        m = int(ym_split[1])
        month = calendar.month_abbr[m]
        file_path = f"{str(arguments_list[1])}/Murree_weather_{ym_split[0]}_{month}.txt"
        month = MonthReading(file_path)
        if flag == "-a":
            mresults = calc.monthly_calc(month)
            rg.month_report(mresults)
        if flag == "-c":
            mcresults = calc.bar_chart(month)
            rg.chart_report(mcresults)
        if flag == "-b":
            mcbresults = calc.bar_chart(month)
            rg.chart_bonus_report(mcbresults)
print()
