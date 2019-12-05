from utilities import format_date, draw_bar_graph, round_float
from constants import Colors, Reports


class ReportGenerator:
    def __init__(self, data):
        self.__data = data
        self.__temperature_unit = 'C'

    def generate(self, report_type):
        if report_type == Reports.SHOW_EXTREMES:
            self.__show_extreme_stats()
        elif report_type == Reports.SHOW_MEANS:
            self.__show_mean_stats()
        elif report_type == Reports.SHOW_GRAPHS:
            self.__show_graphs()

        print('-' * 15)

    def __show_extreme_stats(self):

        max_temperature = self.__data.max_temperature_reading.max_temperature
        min_temperature = self.__data.min_temperature_reading.min_temperature
        max_humidity = self.__data.max_humidity_reading.max_humidity

        max_temperature_date = self.__data.max_temperature_reading.reading_date
        min_temperature_date = self.__data.min_temperature_reading.reading_date
        max_humidity_date = self.__data.max_humidity_reading.reading_date

        print(f"Highest: {max_temperature}{self.__temperature_unit} on {format_date(max_temperature_date)}")
        print(f"Lowest: {min_temperature}{self.__temperature_unit} on {format_date(min_temperature_date)}")
        print(f"Humidity: {max_humidity}% on {format_date(max_humidity_date)}")

    def __show_mean_stats(self):
        print(f"Average Max Temperature: {round_float(self.__data.average_max_temperature)}{self.__temperature_unit}")
        print(f"Average Min Temperature: {round_float(self.__data.average_min_temperature)}{self.__temperature_unit}")
        print(f"Average Mean Humidity: {round_float(self.__data.average_mean_humidity)}%")

    def __show_graphs(self):
        if len(self.__data) == 0:
            print('No data found for generating graphs')
            return

        print(f'{self.__data[0].reading_date.strftime("%B, %Y")}')

        for data in self.__data:
            print(draw_bar_graph(data.reading_date.strftime('%d'),
                                 abs(data.max_temperature),
                                 abs(data.min_temperature),
                                 Colors.BLUE.value,
                                 Colors.RED.value, self.__temperature_unit))
