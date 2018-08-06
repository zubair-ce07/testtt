from __future__ import print_function
from data_calculation_weather_man import DataCalculation

import calendar


class ReportGenerator(DataCalculation):
    """This class takes processed data from DataCalculation class and outputs
    a report for each instance of calculated data according to the format
    specified in the project specifications.
    methods : monthly_report : outputs the monthly report
              yearly_report : outputs the yearly report"""

    def __init__(self, calculated_data):
        """This __init__ function takes inputs from its parent class
        'DataCalculation' and saves the processed data in its own variables
        so it can manipulate it and display on the terminal in the specific format.
        :param calculated_data: class is inherited to obtain calculated data
               All calculated variables are saved in its own variables"""
        self.avg_highest_temp = calculated_data.avg_highest_temp
        self.avg_lowest_temp = calculated_data.avg_lowest_temp
        self.avg_mean_humid = calculated_data.avg_mean_humid
        self.maximum_temp = calculated_data.maximum_temp
        self.maximum_temp_date = calculated_data.maximum_temp_date
        self.minimum_temp = calculated_data.minimum_temp
        self.minimum_temp_date = calculated_data.minimum_temp_date
        self.maximum_humid = calculated_data.maximum_humid
        self.maximum_humid_day = calculated_data.maximum_humid_day

    def monthly_report(self):
        """This method displays the monthly report consisting of
        highest average, lowest average, and average mean humidity.
        :returns: formatted data for monthly report of flag '-a'
        """
        print('Highest Average {} C'.format(self.avg_highest_temp))
        print('Lowest Average {} C'.format(self.avg_lowest_temp))
        print('Average Mean Humidity {} %'.format(self.avg_mean_humid))

    def yearly_report(self):
        """This method displays the yearly report consisting of highest
        temperature, its date, lowest temperature, its date, highest humid day
        and its date. It also converts the date to abbreviation form
        :returns: formatted data to terminal depending on the flag """
        max_date = self.maximum_temp_date[7:]
        max_month_num = self.maximum_temp_date[5:6]
        max_month = calendar.month_abbr[int(max_month_num)]
        min_date = self.minimum_temp_date[7:]
        min_month_num = self.minimum_temp_date[5:6]
        min_month = calendar.month_abbr[int(min_month_num)]
        humid_date = self.maximum_humid_day[7:]
        humid_month_num = self.maximum_humid_day[5:6]
        humid_month = calendar.month_abbr[int(humid_month_num)]
        print('Highest Temperature {} C on {} {}'.format(self.maximum_temp
                                                         , max_month, max_date))
        print('Lowest Temperature {} C on {} {}'.format(self.minimum_temp
                                                        , min_month, min_date))
        print('Highest Humidity {} C on {} {}'.format(self.maximum_humid
                                                      , humid_month, humid_date))
