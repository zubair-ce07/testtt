""" This file contains the ReportGenerator class.
    Using the generate_report() function, that
    takes in the data and type of report to generate
    as an argument, an instance of this class returns
    the member variable `report` with the final
    calculated result.

    Owner: Muhammad Abdullah Zafar -- Arbisoft
"""

import sys
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
        highest_temp = {'value': (-sys.maxsize - 1), 'date': ''}
        lowest_temp = {'value': (sys.maxsize), 'date': ''}
        highest_humid = {'value': (-sys.maxsize - 1), 'date': ''}

        for day in weather_data:
            date = day.timestamp

            day_max_temp = {'date': date,
                            'value': mk_int(day.max_temp,
                                            'max')
                            }

            day_min_temp = {'date': date,
                            'value': mk_int(day.min_temp,
                                            'min')
                            }

            day_max_humid = {'date': date,
                             'value': mk_int(day.mean_humidity,
                                             'max')
                             }

            if day_max_temp['value'] > highest_temp['value']:
                highest_temp['value'] = day_max_temp['value']
                highest_temp['date'] = date

            if day_min_temp['value'] < lowest_temp['value']:
                lowest_temp['value'] = day_min_temp['value']
                lowest_temp['date'] = date

            if day_max_humid['value'] > highest_humid['value']:
                highest_humid['value'] = day_max_humid['value']
                highest_humid['date'] = date

        self.report.clear_reports()

        self.report.add_report('Highest',
                               highest_temp['value'],
                               highest_temp['date'])

        self.report.add_report('Lowest',
                               lowest_temp['value'],
                               lowest_temp['date'])

        self.report.add_report('Humidity',
                               highest_humid['value'],
                               highest_humid['date'])

        return self.report

    def generate_report_monthly_average(self, weather_data):
        avg_highest_temp = 0
        avg_lowest_temp = 0
        avg_mean_humid = 0
        skip_days_min = 0
        skip_days_max = 0
        skip_days_mean = 0

        for day in weather_data:
            init_max_temp = mk_int_zero(day.max_temp)
            init_min_temp = mk_int_zero(day.min_temp)
            init_mean_humid = mk_int_zero(day.mean_humidity)

            if not init_max_temp:
                skip_days_max += 1
            else:
                avg_highest_temp += init_max_temp

            if not init_min_temp:
                skip_days_min += 1
            else:
                avg_lowest_temp += init_min_temp

            if not init_mean_humid:
                skip_days_mean += 1
            else:
                avg_mean_humid += init_mean_humid

        avg_highest_temp /= len(weather_data) - skip_days_max
        avg_lowest_temp /= len(weather_data) - skip_days_min
        avg_mean_humid /= len(weather_data) - skip_days_mean

        self.report.clear_reports()
        self.report.add_report('Highest Average', int(avg_highest_temp), '')
        self.report.add_report('Lowest Average', int(avg_lowest_temp), '')
        self.report.add_report('Avg Mean Humidity', int(avg_mean_humid), '')

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
            if len(req.split('/')) != 1:
                print("Wrong format. Exiting!")
                exit()

            print(color + dialouge + color_reset)
            return self.generate_report_yearly_highest(weather_data)

        elif calculation_type == '-a':
            if len(req.split('/')) != 2:
                print("Wrong format. Exiting!")
                exit()

            print(color + dialouge + color_reset)
            return self.generate_report_monthly_average(weather_data)

        elif calculation_type == '-c':
            if len(req.split('/')) != 2:
                print("Wrong format. Exiting!")
                exit()

            print(color + dialouge + color_reset)
            print(datetime.strftime(datetime.strptime(req, '%Y/%m'), '%B %Y'))
            return self.generate_report_monthly_bar_charts(weather_data)
