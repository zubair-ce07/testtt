from datetime import datetime

from constants import Colors, ReportTypes
from utilities import draw_bar_graph


class ReportGenerator:
    def __init__(self, calculations_results):
        self.__calculation_results = calculations_results
        self.__temp_unit = 'C'

    def generate(self, report_type):
        if report_type == ReportTypes.SHOW_EXTREMES:
            self.__show_extreme_stats()
        elif report_type == ReportTypes.SHOW_MEANS:
            self.__show_mean_stats()
        elif report_type == ReportTypes.SHOW_GRAPHS:
            self.__show_graphs()

    def __show_extreme_stats(self):

        max_temperature = self.__calculation_results.max_temperature_reading.max_temperature
        min_temperature = self.__calculation_results.min_temperature_reading.min_temperature
        max_humidity = self.__calculation_results.max_humidity_reading.max_humidity

        max_temperature_date = self.__calculation_results.max_temperature_reading.reading_date
        min_temperature_date = self.__calculation_results.min_temperature_reading.reading_date
        max_humidity_date = self.__calculation_results.max_humidity_reading.reading_date

        print(f"Highest: {max_temperature}{self.__temp_unit} on {datetime.strftime(max_temperature_date, '%B, %Y')}")
        print(f"Lowest: {min_temperature}{self.__temp_unit} on {datetime.strftime(min_temperature_date, '%B, %Y')}")
        print(f"Humidity: {max_humidity}% on {datetime.strftime(max_humidity_date, '%B, %Y')}")

    def __show_mean_stats(self):
        print(f'Average Max Temperature: {round(self.__calculation_results.average_max_temperature)}{self.__temp_unit}')
        print(f'Average Min Temperature: {round(self.__calculation_results.average_min_temperature)}{self.__temp_unit}')
        print(f'Average Mean Humidity: {round(self.__calculation_results.average_mean_humidity)}%')

    def __show_graphs(self):
        print(f"{self.__calculation_results[0].reading_date.strftime('%B, %Y')}")

        bar_colors = (Colors.RED.value, Colors.BLUE.value)

        for data in self.__calculation_results:
            bar_limits = (abs(data.max_temperature), abs(data.min_temperature))
            print(draw_bar_graph(data.reading_date.strftime('%d'), bar_limits, bar_colors))
