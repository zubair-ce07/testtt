import argparse
import datetime
import os
import fnmatch
from parser import Parser
from calculations import Calculations
from report import Report

class MainClass:

    if __name__ == '__main__':
        file_parser = Parser()
        calculations_object = Calculations()
        report_printer = Report()

        parser = argparse.ArgumentParser()
        parser.add_argument('-d', nargs=1, required=True,
                            help="Specify directory for files with this option")
        parser.add_argument('-e', nargs="*",
                            help="Provide year to show highest temperature, lowest temperature and maxmum humidity for that year")
        parser.add_argument('-a', nargs="*",
                            help="Provide any month in YYYY/MM format to view average of max, min temperature and humidity")
        parser.add_argument('-c', nargs="*",
                            help="Provide any month in YYYY/MM format to show two liner chart report for daily temperature")
        parser.add_argument('-cs', nargs="*",
                            help="Provide any month in YYYY/MM format to show one liner chart report for daily temperature")
        
        result = parser.parse_args()
        directory = result.d[0]

        if result.a:
            for month in result.a:
                print(f"Report for {month}")
                month = datetime.datetime.strptime(month, "%Y/%m").strftime("%Y_%b")
                files_to_parse = []
                for file in os.listdir(directory):
                    if fnmatch.fnmatch(file, '*'+month+'*'):
                        files_to_parse.append(file)
                file_readings = file_parser.parse_files(directory, files_to_parse)
                results = calculations_object.calulate_average_record(file_readings)
                report_printer.show_monthly_report(results)
                print()
        if result.e:
            for year in result.e:
                print(f"Report for year {year}")
                files_to_parse = []
                for file in os.listdir(directory):
                    if fnmatch.fnmatch(file, '*'+year+'*'):
                        files_to_parse.append(file)
                file_readings = file_parser.parse_files(directory,files_to_parse)
                results = calculations_object.calulate_year_wise_record(file_readings)
                report_printer.show_yearly_report(results)
                print()
        if result.c:
            for month in result.c:
                files_to_parse = []
                month = datetime.datetime.strptime(month, "%Y/%m").strftime("%Y_%b")
                for file in os.listdir(directory):
                    if fnmatch.fnmatch(file, '*'+month+'*'):
                        files_to_parse.append(file)
                file_readings = file_parser.parse_files(directory, files_to_parse)
                report_printer.show_chart_report(file_readings)
                print()
        if result.cs:
            for month in result.cs:
                files_to_parse = []
                month = datetime.datetime.strptime(month, "%Y/%m").strftime("%Y_%b")
                for file in os.listdir(directory):
                    if fnmatch.fnmatch(file, '*'+month+'*'):
                        files_to_parse.append(file)
                file_readings = file_parser.parse_files(directory, files_to_parse)
                report_printer.show_one_liner_chart_report(file_readings)
                print()