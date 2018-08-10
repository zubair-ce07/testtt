# -*- coding: utf-8 -*-
"""
All implementations regarding reports handling and calculations are done here, reports are managed and printed from
this script as well.
"""
from colorama import Fore, Style

from app_factory.weather_man_app.utils.global_contants import MathHelper, ReportsHelper, DateMapper
from app_factory.configs.app_configs import AppConfigs


class ResultsCalculator(object):
    """
    Class for computing the calculations given the readings data structure.
    """
    @staticmethod
    def update_year_result(weathe_data_entry, report):
        max_temp = MathHelper.parse_int(weathe_data_entry['Max TemperatureC'])
        min_temp = MathHelper.parse_int(weathe_data_entry['Min TemperatureC'])
        humidity = MathHelper.parse_int(weathe_data_entry['Max Humidity'])
        day = weathe_data_entry['PKT']
        if max_temp and max_temp > report['highest_temp']['value']:
            report['highest_temp']['value'] = max_temp
            report['highest_temp']['day'] = DateMapper.get_month_full_name(day)
        if min_temp and min_temp < report['lowest_temp']['value']:
            report['lowest_temp']['value'] = min_temp
            report['lowest_temp']['day'] = DateMapper.get_month_full_name(day)
        if humidity and humidity > report['highest_humidity']['value']:
            report['highest_humidity']['value'] = humidity
            report['highest_humidity']['day'] = DateMapper.get_month_full_name(day)

    @staticmethod
    def update_year_with_month_report(weathe_data_entry, report):
        max_temp = MathHelper.parse_int(weathe_data_entry['Max TemperatureC'])
        min_temp = MathHelper.parse_int(weathe_data_entry['Min TemperatureC'])
        mean_humidity = MathHelper.parse_int(weathe_data_entry[' Mean Humidity'])
        day = weathe_data_entry['PKT']
        if max_temp:
            report['average_highest_temp']['value'] += max_temp
            report['average_highest_temp']['total-entries'] += 1
        if min_temp:
            report['average_lowest_temp']['value'] += min_temp
            report['average_lowest_temp']['total-entries'] += 1
        if mean_humidity:
            report['average_mean_humidity']['value'] += mean_humidity
            report['average_mean_humidity']['total-entries'] += 1

    @staticmethod
    def get_month_bar_chart_result_for_day(weathe_data_entry):
        return MathHelper.parse_int(weathe_data_entry['Max TemperatureC']), \
               MathHelper.parse_int(weathe_data_entry['Min TemperatureC']), \
               weathe_data_entry['PKT'].split('-')[-1]

    @staticmethod
    def compute_average(report):
        for category in report.keys():
            report[category]['value'] /= report[category]['total-entries']


class ReportsHandler(object):
    """
    Class for creating the reports given the results data structure.
    """
    def __init__(self, report_category):
        self.report_category = report_category
        self.report = ReportsHelper.get_empty_report(AppConfigs.app_name, report_category)

    def update_year_report(self, weather_data_entry):
        ResultsCalculator.update_year_result(weather_data_entry, self.report)

    def update_year_with_month_report(self, weather_data_entry):
        ResultsCalculator.update_year_with_month_report(weather_data_entry, self.report)

    def show_month_bar_chart_report(self, weather_data_entry):
        highest_temp, lowest_temp, day = ResultsCalculator.get_month_bar_chart_result_for_day(
            weather_data_entry
        )
        stars = '+' * abs(highest_temp)
        print(f"{day} {Fore.RED}{stars}{Style.RESET_ALL} {highest_temp}C")
        stars = '+' * abs(lowest_temp)
        print(f"{day} {Fore.BLUE}{stars}{Style.RESET_ALL} {lowest_temp}C")

    def show_month_bar_chart_in_one_line_report(self, weather_data_entry):
        highest_temp, lowest_temp, day = ResultsCalculator.get_month_bar_chart_result_for_day(
            weather_data_entry
        )
        stars = '+' * abs(lowest_temp)
        print(f"{day} {Fore.BLUE}{stars}{Style.RESET_ALL}", end="")
        stars = '+' * abs(highest_temp)
        print(f"{Fore.RED}{stars}{Style.RESET_ALL} {lowest_temp}C | {highest_temp}C")

    def show_report(self):
        report_output = ReportsHelper.get_report_output(AppConfigs.app_name, self.report_category)
        for output_category, str_expression in report_output.items():
            if 'day' in self.report[output_category].keys():
                print(str_expression.format(
                    self.report[output_category]['value'], self.report[output_category]['day'])
                )
            else:
                print(str_expression.format(self.report[output_category]['value']))

    def prepare_averages_for_result(self):
        ResultsCalculator.compute_average(self.report)
