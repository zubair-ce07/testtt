from data_calculator import CalculatingData
import calendar


class ReportGenerator(CalculatingData):
    """This is the main report generator module which takes input
    from other modules and then generates the reports accordingly."""

    def __init__(self, calculating_data):
        self.max = calculating_data.yearly_most_humid_value

    def generate_monthly_report(self, calculating_data):
        print('Calculating monthly averages for {} month of {}'.format
              (calculating_data.month_date[5],
               calculating_data.month_date[0:4]))
        print('Highest Average: {}'.format
              (round(calculating_data.average_high_temp)))
        print('Lowest Average: {}'.format
              (round(calculating_data.average_min_temp)))
        print('Average Mean Humidity: {}%\n'.format
              (round(calculating_data.average_mean_humidity)))

    def generate_yearly_report(self, calculating_data):
        print('Calculating Yearly report for {}'.format
              ((calculating_data.yearly_highest_temp_date[0:4])))
        print('Highest: {}C on {} {}'.format
              (calculating_data.yearly_highest_temp,
               calendar.month_abbr
               [int(calculating_data.yearly_highest_temp_date[5:6])],
               calculating_data.yearly_highest_temp_date[7:]))

        print('Lowest: {}C on {} {}'.format
              (calculating_data.yearly_lowest_temp,
               calendar.month_abbr
               [int(calculating_data.yearly_lowest_temp_date[5:6])],
               calculating_data.yearly_lowest_temp_date[7:]))

        print('Humidity: {}% on {} {}\n'.format
              (calculating_data.yearly_most_humid_value,
               calendar.month_abbr
               [int(calculating_data.yearly_most_humid_day[5:6])],
               calculating_data.yearly_most_humid_day[7:]))
