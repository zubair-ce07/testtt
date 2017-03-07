from termcolor import colored


class ChartReports:
    def __init__(self):
        pass

    PKT = 'PKT'
    MAX_TEMPERATURE = 'Max TemperatureC'
    MIN_TEMPERATURE = 'Min TemperatureC'
    MAX_TEMPERATURE_COLOR = 'red'
    MIN_TEMPERATURE_COLOR = 'blue'

    @staticmethod
    def color_bar_chart(temperature, color):
        bar_chart = ""
        for index in range(temperature):
            bar_chart += colored('+', color)
        return bar_chart

    @staticmethod
    def display_bar_chart(current_day, temperature, color):
        bar_chart = ""
        bar_chart += str(current_day) + " "
        bar_chart += ChartReports.color_bar_chart(temperature, color)
        bar_chart += " " + str(temperature) + "C"
        print bar_chart

    @staticmethod
    def daily_bar_chart(
            current_day, highest_temperature, lowest_temperature):
        ChartReports.display_bar_chart(
            current_day, highest_temperature, ChartReports.MAX_TEMPERATURE_COLOR)
        ChartReports.display_bar_chart(
            current_day, lowest_temperature, ChartReports.MIN_TEMPERATURE_COLOR)

    @staticmethod
    def daily_stacked_bar_chart(
            current_day, highest_temperature, lowest_temperature):
        stacked_bar_chart = ""
        stacked_bar_chart += str(current_day) + " "
        stacked_bar_chart += ChartReports.color_bar_chart(
            lowest_temperature, ChartReports.MIN_TEMPERATURE_COLOR)
        stacked_bar_chart += ChartReports.color_bar_chart(
            highest_temperature, ChartReports.MAX_TEMPERATURE_COLOR)
        stacked_bar_chart += " " + str(lowest_temperature) + "C - "
        stacked_bar_chart += str(highest_temperature) + "C"
        print stacked_bar_chart

    # Method to draw horizontal bar chart on the console for the highest
    # And lowest temperature on each day
    @staticmethod
    def display_monthly_report(weather_records, is_bonus_task):

        for single_day in weather_records:
            current_date = single_day[ChartReports.PKT]
            highest_temperature = single_day[ChartReports.MAX_TEMPERATURE]
            lowest_temperature = single_day[ChartReports.MIN_TEMPERATURE]
            if is_bonus_task:
                ChartReports.daily_stacked_bar_chart(
                    current_date.day, highest_temperature, lowest_temperature)
            else:
                ChartReports.daily_bar_chart(
                    current_date.day, highest_temperature, lowest_temperature)
