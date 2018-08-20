# -*- coding: utf-8 -*-
"""
Weather man application which perform data analytics on weather data.
"""
from weather_man_app.weather_reader import WeatherReader
from weather_man_app.utils.decorators import prepare_input
from weather_man_app.utils.report_handlers import ReportsHandler


class WeatherMan:
    """
    Contains complete flow required for working of weather man.
    """
    def __init__(self):
        self.data = None
        self.results = None

    @prepare_input
    def generate_year_result(self, **kwargs):
        """
        Get processed data of weather, generate and show report of an year.
        :param kwargs: key word arguments, required keys are: file_path and period (year or year/month)
        """
        self.results = ReportsHandler(report_category='years')
        weather_data_holder = WeatherReader(
            file_path=kwargs.get('file_path'),
            period=kwargs.get('period')
        )
        self.results.update_year_report(weather_data_holder.weather_readings)
        self.results.show_report()

    @prepare_input
    def generate_year_with_month_result(self, **kwargs):
        """
        Get processed data of weather, generate and show report of a specific month of an year.
        :param kwargs: key word arguments, required keys are: file_path and period (year or year/month)
        """
        self.results = ReportsHandler(report_category='year_with_month')
        weather_data_holder = WeatherReader(
            file_path=kwargs.get('file_path'),
            period=kwargs.get('period')
        )
        self.results.update_year_with_month_report(weather_data_holder.weather_readings)
        self.results.show_report()

    @prepare_input
    def generate_month_bar_chart_result(self, **kwargs):
        """
        Get processed data of weather, generate and show report of a month in form on bar charts.
        :param kwargs: key word arguments, required keys are: file_path and period (year or year/month)
        """
        self.results = ReportsHandler(report_category='month_bar_chart')
        weather_data_holder = WeatherReader(
            file_path=kwargs.get('file_path'),
            period=kwargs.get('period')
        )
        self.results.show_month_bar_chart_report(weather_data_holder.weather_readings)

    @prepare_input
    def generate_month_bar_chart_in_one_line_result(self, **kwargs):
        """
        Get processed data of weather, generate and show report of a month in form on bar charts in one line of
        each day.
        :param kwargs: key word arguments, required keys are: file_path and period (year or year/month)
        """
        self.results = ReportsHandler(report_category='month_bar_chart_in_one_line')
        weather_data_holder = WeatherReader(
            file_path=kwargs.get('file_path'),
            period=kwargs.get('period')
        )
        self.results.show_month_bar_chart_in_one_line_report(weather_data_holder.weather_readings)

    def show_result(self, file_path, category, year_month):
        """
        Calling function for weather man that calls specific functions depending on the categories.
        :param file_path: File path where weather data files are presenet
        :param category: Category of report to generate eg: year
        :param year_month: year_month is basically called period as it can be year eg 2010 or
         year with month like 2011/1
        :return:
        """
        getattr(self, 'generate_{}_result'.format(category))(
            category=category, file_path=file_path, period=year_month
        )
