# -*- coding: utf-8 -*-
"""
All implementations regarding reports handling and calculations are done here, reports are managed and printed from
this script as well.
"""
import statistics

from colorama import Fore, Style

from weather_man.utils.global_content import ReportHelper, DateMapper


class ResultCalculator:
    """
    Class for computing the calculations given the readings data structure.
    """
    @staticmethod
    def update_year_result(weather_info, report):
        """
        Given a report empty and new entry of weather data it updates that report if required
        checking different cases.
        :param weather_info: New entry to check
        :param report: Empty or already written report
        """
        max_temp = max(weather_info['max_temp'])
        report['highest_temp']['value'] = max_temp
        report['highest_temp']['day'] = DateMapper.get_month_full_name_and_day(
            weather_info['day'][weather_info['max_temp'].index(max_temp)])
        min_temp = min(weather_info['min_temp'])
        report['lowest_temp']['value'] = min_temp
        report['lowest_temp']['day'] = DateMapper.get_month_full_name_and_day(
            weather_info['day'][weather_info['min_temp'].index(min_temp)])
        min_temp = max(weather_info['max_humidity'])
        report['highest_humidity']['value'] = min_temp
        report['highest_humidity']['day'] = DateMapper.get_month_full_name_and_day(
            weather_info['day'][weather_info['max_humidity'].index(min_temp)])

    @staticmethod
    def update_year_with_month_report(weather_info, report):
        """
        Given a report empty and new entry of weather data it updates that report if required
        checking different cases.
        :param weather_info: New entry to check
        :param report: Empty or already written report
        """
        report['average_highest_temp']['value'] = statistics.mean(weather_info['max_temp'])
        report['average_lowest_temp']['value'] = statistics.mean(weather_info['min_temp'])
        report['average_mean_humidity']['value'] = statistics.mean(weather_info['mean_humidity'])


class ReportHandler:
    """
    Class for creating the reports given the results data structure.
    """
    def __init__(self, report_category):
        self.report_category = report_category
        self.report = ReportHelper.get_empty_report(report_category)

    def update_year_report(self, weather_info):
        """
        Updates yearly report providing new weather data entry of a day.
        :param weather_info: Weather data entries.
        """
        ResultCalculator.update_year_result(weather_info, self.report)

    def update_year_with_month_report(self, weather_info):
        """
        Updates specific month of an year's report providing new weather data entry of a day.
        :param weather_info: Weather data entries.
        """
        ResultCalculator.update_year_with_month_report(weather_info, self.report)

    @staticmethod
    def show_month_bar_chart_report(weather_info):
        """
        Feature of weather man to display day temperature in 2 lines is done here, implementation is done to print on
        the console at the moment.
        :param weather_info: Weather data entries.
        """
        weather_info_zipped = zip(weather_info['max_temp'], weather_info['min_temp'], weather_info['day'])
        for highest_temp, lowest_temp, day in weather_info_zipped:
            day = DateMapper.get_date(day)
            stars = '+' * abs(highest_temp)
            print(f"{day} {Fore.RED}{stars}{Style.RESET_ALL} {highest_temp}C")
            stars = '+' * abs(lowest_temp)
            print(f"{day} {Fore.BLUE}{stars}{Style.RESET_ALL} {lowest_temp}C")

    @staticmethod
    def show_month_bar_chart_in_one_line_report(weather_info):
        """
        Feature of weather man to display day temperature in 1 lines is done here, implementation is done to print on
        the console at the moment.
        :param weather_info: Weather data entries
        """
        weather_info_zipped = zip(weather_info['max_temp'], weather_info['min_temp'], weather_info['day'])
        for highest_temp, lowest_temp, day in weather_info_zipped:
            day = DateMapper.get_date(day)
            stars = '+' * abs(lowest_temp)
            print(f"{day} {Fore.BLUE}{stars}{Style.RESET_ALL}", end="")
            stars = '+' * abs(highest_temp)
            print(f"{Fore.RED}{stars}{Style.RESET_ALL} {lowest_temp}C | {highest_temp}C")

    def show_report(self):
        """
        Print a specific report of weather data.
        """
        report_output = ReportHelper.get_report_output(self.report_category)
        for output_category, output_expresstion in report_output.items():
            if 'day' in self.report[output_category].keys():
                print(output_expresstion.format(
                    self.report[output_category]['value'], self.report[output_category]['day'])
                )
            else:
                print(output_expresstion.format(self.report[output_category]['value']))
