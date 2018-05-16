import argparse
import datetime
import os
import fnmatch
from parser import Parser
from calculations import Calculations
from report import Report

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', nargs=1, required=True,
                        help="Specify directory for files with this option")
    parser.add_argument('-e', nargs="*",
                        help="Provide year to show highest temperature, lowest temperature and maxmum humidity for that year")
    parser.add_argument('-a', nargs=1,
                        help="Provide any month in YYYY/MM format to view average of max, min temperature and humidity")
    parser.add_argument('-c', nargs=1,
                        help="Provide any month in YYYY/MM format to show two liner chart report for daily temperature")
    parser.add_argument('-cs', nargs=1,
                        help="Provide any month in YYYY/MM format to show one liner chart report for daily temperature")
    
    result = parser.parse_args()
    directory = result.d[0]

    if result.a:
        print(f"Report for {result.a[0]}")
        month = datetime.datetime.strptime(result.a[0], "%Y/%m").strftime("%Y_%b")
        files_to_parse = []
        file_readings = Parser.parse_files(directory, month)
        Report.show_monthly_report(file_readings)
        print()
    if result.e:
        print(f"Report for year {result.e[0]}")
        files_to_parse = []
        file_readings = Parser.parse_files(directory,result.e[0])
        Report.show_yearly_report(file_readings)
        print()
    if result.c:
        files_to_parse = []
        month = datetime.datetime.strptime(result.c[0], "%Y/%m").strftime("%Y_%b")
        file_readings = Parser.parse_files(directory, month)
        Report.show_chart_report(file_readings)
        print()
    if result.cs:
        files_to_parse = []
        month = datetime.datetime.strptime(result.cs[0], "%Y/%m").strftime("%Y_%b")
        file_readings = Parser.parse_files(directory, month)
        Report.show_one_liner_chart_report(file_readings)
        print()
