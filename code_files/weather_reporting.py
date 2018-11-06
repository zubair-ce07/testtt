#!/usr/bin/python3.6
import calendar

from constants import FILE_ERROR_MESSAGE


class WeatherReporting:
    color_blue = "\033[0;34;48m"
    color_normal = "\033[0m"
    color_red = "\033[0;31;48m"

    def yearly_report(self, report, date):
        highest_temp_date = report['highest_temp_date']
        lowest_temp_date = report['lowest_temp_date']
        highest_humidity_date = report['highest_humidity_date']

        print(date.year)

        print('Highest: ', report['highest_temp'], 'C on ',
              calendar.month_name[highest_temp_date.month], highest_temp_date.day)

        print('Lowest: ', report['lowest_temp'], 'C on ',
              calendar.month_name[lowest_temp_date.month], lowest_temp_date.day)

        print('Humidity: ', report['highest_humidity'], '% on ',
              calendar.month_name[highest_humidity_date.month], highest_humidity_date.day)

        print('\n-------------------------------------\n')

    def monthly_report(self, report, date):
        highest_temp_avg = round(report['average_max_temp'])
        lowest_temp_avg = round(report['average_min_temp'])
        mean_humidity_avg = round(report['average_mean_humidity'])

        print(date.year, calendar.month_name[date.month])

        print('Highest Average: ', highest_temp_avg, 'C')

        print('Lowest Average: ', lowest_temp_avg, 'C')

        print('Average Mean Humidity: ', mean_humidity_avg, '%')

        print('\n-------------------------------------\n')

    def monthly_bar_chart(self, report, record_date):
        high_temperature_list = report.get('high_temprature')
        low_temperature_list = report.get('low_temprature')
        dates = report['dates']
        print(record_date.year, calendar.month_name[record_date.month])

        for high, low, date in zip(high_temperature_list, low_temperature_list, dates):
            highest_temp_bar = f"{self.color_red}{'+'*abs(high)}{self.color_normal}" if high else ''
            lowest_temp_bar = f"{self.color_blue}{'+'*abs(low)}{self.color_normal}" if low else ''
            highest_temp = f"{high} C" if high else ''
            lowest_temp = f"{low} C" if low else ''

            print(date.day, lowest_temp_bar, highest_temp_bar, lowest_temp, highest_temp)

        print('\n-------------------------------------\n')

    def display_report(self, report, date):
        operation = report.get('operation')
        
        if operation == 'e':
            self.yearly_report(report, date)
        elif operation == 'a':
            self.monthly_report(report, date)
        elif operation == 'c':
            self.monthly_bar_chart(report, date)
        else:
            print(FILE_ERROR_MESSAGE, '\n\n')
