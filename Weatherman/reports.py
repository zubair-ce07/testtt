#!/usr/bin/python3
import calendar
import colorama
from colorama import Fore
from colorama import Style

from data_holder import *


class WeathermanReportPrinter:
    'Class to print reports'

    def print_yearly_report(self, result):

        if (result):
            if (result.max_temprature):
                print("Highest:", end = " ")
                print(str(result.max_temprature.max_temprature) + "C on", end = " ")
                print(result.max_temprature.date.strftime("%B %d"))

            if (result.min_temprature):
                print("Lowest:", end = " ")
                print(str(result.min_temprature.min_temprature) + "C on", end = " ")
                print(result.min_temprature.date.strftime("%B %d"))

            if (result.max_humidity):
                print("Humidity:", end = " ")
                print(str(result.max_humidity.max_humidity) + "% on", end = " ")
                print(result.max_humidity.date.strftime("%B %d"))
                print("\n")
        else:
            print("Data not found.\n")

    def print_average_report(self, result, month_number, given_year):
        if (result):
            print("Highest Average: " + str(int(result.max_avg_temperature)) + "C")
            print("Lowest Average: " + str(int(result.min_avg_temperature)) + "C")
            print("Average Mean Humidity:" + str(int(result.mean_humidity_avg)) + "%\n")
        else:
            print(calendar.month_name[int(month_number)], given_year)
            print("Data not found.\n")



    def print_monthly_report(self, monthly_records, month_number, given_year):
        print(calendar.month_name[int(month_number)], given_year)
        if (monthly_records):
            print(len(monthly_records))
            for day in monthly_records:
                if (hasattr(day,'min_temprature') and hasattr(day,'max_temprature')):
                    print(day.date.strftime("%d"), end = " ")
                    print(Fore.BLUE + "+" * day.min_temprature, end = "")
                    print(Fore.RED + "+" * day.max_temprature, end = " ")
                    print(Fore.WHITE + str(day.min_temprature) + "C - " + str(day.max_temprature) + "C")
            print("\n")
        else:
            print("Data not found.\n")
