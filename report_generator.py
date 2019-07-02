import calendar

from data_calculator import DataCalculator


class ReportGenerator(DataCalculator):

    def __init__(self, calculating_data):
        self.max_temp = calculating_data.yearly_most_humid_value

    def generate_monthly_report(self, calculating_data):
        print(f"Highest Average: {round(calculating_data.average_high_temp)}")
        print(f"Lowest Average: {round(calculating_data.average_min_temp)}")
        print(f"Average Mean Humidity: "
              f"{round(calculating_data.average_mean_humidity)}%\n")

    def generate_yearly_report(self, calculating_data):
        highest_date = calculating_data.yearly_highest_temp_date
        lowest_date = calculating_data.yearly_lowest_temp_date
        humid_date = calculating_data.yearly_most_humid_day

        print(f"Highest: {calculating_data.yearly_highest_temp}C on "
              f"{highest_date.day}"
              f" {calendar.month_abbr[highest_date.month]}")
        print(f"Lowest: {calculating_data.yearly_lowest_temp}C on "
              f"{ lowest_date.day}"
              f" {calendar.month_abbr[lowest_date.month]}")
        print(f"Humidity: {calculating_data.yearly_most_humid_value}% on "
              f"{humid_date.day}"
              f" {calendar.month_abbr[humid_date.month]}")

    def generate_bonus_report(self, weather_files, date):

        iterations = 0
        for entry in weather_files:
            if entry.date.year == date.year and \
                    entry.date.month == date.month:
                iterations += 1
                maximum = entry.maximum_temp
                minimum = entry.minimum_temp
                difference = maximum - minimum
                print(iterations, " ", end='')
                for values in range(minimum):
                    print('\033[1;34m*\033[1;m', end='')
                for values in range(difference):
                    print('\033[1;31m*\033[1;m', end='')
                print(" ", minimum, "C - ", maximum, "C\n")
