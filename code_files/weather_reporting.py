#!/usr/bin/python3.6
import calendar

from constants import FILE_ERROR_MESSAGE


class WeatherReporting:

    def display_yearly_report(self, report, date):
        highest_month_name = calendar.month_name[report[0][1].month]
        lowest_month_name = calendar.month_name[report[1][1].month]
        most_humid_month_name = calendar.month_name[report[2][1].month]
        print(
            date.year,
            '\nHighest: ', report[0][0], 'C on ', highest_month_name, report[0][1].day,
            '\nLowest: ', report[1][0], 'C on ', lowest_month_name, report[1][1].day,
            '\nHumidity: ', report[2][0], '% on ', most_humid_month_name, report[2][1].day,
            '\n-------------------------------------\n'
        )

    def display_monthly_report(self, report, date):
        print(
            date.year, calendar.month_name[date.month],
            '\nHighest Average: ', round(report[0]), 'C',
            '\nLowest Average: ', round(report[1]), 'C',
            '\nAverage Mean Humidity: ', round(report[2]), '%',
            '\n-------------------------------------\n'
        )

    def display_monthly_bar_chart(self, report, date):
        high_temperature_list = report.get('high_temprature')
        low_temperature_list = report.get('low_temprature')
        print(date.year, calendar.month_name[date.month])
        count = 1
        for high, low in zip(high_temperature_list, low_temperature_list):
            if low is None and high is None:
                print(count)
            elif low is None or high is None:
                if low is None:
                    print(count, "\033[0;31;48m+"*abs(high), "\033[0m  ",
                          str(high) + "C")
                if high is None:
                    print(count, "\033[0;34;48m+"*abs(low),
                          "\033[0m", str(low), "C")
            else:
                print(count, "\033[0;34;48m+"*abs(low),
                      "\033[0;31;48m+"*abs(high), "\033[0m", str(low), 'C',
                      str(high) + 'C')
            count += 1
        print('\n-------------------------------------\n')

    def display_report(self, report, operation, date):
        if len(report) > 1:
            if operation == 'e':
                self.display_yearly_report(report, date)
            elif operation == 'a':
                self.display_monthly_report(report, date)
            else:
                self.display_monthly_bar_chart(report, date)
        else:
            print(FILE_ERROR_MESSAGE, '\n\n')
