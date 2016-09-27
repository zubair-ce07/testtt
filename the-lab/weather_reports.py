import operator
from report_printer import ReportPrinter
from chart import Chart
from weather_data_reader import WeatherDataReader

class WeatherReports:
    @staticmethod
    def __get_extremum(weather_data, attribute, extremum_function=max):
        """ Finds the extremum value of an attribute in object list based on
        the extremum_function passed to it. """
        return extremum_function(
            [data for data in weather_data if getattr(data, attribute)],
            key=operator.attrgetter(attribute))

    @staticmethod
    def __get_chart_data(report_date, data_directory):
        """ Returns a list of list of maximum and minimum temperatures and
        a list of indices"""
        weather_data_reader = WeatherDataReader(report_date, data_directory)
        weather_data = weather_data_reader.get_weather_data()
        for weather_params in weather_data:
            if not weather_params.max_temp:
                weather_params.max_temp = 0
            if not weather_params.min_temp:
                weather_params.min_temp = 0

        max_temp_bar = [weather_param.max_temp for weather_param in
                        weather_data]
        min_temp_bar = [weather_param.min_temp for weather_param in
                        weather_data]
        indices = [k.date.split('-')[2] for k in weather_data]

        return [max_temp_bar, min_temp_bar], indices

    @staticmethod
    def monthly_console_bar_chart(report_date, data_directory):
        """ Gets the data for a bar chart and passes it to the appropriate cmd
        method of the Chart class """
        chart_bars, indices = WeatherReports.__get_chart_data(
            report_date, data_directory)
        Chart.console_barchart(chart_bars, indices)

    @staticmethod
    def monthly_console_stack_chart(report_date, data_directory):
        """ Gets the data for a stack chart and passes it to the appropriate
        method of the Chart class """
        chart_bars, indices = WeatherReports.__get_chart_data(
            report_date, data_directory)
        Chart.console_stackchart(chart_bars, indices)

    @staticmethod
    def monthly_gui_bar_chart(report_date, data_directory):
        """ Gets the data for a bar chart and passes it to the appropriate gui
        method of the Chart class """
        chart_bars, indices = WeatherReports.__get_chart_data(
            report_date, data_directory)
        Chart.gui_barchart(chart_bars, indices, ('Min', 'Max'),
                           ytitle='Temperature(C)',
                           char_title='Min Max Temperature Bar Chart')

    @staticmethod
    def monthly_averages(report_date, data_directory):
        """ For a given month, gets the maximum and minimum average
        temperatures and calls the appropriate function of the ReportPrinter
        class """
        weather_data_reader = WeatherDataReader(report_date, data_directory)
        weather_data = weather_data_reader.get_weather_data()

        max_avg = WeatherReports.__get_extremum(weather_data, 'max_avg_temp',
                                                extremum_function=max)
        least_avg = WeatherReports.__get_extremum(weather_data, 'min_avg_temp',
                                                  extremum_function=min)
        max_humidity = WeatherReports.__get_extremum(weather_data,
                                                     'max_avg_humidty',
                                                     extremum_function=max)
        ReportPrinter.averages(max_avg, least_avg, max_humidity)

    @staticmethod
    def annual_extrema(report_date, data_directory):
        """ For a given year, gets the maximum and minimum
        temperatures/humidity and calls the appropriate function of the
        ReportPrinter class """
        weather_data_reader = WeatherDataReader(report_date, data_directory)
        weather_data = weather_data_reader.get_weather_data()
        max_temp = WeatherReports.__get_extremum(weather_data, 'max_temp',
                                                 extremum_function=max)
        min_temp = WeatherReports.__get_extremum(weather_data, 'min_temp',
                                                 extremum_function=min)
        max_humidity = WeatherReports.__get_extremum(weather_data,
                                                     'max_humidity',
                                                     extremum_function=max)
        min_humidity = WeatherReports.__get_extremum(weather_data,
                                                     'min_humidity',
                                                     extremum_function=min)

        ReportPrinter.extrema(max_temp, min_temp, max_humidity, min_humidity)
