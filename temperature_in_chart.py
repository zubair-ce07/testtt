"""
this module displays monthly temperature of a month in a bar chart
"""
from calendar import month_abbr, month_name
import glob
from csv_hanlder import WeatherCsvHandler
from utils import weather_data


class TemperatureInChart:
    """
        this class displays weather data in chart
    """

    def __init__(self, two_line_chart=False, one_line_chart=False):
        self.two_line_chart = two_line_chart
        self.one_line_chart = one_line_chart

    def display_two_line_chart(self):
        """
        displays the daily temperture of a month
        :return:
        """
        for daily_weather in weather_data:
            day = daily_weather.date.split("-")[2]
            if daily_weather.max_temperature:
                max_temp = int(daily_weather.max_temperature)
                max_temp_string = "+" * max_temp
                print("%s \033[0;31m%s\033[0;m %dC" % (day, max_temp_string, max_temp))
            if daily_weather.min_temperature:
                min_temp = int(daily_weather.min_temperature)
                min_temp_string = "-" * min_temp
                print("%s \033[0;34m%s\033[0;m %dC" % (day, min_temp_string, min_temp))

    def display_one_line_chart(self):
        """
        display horizontally the temperatures of the month
        :return:
        """
        for daily_weather in weather_data:
            max_temp_flag = False
            min_temp_flag = False
            max_temp_string = ""
            min_temp_string = ""
            max_temp = 0
            min_temp = 0
            day = daily_weather.date.split("-")[2]
            if daily_weather.max_temperature:
                max_temp = int(daily_weather.max_temperature)

                max_temp_flag = True
                max_temp_string = "+" * max_temp
            if daily_weather.min_temperature:
                min_temp = int(daily_weather.min_temperature)

                min_temp_flag = True
                min_temp_string = '-' * min_temp
            if max_temp_flag or min_temp_flag:
                print("%s \033[0;34m%s\033[0;m\033[0;31m%s\033[0;m  %dC - %dC"
                      % (day, min_temp_string, max_temp_string,
                         min_temp, max_temp))

    def display_temperature_in_chart(self, date_str, dir_path):
        """
        this method displays emperature in chart according to type
        :param date_str:
        :param dir_path:
        :return:
        """
        (year, month) = date_str.split('/')
        month = int(month)
        file_path = glob.glob(dir_path + "/*_" + year + "_" + month_abbr[month] + "*")
        if file_path:
            file_path = file_path[0]
            if not weather_data:
                csv_handler = WeatherCsvHandler(file_path)
                csv_handler.read_csv_and_fill_data()
            print("%s %s" % (month_name[month], year))
            if self.two_line_chart:
                self.display_two_line_chart()
            elif self.one_line_chart:
                self.display_one_line_chart()
        else:
            print("No Data Found for the Specified Month")
