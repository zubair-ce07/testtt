#!/usr/bin/python3.6
import calendar

from constants import FILE_ERROR_MESSAGE


class WeatherReporting:
    color_blue = "\033[0;34;48m"
    color_normal = "\033[0m"
    color_red = "\033[0;31;48m"

    def yearly_report(self, report):
        if not report:
            print(FILE_ERROR_MESSAGE, '\n\n')
            return

        highest_temp_date = report['highest_temperature_date']
        lowest_temp_date = report['lowest_temperature_date']
        highest_humidity_date = report['highest_humidity_date']

        highest_temperature_report = f"Highest: {report['highest_temperature']}C"\
            f"on {calendar.month_name[highest_temp_date.month]} {highest_temp_date.day}"
        lowest_temperature_report = f"Lowest: {report['lowest_temperature']}C"\
            f"on {calendar.month_name[lowest_temp_date.month]} {lowest_temp_date.day}"
        highest_humidity_report = f"Humidity: {report['highest_humidity']}% "\
            f"on {calendar.month_name[highest_humidity_date.month]} {highest_humidity_date.day}"
        
        print(highest_temperature_report)
        print(lowest_temperature_report)
        print(highest_humidity_report)
        print('-------------------------------------\n')

    def monthly_report(self, report):
        if not report:
            print(FILE_ERROR_MESSAGE, '\n\n')
            return

        highest_average = f"Highest Average: {round(report['average_max_temperature'])}C"
        lowest_average = f"Lowest Average: {round(report['average_min_temperature'])}C"
        mean_humidity = f"Average Mean Humidity: {round(report['average_mean_humidity'])}%"

        print(highest_average)
        print(lowest_average)
        print(mean_humidity)
        print('-------------------------------------\n')

    def monthly_bar_chart(self, weather_records, date):
        month_record = weather_records.month_readings(date)
        if not month_record:
            print(FILE_ERROR_MESSAGE, '\n\n')
            return
        
        high_temperatures = month_record.get('max_temperature')
        low_temperatures = month_record.get('min_temperature')
        dates = month_record.get('pkt')
        
        for high, low, date in zip(high_temperatures, low_temperatures, dates):
            highest_temp_bar = f"{self.color_red}{'+'*abs(high)}{self.color_normal}" if high else ''
            lowest_temp_bar = f"{self.color_blue}{'+'*abs(low)}{self.color_normal}" if low else ''
            highest_temp = f"{high} C" if high else ''
            lowest_temp = f"{low} C" if low else ''

            print(date.day, lowest_temp_bar, highest_temp_bar, lowest_temp, highest_temp)

        print('-------------------------------------\n')
