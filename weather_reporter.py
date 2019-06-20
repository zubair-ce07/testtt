import calendar

from weather_analyzer import WeatherAnalyzer


class WeatherReporter:

    def __init__(self):
        self.red_color_template = '\033[31m{}'
        self.blue_color_template = "\033[34m{}"
        self.weather_analyzer = WeatherAnalyzer()

    def generate_annual_report(self, report_year, dir_path):
        weather_results = self.weather_analyzer.get_results(dir_path, report_year)
        self.print_annual_report(weather_results)

    def generate_monthly_report(self, report_year, report_month, dir_path):
        weather_results = self.weather_analyzer.get_results(dir_path, report_year, report_month)
        self.print_monthly_report(weather_results)

    def generate_bar_chart(self, report_year, report_month, dir_path):
        weather_results = self.weather_analyzer.get_results(dir_path, report_year, report_month)
        self.print_monthly_bar_chart(weather_results)
        self.print_bonus_chart(weather_results)

    def print_monthly_bar_chart(self, weather_results):
        for day_num, weather_reading in enumerate(weather_results.daily_reading):
            self.draw_bar_chart(weather_reading.min_temperature, self.blue_color_template, day_num)
            self.draw_bar_chart(weather_reading.max_temperature, self.red_color_template, day_num)

    def draw_bar_chart(self, temp, temp_color_code, day_num):
        print(f"{day_num}{temp_color_code.format('+' * temp)}{temp}C")

    def print_bonus_chart(self, weather_results):
        print("\nBonus\n")
        for day_num, weather_reading in enumerate(weather_results.daily_reading):
            max_temp = weather_reading.max_temperature
            min_temp = weather_reading.min_temperature
            self.draw_bonus_bar_chart(day_num, max_temp, min_temp)

    def draw_bonus_bar_chart(self, day_num, temp_min, temp_max):
        print(f"{day_num}{self.blue_color_template.format('+' * temp_min)}"
              f"{self.red_color_template.format('+' * temp_max)}{temp_min}C-{temp_max}C")

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
