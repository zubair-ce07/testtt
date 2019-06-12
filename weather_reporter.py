import calendar

from color_codes import ColorCode
from weather_analyzer import WeatherAnalyzer


class WeatherReporter:

    def __init__(self):
        self.weather_analyzer = WeatherAnalyzer()

    def generate_year_report(self, report_year, dir_path):
        self.weather_analyzer.read_files(dir_path)
        temp_max_obj, temp_min_obj, \
            max_humid_obj = self.weather_analyzer.extract_year_data(
                report_year)
        self.print_year_temp_report(temp_max_obj, temp_min_obj, max_humid_obj)

    def generate_month_report(self, report_year, dir_path):
        self.weather_analyzer.read_files(dir_path)
        month_data_list = self.weather_analyzer.collect_month_data(
            report_year)
        max_temp_avg, min_temp_avg, \
            humidity_avg = self.weather_analyzer.compute_month_data_average(
                month_data_list)
        self.print_month_temp_report(max_temp_avg, min_temp_avg, humidity_avg)

    def generate_barchart_report(self, report_year, dir_path):
        self.weather_analyzer.read_files(dir_path)
        month_data_list = self.weather_analyzer.collect_month_data(
            report_year)
        barchart_data_list = self.calc_month_chart(month_data_list)
        self.print_month_chart(barchart_data_list)
        print("\nBonus\n")
        bonus_barchart_data_list = self.calc_bonus_chart(month_data_list)
        self.print_bonus_chart(bonus_barchart_data_list)

    def calc_month_chart(self, month_data_list):
        barchart_data_list = []
        day_num = 1
        for day_data in month_data_list:
            if day_data.max_temperature:
                barchart_data_list.append([int(day_data.max_temperature),
                                           ColorCode.RED.value, day_num])
            if day_data.min_temperature:
                barchart_data_list.append([int(day_data.min_temperature),
                                           ColorCode.BLUE.value, day_num])
                day_num += 1
        return barchart_data_list

    def calc_bonus_chart(self, month_data_list):
        barchart_data_list = []
        day_num = 1
        for day_data in month_data_list:
            if day_data.max_temperature:
                temp_max = int(day_data.max_temperature)
                barchart_max_temp = ColorCode.RED.value + ('+' * temp_max)
            if day_data.min_temperature:
                temp_min = int(day_data.min_temperature)
                barchart_min_temp = ColorCode.BLUE.value + ('+' * temp_min)
                barchart_data_list.append([day_num, barchart_min_temp,
                                           barchart_max_temp,
                                           temp_min, temp_max])
            day_num += 1
        return barchart_data_list

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
        barchart_month = '+' * temp
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

    def print_year_temp_report(self, temp_max_obj, temp_min_obj,
                               max_humid_obj):
        max_temp_date = temp_max_obj.pkt.split("-")
        min_temp_date = temp_min_obj.pkt.split("-")
        max_humidity_date = max_humid_obj.pkt.split("-")
        print("Highest: " + temp_max_obj.max_temperature +
              "C on " + calendar.month_name[int(max_temp_date[1])] +
              " " + str(max_temp_date[2]))
        print("Lowest: " + temp_min_obj.min_temperature +
              "C on " + calendar.month_name[int(min_temp_date[1])] +
              " " + str(min_temp_date[2]))
        print("Humid: " + max_humid_obj.max_humidity +
              "% on " + calendar.month_name[int(max_humidity_date[1])] +
              " " + str(max_humidity_date[2]))

    def print_month_temp_report(self, max_temp_avg, min_temp_avg,
                                humidity_avg):
        print("Highest Average: " +
              str(max_temp_avg) +
              "C")
        print("Lowest Average: " +
              str(min_temp_avg) +
              "C")
        print("Average Humidity: " +
              str(humidity_avg) +
              "%")
