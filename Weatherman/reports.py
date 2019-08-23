#!/usr/bin/python3
import calendar

from colorama import Fore

class WeathermanReportPrinter:

    def print_yearly_report(self, result):
        self.__print_reading(result.max_temprature, "max_temprature", "Highest:", "C")
        self.__print_reading(result.min_temprature, "min_temprature", "Lowest:", "C")
        self.__print_reading(result.max_humidity, "max_humidity", "Humidity:", "%")
        print("\n")

    def __print_reading(self, weather_record, attribute_name, fact_prefix, postfix):
        print(fact_prefix, end=" ")
        print(f"{str(getattr(weather_record, attribute_name))}{postfix} on", end=" ")
        print(weather_record.date.strftime("%B %d"))

    def print_average_report(self, result):

        print(f"Highest Average: {str(int(result.highest_avg_temp))}C")
        print(f"Lowest Average: {str(int(result.lowest_avg_temp))}C")
        print(f"Average Mean Humidity: {str(int(result.avg_mean_humidity))}%\n")



    def print_monthly_report(self, monthly_records, month_number, given_year):
        print(calendar.month_name[int(month_number)], given_year)
        for day in monthly_records:
            print(day.date.strftime("%d"), end=" ")
            print(f"{Fore.BLUE}+" * day.min_temprature, end="")
            print(f"{Fore.RED}+" * day.max_temprature, end=" ")
            print(f"{Fore.WHITE}{str(day.min_temprature)}C - {str(day.max_temprature)}C")
        print("\n")
