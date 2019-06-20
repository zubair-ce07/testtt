import sys
import calendar

import calc
import terminalfunctions as tf
import reportgen as rg

from ds import YearReading
from ds import MonthReading
from ds import YearResults
from ds import MonthResults
from ds import ChartResults

arguments_list = list(sys.argv)
arguments = iter(sys.argv)

if (tf.validateArguments(arguments_list) == False):
    tf.printUsage()
    sys.exit(1)

next(arguments)
next(arguments)
report_count = int((len(arguments_list)/2) - 1)

for i in range(report_count):
    print()
    flag = str(next(arguments))
    value = str(next(arguments))
    if (flag == "-e"):
        year = YearReading(arguments_list[1], value)
        yresults = calc.yearlyCalc(year)
        rg.yearReport(yresults)
    else:
        ym_split = value.split('/')
        m = int(ym_split[1])
        month = calendar.month_abbr[m]
        file_path = str(arguments_list[1]) + "/Murree_weather_" + ym_split[0] + "_" + month + ".txt"
        month = MonthReading(file_path)
        if (flag == "-a"):
            mresults = calc.monthlyCalc(month)
            rg.monthReport(mresults)
        if (flag == "-c"):
            mcresults = calc.barChart(month)
            rg.chartReport(mcresults)
        if (flag == "-b"):
            mcbresults = calc.barChart(month)
            rg.chartBonusReport(mcbresults)
print()