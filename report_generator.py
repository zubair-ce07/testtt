import calendar
from data_calculator import CalculatingData


class ReportGenerator(CalculatingData):

    def __init__(self, calculating_data):
        self.max_temp = calculating_data.yearly_most_humid_value

    def generate_monthly_report(self, calculating_data):
        print(f"Calculating monthly averages for "
              f"{calculating_data.month_date[5]} month of "
              f"{calculating_data.month_date[0:4]}")
        print(f"Highest Average: {round(calculating_data.average_high_temp)}")
        print(f"Lowest Average: {round(calculating_data.average_min_temp)}")
        print(f"Average Mean Humidity: "
              f"{round(calculating_data.average_mean_humidity)}%\n")

    def generate_yearly_report(self, calculating_data):

        highest_month = calendar.month_abbr\
        [int(calculating_data.yearly_highest_temp_date[5:6])]
        lowest_month = calendar.month_abbr\
        [int(calculating_data.yearly_lowest_temp_date[5:6])]
        humid_month = calendar.month_abbr\
        [int(calculating_data.yearly_most_humid_day[5:6])]

        print(f"Calculating Yearly report for "
              f"{calculating_data.yearly_highest_temp_date[0:4]}")
        print(f"Highest: {calculating_data.yearly_highest_temp}C on "
              f"{highest_month} "
              f"{calculating_data.yearly_highest_temp_date[7:]}")
        print(f"Lowest: {calculating_data.yearly_lowest_temp}C on "
              f"{lowest_month} "
              f"{ calculating_data.yearly_lowest_temp_date[7:]}")
        print(f"Humidity: {calculating_data.yearly_most_humid_value}% on"
              f" {humid_month} "
              f"{calculating_data.yearly_most_humid_day[7:]}\n")
