from weather_analyzer import WeatherAnalyzer
import calendar
from color_codes import ColorCode


class WeatherReporter:

    def __init__(self):
        self.weather_analyzer_obj = WeatherAnalyzer()

    def read_files(self, files_path):
        self.weather_analyzer_obj.read_files(files_path)

    def genrate_year_report(self, given_arg_list):
        self.weather_analyzer_obj.read_files(given_arg_list[2])
        max_data_list = self.weather_analyzer_obj.extract_year_data(
            given_arg_list[1])
        self.print_year_temp_report(max_data_list)

    def genrate_month_report(self, given_arg_list):
        self.weather_analyzer_obj.read_files(given_arg_list[2])
        avg_data_list = self.weather_analyzer_obj.extract_month_data(
            given_arg_list[1])
        self.print_month_temp_report(avg_data_list)

    def genrate_barchart_report(self, given_arg_list):
        self.weather_analyzer_obj.read_files(given_arg_list[2])
        barchart_data_list = self.weather_analyzer_obj.calc_month_chart(
            given_arg_list[1])
        self.print_month_chart(barchart_data_list)
        print("\nBonus\n")
        bonus_barchart_data_list = self.weather_analyzer_obj.calc_bonus_chart(
            given_arg_list[1])
        self.print_bonus_chart(bonus_barchart_data_list)

    def print_bonus_chart(self, barchart_data_list):
        for data_list in barchart_data_list:
            self.draw_bonus_barchart(data_list[0], data_list[1], data_list[2],
                                     data_list[3], data_list[4])
            print("")

    def print_month_chart(self, barchart_data_list):
        for data_list in barchart_data_list:
            self.draw_barchart(data_list[0], data_list[1], data_list[2])

    def draw_barchart(self, temp, temp_color_code, day_num):
        """ draw bar chart """
        counter = 0
        barchart_month = self.weather_analyzer_obj.calc_barchart(temp)
        print(ColorCode.GREY.value + (str(day_num)) +
              " " + (temp_color_code + barchart_month) +
              " " + (ColorCode.GREY.value + str(temp) + "C"))

    def draw_bonus_barchart(self, day_num, barchart_min_temp,
                            barchart_max_temp,
                            temp_min, temp_max):
        print((ColorCode.GREY.value + str(day_num)) +
              " " + barchart_min_temp + barchart_max_temp +
              " " + (ColorCode.GREY.value + str(temp_min) + "C-") +
              (ColorCode.GREY.value + str(temp_max) + "C"))

    def print_year_temp_report(self, max_data_list):
        max_temp_date = max_data_list[0].pkt.split("-")
        min_temp_date = max_data_list[1].pkt.split("-")
        max_humidity_date = max_data_list[2].pkt.split("-")
        print("Highest: " + max_data_list[0].max_temperaturec +
              "C on " + calendar.month_name[int(max_temp_date[1])] +
              " " + str(max_temp_date[2]))
        print("Lowest: " + max_data_list[1].min_temperaturec +
              "C on " + calendar.month_name[int(min_temp_date[1])] +
              " " + str(min_temp_date[2]))
        print("Humid: " + max_data_list[2].max_humidity +
              "% on " + calendar.month_name[int(max_humidity_date[1])] +
              " " + str(max_humidity_date[2]))

    def print_month_temp_report(self, avg_data_list):
        print("Highest Average: " +
              str(avg_data_list[0]) +
              "C")
        print("Lowest Average: " +
              str(avg_data_list[1]) +
              "C")
        print("Average Humidity: " +
              str(avg_data_list[2]) +
              "%")
