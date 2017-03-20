from termcolor import colored


class ChartReports:
    __MAX_TEMPERATURE_COLOR = 'red'
    __MIN_TEMPERATURE_COLOR = 'blue'

    @staticmethod
    def __color_bar_chart(temperature, color):
        bar_chart = ""
        for index in range(temperature):
            bar_chart += colored('+', color)
        return bar_chart

    @staticmethod
    def __display_bar_chart(current_day, temperature, color):
        bar_chart = ""
        bar_chart += str(current_day) + " "
        bar_chart += ChartReports.__color_bar_chart(temperature, color)
        bar_chart += " " + str(temperature) + "C"
        print bar_chart

    @staticmethod
    def daily_bar_chart(
            current_day, highest_temperature, lowest_temperature):
        ChartReports.__display_bar_chart(
            current_day, highest_temperature, ChartReports.__MAX_TEMPERATURE_COLOR)
        ChartReports.__display_bar_chart(
            current_day, lowest_temperature, ChartReports.__MIN_TEMPERATURE_COLOR)

    @staticmethod
    def daily_stacked_bar_chart(
            current_day, highest_temperature, lowest_temperature):
        stacked_bar_chart = ""
        stacked_bar_chart += str(current_day) + " "
        stacked_bar_chart += ChartReports.__color_bar_chart(
            lowest_temperature, ChartReports.__MIN_TEMPERATURE_COLOR)
        stacked_bar_chart += ChartReports.__color_bar_chart(
            highest_temperature, ChartReports.__MAX_TEMPERATURE_COLOR)
        stacked_bar_chart += " " + str(lowest_temperature) + "C - "
        stacked_bar_chart += str(highest_temperature) + "C"
        print stacked_bar_chart
