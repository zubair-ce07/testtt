#!/usr/bin/python3
import calendar
import colorama
from colorama import Fore
from colorama import Style

from data_holder import *


class WeathermanReportPrinter:
    'Class to print reports'

    def print_yearly_report(self, facts):

        highest_temp = facts[0]
        min_temp = facts[1]
        max_humidity = facts[2]

        if (highest_temp):
            print("Highest:", end = " ")
            print(str(highest_temp[yearly_record_fields[2]]) + "C on", end = " ")
            print(highest_temp[yearly_record_fields[0]].strftime("%B %d"))

            print("Lowest:", end = " ")
            print(str(min_temp[yearly_record_fields[1]]) + "C on", end = " ")
            print(min_temp[yearly_record_fields[0]].strftime("%B %d"))

            print("Humidity:", end = " ")
            print(str(max_humidity[yearly_record_fields[3]]) + "% on", end = " ")
            print(max_humidity[yearly_record_fields[0]].strftime("%B %d"))
            print("\n")

        else:
            print("Data not found.\n")

    def print_average_report(self, avg_facts, month_number, given_year):
        if (avg_facts[0] == 0 and avg_facts[1] == 0 and avg_facts[2] == 0):
            print(calendar.month_name[int(month_number)], given_year)
            print("Data not found.\n")
        else:
            print("Highest Average: " + str(int(avg_facts[1])) + "C")
            print("Lowest Average: " + str(int(avg_facts[0])) + "C")
            print("Average Mean Humidity:" + str(int(avg_facts[2])) + "%\n")

    def print_monthly_report(self, monthly_records, month_number, given_year):
        print(calendar.month_name[int(month_number)], given_year)
        if (monthly_records):

            for day in monthly_records:
                print(day[temperature_fields[0]].strftime("%d"), end = " ")
                print(Fore.BLUE + "+" * day[temperature_fields[1]], end = "")
                print(Fore.RED + "+" * day[temperature_fields[2]], end = " ")
                print(Fore.WHITE + str(day[temperature_fields[1]]) + "C - " + str(day[temperature_fields[2]]) + "C")
            print("\n")
        else:
            print("Data not found.\n")
