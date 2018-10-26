#!/usr/bin/python3.6
from constants import FILE_ERROR_MESSAGE


class WeatherReporting:

    def display_yearly_report(self, report, record_info):
        print(
            record_info,
            '\nHighest: ', report[0][0], 'C on ', report[0][1], report[0][2],
            '\nLowest: ', report[1][0], 'C on ', report[1][1], report[1][2],
            '\nHumidity: ', report[2][0], '% on ', report[2][1], report[2][2],
            '\n-------------------------------------\n'
        )

    def display_monthly_report(self, report, record_info):
        print(
            record_info,
            '\nHighest Average: ', round(report[0]), 'C',
            '\nLowest Average: ', round(report[1]), 'C',
            '\nAverage Mean Humidity: ', round(report[2]), '%',
            '\n-------------------------------------\n'
        )

    def display_monthly_bar_chart(self, report, record_info):
        high_temperature_list = report.get('high_temprature')
        low_temperature_list = report.get('low_temprature')
        print(record_info)
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

    def display_report(self, report, operation, record_info):
        if len(report) > 1:
            if operation == 'e':
                self.display_yearly_report(report, record_info)
            elif operation == 'a':
                self.display_monthly_report(report, record_info)
            else:
                self.display_monthly_bar_chart(report, record_info)
        else:
            print(FILE_ERROR_MESSAGE, '\n\n')
