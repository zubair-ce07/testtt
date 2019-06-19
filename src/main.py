import sys
import calendar

import terminalfunctions as tf
import reportgen as rg
from yearreading import YearReading
from monthreading import MonthReading
from yearresults import YearResults
from monthresults import MonthResults
from chartresults import ChartResults

import calc

arguments_list = list(sys.argv)
arguments = iter(sys.argv)

print(arguments_list)
if (tf.validateArguments(arguments_list) == False):
    tf.printUsage()
    sys.exit(1)

next(arguments)
next(arguments)
print("Length of arg list:", len(arguments_list))
report_count = (len(arguments_list)/2) - 1
report_count = int(report_count)
print("Report count:", report_count)
for i in range(report_count):
    flag = str(next(arguments))
    value = str(next(arguments))
    if (flag == "-e"):
        year = YearReading(arguments_list[1], value)
        yresults = calc.yearlycalc(year)
        rg.yearreport(yresults)
    else:
        ym_split = value.split('/')
        m = int(ym_split[1])
        month = calendar.month_abbr[m]
        file_path = str(arguments_list[1]) + "/Murree_weather_" + ym_split[0] + "_" + month + ".txt"
        month = MonthReading(file_path)
        if (flag == "-a"):
            mresults = calc.monthlycalc(month)
            rg.monthreport(mresults)
        if (flag == "-c"):
            mcresults = calc.barchart(month)
            rg.chart(mcresults)
    