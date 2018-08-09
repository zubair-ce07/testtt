# -*- coding: utf-8 -*-
"""
Weather man application which perform data analytics on weather data.
"""
from app_factory.weather_man_app.utils.data_handlers import WeatherReadingData
from app_factory.weather_man_app.utils.decorators import validate_input
from app_factory.weather_man_app.utils.design_patterns import Singleton
from app_factory.weather_man_app.utils.report_handlers import ReportsHandler


class WeatherMan(metaclass=Singleton):
    """
    Contains complete flow required for working of weather man.
    """
    def __init__(self):
        self.data = None
        self.results = None

    @validate_input
    def year_result(self, *args, **kwargs):
        self.results = ReportsHandler(report_category='years')
        weather_data_holder = WeatherReadingData(
            file_path=kwargs.get('file_path'),
            period=kwargs.get('period')
        )
        for data in weather_data_holder.weather_data:
            self.results.update_year_report(data)
        self.results.show_report()

    @validate_input
    def year_with_month_result(self, *args, **kwargs):
        self.results = ReportsHandler(report_category='year_with_month')
        weather_data_holder = WeatherReadingData(
            file_path=kwargs.get('file_path'),
            period=kwargs.get('period')
        )
        for data in weather_data_holder.weather_data:
            self.results.update_year_with_month_report(data)
        self.results.prepare_averages_for_result()
        self.results.show_report()

    @validate_input
    def month_bar_chart_result(self, *args, **kwargs):
        self.results = ReportsHandler(report_category='month_bar_chart')
        weather_data_holder = WeatherReadingData(
            file_path=kwargs.get('file_path'),
            period=kwargs.get('period')
        )
        for data in weather_data_holder.weather_data:
            self.results.show_month_bar_chart_report(data)

    @validate_input
    def month_bar_chart_in_one_line_result(self, *args, **kwargs):
        self.results = ReportsHandler(report_category='month_bar_chart_in_one_line')
        weather_data_holder = WeatherReadingData(
            file_path=kwargs.get('file_path'),
            period=kwargs.get('period')
        )
        for data in weather_data_holder.weather_data:
            self.results.show_month_bar_chart_in_one_line_report(data)

    def show_result(self, file_path, category, year_month):
        return getattr(self, '{}_result'.format(category))(category=category, file_path=file_path, period=year_month)
