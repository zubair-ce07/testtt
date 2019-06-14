import calendar

from weather_analyzer import WeatherAnalyzer


class WeatherReporter:

    def __init__(self):
        self.red_color_code = '\033[31m'
        self.blue_color_code = '\033[34m'
        self.grey_color_code = '\033[37m'
        self.weather_analyzer = WeatherAnalyzer()

    def generate_year_report(self, report_year, dir_path):
        self.weather_analyzer.collect_data_set(dir_path)
        temp_max_obj, temp_min_obj, \
            max_humid_obj = self.weather_analyzer.extract_year_data(
             report_year)
        self.print_year_temp_report(temp_max_obj, temp_min_obj, max_humid_obj)

    def generate_month_report(self, report_year, dir_path):
        self.weather_analyzer.collect_data_set(dir_path)
        month_weather_record = self.weather_analyzer.collect_month_data(
            report_year)
        max_temp_avg, min_temp_avg, \
            humidity_avg = self.weather_analyzer.compute_month_data_average(
                month_weather_record)
        self.print_month_temp_report(round(max_temp_avg), round(min_temp_avg),
                                     round(humidity_avg))

    def generate_barchart_report(self, report_year, dir_path):
        self.weather_analyzer.collect_data_set(dir_path)
        month_data_record = self.weather_analyzer.collect_month_data(
            report_year)
        barchart_data = self.calc_month_chart(month_data_record)
        self.print_month_chart(barchart_data)
        print("\nBonus\n")
        bonus_barchart_data = self.calc_bonus_chart(month_data_record)
        self.print_bonus_chart(bonus_barchart_data)

    def calc_month_chart(self, month_data_record):
        barchart_data = []
        day_num = 1
        for day_data in month_data_record:
            if day_data.max_temperature:
                barchart_data.append([int(day_data.max_temperature),
                                      self.red_color_code, day_num])
            if day_data.min_temperature:
                barchart_data.append([int(day_data.min_temperature),
                                      self.blue_color_code, day_num])
                day_num += 1
        return barchart_data

    def calc_bonus_chart(self, month_data_record):
        bonus_barchart_data = []
        day_num = 1
        for day_data in month_data_record:
            if day_data.max_temperature:
                temp_max = int(day_data.max_temperature)
                barchart_max_temp = self.red_color_code + ('+' * temp_max)
            if day_data.min_temperature:
                temp_min = int(day_data.min_temperature)
                barchart_min_temp = self.blue_color_code + ('+' * temp_min)
                bonus_barchart_data.append([day_num, barchart_min_temp,
                                            barchart_max_temp,
                                            temp_min, temp_max])
            day_num += 1
        return bonus_barchart_data

    def print_bonus_chart(self, bonus_barchart_data):
        for barchart_row in bonus_barchart_data:
            self.draw_bonus_barchart(barchart_row[0], barchart_row[1],
                                     barchart_row[2],
                                     barchart_row[3], barchart_row[4])
            print("")

    def print_month_chart(self, barchart_data):
        for barchart_row in barchart_data:
            self.draw_barchart(barchart_row[0], barchart_row[1],
                               barchart_row[2])

    def draw_barchart(self, temp, temp_color_code, day_num):
        """ draw bar chart """
        barchart_month = '+' * temp
        print(f"{self.grey_color_code}{day_num}{temp_color_code} "
              f"{barchart_month}{self.grey_color_code}{temp}C")

    def draw_bonus_barchart(self, day_num, barchart_min_temp,
                            barchart_max_temp,
                            temp_min, temp_max):
        print(f"{self.grey_color_code}{day_num}{barchart_min_temp}"
              f"{barchart_max_temp}{self.grey_color_code}"
              f"{temp_min}C-{self.grey_color_code}{temp_max}C")

    def print_year_temp_report(self, temp_max_obj, temp_min_obj,
                               max_humid_obj):
        max_temp_date = temp_max_obj.pkt.split("-")
        min_temp_date = temp_min_obj.pkt.split("-")
        max_humidity_date = max_humid_obj.pkt.split("-")
        print(f"Highest: {temp_max_obj.max_temperature}C on "
              f"{calendar.month_name[int(max_temp_date[1])]} "
              f"{max_temp_date[2]}")
        print(f"Lowest: {temp_min_obj.min_temperature}C on "
              f"{calendar.month_name[int(min_temp_date[1])]} "
              f"{min_temp_date[2]}")
        print(f"Humid: {max_humid_obj.max_humidity}% on "
              f"{calendar.month_name[int(max_humidity_date[1])]} "
              f"{max_humidity_date[2]}")
        print("")

    def print_month_temp_report(self, max_temp_avg, min_temp_avg,
                                humidity_avg):
        print(f"Highest Average: {max_temp_avg}C")
        print(f"Lowest Average: {min_temp_avg}C")
        print(f"Average Mean Humidity: {humidity_avg}%")
        print("")
