import calendar

from weather_analyzer import WeatherAnalyzer


class WeatherReporter:

    def __init__(self):
        self.red_color_code = '\033[31m'
        self.blue_color_code = '\033[34m'
        self.grey_color_code = '\033[37m'
        self.weather_analyzer = WeatherAnalyzer()

    def generate_annual_report(self, report_year, dir_path):
        weather_results = self.weather_analyzer.get_weather_results(dir_path, report_year)
        self.print_annual_report(weather_results)

    def generate_monthly_report(self, report_year, report_month, dir_path):
        weather_results = self.weather_analyzer.get_weather_results(dir_path, report_year,
                                                                    report_month)
        self.print_monthly_report(weather_results)

    def generate_bar_chart(self, report_year, report_month, dir_path):
        weather_results = self.weather_analyzer.get_weather_results(dir_path, report_year,
                                                                    report_month)
        self.print_monthly_bar_chart(weather_results)
        self.print_bonus_chart(weather_results)

    def print_monthly_bar_chart(self, weather_results):
        day_num = 1
        for weather_reading in weather_results.daily_reading:
            if weather_reading.pkt:
                self.draw_bar_chart_row(weather_reading.min_temperature, self.blue_color_code,
                                        day_num)
                self.draw_bar_chart_row(weather_reading.max_temperature, self.red_color_code,
                                        day_num)

    def draw_bar_chart_row(self, temp, temp_color_code, day_num):
        bar_chart_month = '+' * temp
        print(f"{self.grey_color_code}{day_num}{temp_color_code} "
              f"{bar_chart_month}{self.grey_color_code}{temp}C")

    def print_bonus_chart(self, weather_results):
        print("\nBonus\n")
        day_num = 1
        for weather_reading in weather_results.daily_reading:
            if weather_reading.pkt:
                max_temp = weather_reading.max_temperature
                min_temp = weather_reading.min_temperature
                bar_chart_min_temp = self.blue_color_code + ('+' * min_temp)
                bar_chart_max_temp = self.red_color_code + ('+' * max_temp)
                self.draw_bonus_bar_chart_row(day_num, bar_chart_min_temp, bar_chart_max_temp,
                                              max_temp, min_temp)

    def draw_bonus_bar_chart_row(self, day_num, bar_chart_min_temp, bar_chart_max_temp, temp_min,
                                 temp_max):
        print(f"{self.grey_color_code}{day_num}{bar_chart_min_temp}"
              f"{bar_chart_max_temp}{self.grey_color_code}"
              f"{temp_min}C-{self.grey_color_code}{temp_max}C")

    def print_annual_report(self, weather_results):
        print(f"Highest: {weather_results.max_humidity_record.max_temperature}C on "
              f"{calendar.month_name[weather_results.max_humidity_record.pkt.month]} "
              f"{weather_results.max_humidity_record.pkt.day}")
        print(f"Lowest: {weather_results.min_temp_record.min_temperature}C on "
              f"{calendar.month_name[weather_results.min_temp_record.pkt.month]} "
              f"{weather_results.min_temp_record.pkt.day}")
        print(f"Humid: {weather_results.max_humidity_record.max_humidity}% on "
              f"{calendar.month_name[weather_results.max_humidity_record.pkt.month]} "
              f"{weather_results.max_humidity_record.pkt.day}")

    def print_monthly_report(self, weather_results):
        print(f"Highest Average: {weather_results.avg_max_temp}C")
        print(f"Lowest Average: {weather_results.avg_min_temp}C")
        print(f"Average Mean Humidity: {weather_results.mean_humidity_avg}%")
