import os
import sys
import datetime
from parser import Parser
from calculations import Calculations
from report import Report


file_parser = Parser()
calculations_object = Calculations()
report_printer = Report()

def generate_yearwise_report(year):
    file_readings = file_parser.parse_files_for_yearwise_record(sys.argv[1], year)
    results = calculations_object.calulate_year_wise_record(file_readings)
    report_printer.show_report(results)

def generate_monthwise_report(month):
    file_readings = file_parser.parse_files_for_monthwise_records(sys.argv[1], month)
    results = calculations_object.calulate_average_record(file_readings)
    report_printer.show_report(results)

def generate_chart(month):
    file_readings = file_parser.parse_files_for_monthwise_records(sys.argv[1], month)
    report_printer.show_chart_report(file_readings)

def generate_one_liner_chart(month):
    file_readings = file_parser.parse_files_for_monthwise_records(sys.argv[1], month)
    report_printer.show_one_liner_chart_report(file_readings)

if (len(sys.argv) == 4):
    if (sys.argv[2] == "-e"):
        generate_yearwise_report(sys.argv[3])
    elif (sys.argv[2] == "-a"):
        month = datetime.datetime.strptime(sys.argv[3], "%Y/%m").strftime("%Y_%b")
        generate_monthwise_report(month)
    elif (sys.argv[2] == "-c"):
        month = datetime.datetime.strptime(sys.argv[3], "%Y/%m").strftime("%Y_%b")
        generate_chart(month)
    elif (sys.argv[2] == "-cs"):
        month = datetime.datetime.strptime(sys.argv[3], "%Y/%m").strftime("%Y_%b")
        generate_one_liner_chart(month)
    else:
        print(sys.argv[2] + " is not a valid option.")
elif (len(sys.argv) > 4):
    for i in range(2, len(sys.argv)):
        if (i % 2 == 0):
            if (sys.argv[i] == "-e"):
                generate_yearwise_report(sys.argv[i+1])
            elif (sys.argv[i] == "-a"):
                month = datetime.datetime.strptime(sys.argv[i+1], "%Y/%m").strftime("%Y_%b")
                generate_monthwise_report(month)
            elif (sys.argv[i] == "-c"):
                month = datetime.datetime.strptime(sys.argv[i+1], "%Y/%m").strftime("%Y_%b")
                generate_chart(month)
            elif (sys.argv[i] == "-cs"):
                month = datetime.datetime.strptime(sys.argv[i+1], "%Y/%m").strftime("%Y_%b")
                generate_one_liner_chart(month)
            else:
                print(sys.argv[i] + " is not a valid option.")
else:
    print("Invalid command")