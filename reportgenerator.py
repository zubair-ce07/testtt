""" This file contains the ReportGenerator class.
    Using the generate_report() function, that
    takes in the data and type of report to generate
    as an argument, an instance of this class returns
    the member variable `report` with the final
    calculated result.

    Owner: Muhammad Abdullah Zafar -- Arbisoft
"""

import sys
from statistics import mean
from datetime import datetime
from reportcontainer import ReportContainer


def mk_int(string_int, t):
    string_int = string_int.strip()

    if not string_int and t == 'min':
        return sys.maxsize
    elif not string_int and t == 'max':
        return (-sys.maxsize - 1)
    else:
        return int(string_int)


def mk_int_zero(string_int):
    return int(string_int.strip()) if string_int else 0


class ReportGenerator:
    report = ReportContainer()

    def generate_report_yearly_highest(self, weather_data):

        highest_temp = str(max([int(x.max_temp)
                                for x in weather_data
                                if x.max_temp != '']))

        lowest_temp = str(min([int(x.min_temp)
                               for x in weather_data
                               if x.min_temp != '']))

        highest_humid = str(max([int(x.max_humidity)
                                 for x in weather_data
                                 if x.max_humidity != '']))

        final_highest = [[d.max_temp, d.timestamp]
                         for d in weather_data
                         if d.max_temp == highest_temp]

        final_lowest = [[d.min_temp, d.timestamp]
                        for d in weather_data
                        if d.min_temp == lowest_temp]

        final_humid = [[d.max_humidity, d.timestamp]
                       for d in weather_data
                       if d.max_humidity == highest_humid]

        self.report.clear_reports()

        self.report.add_report('Highest',
                               final_highest[0][0],
                               final_highest[0][1])

        self.report.add_report('Lowest',
                               final_lowest[0][0],
                               final_lowest[0][1])

        self.report.add_report('Humidity',
                               final_humid[0][0],
                               final_humid[0][1])

        return self.report

    def generate_report_monthly_average(self, weather_data):
        max_temps = [int(x.max_temp) for x in weather_data if x.max_temp != '']
        min_temps = [int(x.min_temp) for x in weather_data if x.min_temp != '']
        max_humid = [int(x.max_humidity)
                     for x in weather_data
                     if x.max_humidity != '']

        avg_max_temp = mean(max_temps)
        avg_min_temp = mean(min_temps)
        avg_max_humid = mean(max_humid)

        self.report.clear_reports()
        self.report.add_report('Highest Average', int(avg_max_temp), '')
        self.report.add_report('Lowest Average', int(avg_min_temp), '')
        self.report.add_report('Avg Mean Humidity', int(avg_max_humid), '')

        return self.report

    def generate_report_monthly_bar_charts(self, weather_data):

        self.report.clear_reports()
        purple = "\033[0;35;40m"
        red = "\033[0;31;40m+"
        blue = "\033[0;34;40m+"

        for day in weather_data:
            day_max_temp = day.max_temp
            day_min_temp = day.min_temp

            date = day.timestamp
            if date:
                date = datetime.strptime(date, '%Y-%m-%d')
                date = datetime.strftime(date, '%d') + ' '

                range_max_temp = range(abs(mk_int_zero(day_max_temp)))
                range_min_temp = range(abs(mk_int_zero(day_min_temp)))

                final_string = ''
                final_string = purple + date
                final_string += ''.join([blue for x in range_min_temp])
                final_string += ''.join([red for x in range_max_temp])
                final_string += ' ' + purple + day_min_temp + 'C'
                final_string += ' - ' + purple + day_max_temp + 'C'

                print(final_string.replace(purple + 'C', 'No Value Available'))

        print("\033[0;0;40m")

    def generate_report(self, weather_data, calculation_type, req):
        color = "\033[1;30;47m"
        color_reset = "\033[0;37;40m"
        dialouge = 'Report for ' + req + ' for option ' + calculation_type
        if calculation_type == '-e':
            print(color + dialouge + color_reset)
            return self.generate_report_yearly_highest(weather_data)

        elif calculation_type == '-a':
            print(color + dialouge + color_reset)
            return self.generate_report_monthly_average(weather_data)

        elif calculation_type == '-c':
            print(color + dialouge + color_reset)
            print(datetime.strftime(datetime.strptime(req, '%Y/%m'), '%B %Y'))
            return self.generate_report_monthly_bar_charts(weather_data)
