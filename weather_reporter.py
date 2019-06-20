import calendar

from weather_analyzer import WeatherAnalyzer


class WeatherReporter:

    def __init__(self):
        self.red_color_code = '\033[31m'
        self.blue_color_code = '\033[34m'
        self.grey_color_code = '\033[37m'
        self.weather_analyzer = WeatherAnalyzer()

    def generate_annual_report(self, report_year, dir_path):
        weather_results = self.weather_analyzer.get_weather_results(dir_path, int(report_year))
        self.print_annual_report(weather_results)

    def generate_monthly_report(self, report_year, report_month, dir_path):
        weather_results = self.weather_analyzer.get_weather_results(dir_path, report_year, report_month)
        self.print_monthly_report(weather_results)

    def generate_bar_chart(self, report_year, report_month, dir_path):
        weather_results = self.weather_analyzer.get_weather_results(dir_path, report_year, report_month)
        bar_chart = self.calculate_bar_chart(weather_results)
        self.print_monthly_bar_chart(bar_chart)
        print("\nBonus\n")
        bonus_bar_chart = self.calculate_bonus_chart(weather_results)
        self.print_bonus_chart(bonus_bar_chart)

    def calculate_bar_chart(self, month_weather_record):
        bar_chart = []
        day_num = 1
        for daily_reading in month_weather_record.daily_reading:
            if daily_reading.max_temperature:
                bar_chart.append([int(daily_reading.max_temperature), self.red_color_code, day_num])
            if daily_reading.min_temperature:
                bar_chart.append([int(daily_reading.min_temperature), self.blue_color_code, day_num])
                day_num += 1
        return bar_chart

    def calculate_bonus_chart(self, month_weather_record):
        bonus_bar_chart = []
        day_num = 1
        for day_weather_record in month_weather_record.daily_reading:
            if day_weather_record.max_temperature:
                temp_max = int(day_weather_record.max_temperature)
                bar_chart_max_temp = self.red_color_code + ('+' * temp_max)
            if day_weather_record.min_temperature:
                temp_min = int(day_weather_record.min_temperature)
                bar_chart_min_temp = self.blue_color_code + ('+' * temp_min)
                bonus_bar_chart.append([day_num, bar_chart_min_temp, bar_chart_max_temp,
                                       temp_min, temp_max])
            day_num += 1
        return bonus_bar_chart

    def print_bonus_chart(self, bonus_bar_chart):
        for bar_chart_row in bonus_bar_chart:
            self.draw_bonus_bar_chart(bar_chart_row[0], bar_chart_row[1], bar_chart_row[2],
                                      bar_chart_row[3], bar_chart_row[4])

    def print_monthly_bar_chart(self, bar_chart):
        for bar_chart_row_ in bar_chart:
            self.draw_bar_chart(bar_chart_row_[0], bar_chart_row_[1], bar_chart_row_[2])

    def draw_bar_chart(self, temp, temp_color_code, day_num):
        bar_chart_month = '+' * temp
        print(f"{self.grey_color_code}{day_num}{temp_color_code} "
              f"{bar_chart_month}{self.grey_color_code}{temp}C")

    def draw_bonus_bar_chart(self, day_num, bar_chart_min_temp, bar_chart_max_temp, temp_min,
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
        print(f"Highest Average: {round(weather_results.avg_max_temp)}C")
        print(f"Lowest Average: {round(weather_results.avg_min_temp)}C")
        print(f"Average Mean Humidity: {round(weather_results.mean_humidity_avg)}%")
