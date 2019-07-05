from Calculator import *


class ReportGenerator:

    def __init__(self, weather_data_obj):
        self.weather_data_obj = weather_data_obj

    def year_report(self):
        max_temperature = maximum_value(
            self.weather_data_obj.weather_readings,
            key=lambda row: row.max_temperature
        )
        min_temperature = minimum_value(
            self.weather_data_obj.weather_readings,
            key=lambda row: row.min_temperature
        )
        max_humidity = maximum_value(
            self.weather_data_obj.weather_readings,
            key=lambda row: row.max_humidity
        )
        print(f"Highest: {max_temperature.max_temperature}C on {max_temperature.pkt.strftime('%d %b')}")
        print(f"Lowest: {min_temperature.min_temperature}C on {min_temperature.pkt.strftime('%d %b')}")
        print(f"Humidity: {max_humidity.max_humidity}% on {max_humidity.pkt.strftime('%d %b')}")
        print("\n")

    def month_report(self):
        mean_max_temperature = mean_value(
            self.weather_data_obj.weather_readings,
            key=lambda row: row.max_temperature
        )
        mean_min_temperature = mean_value(
            self.weather_data_obj.weather_readings,
            key=lambda row: row.min_temperature
        )
        mean_humidity = mean_value(
            self.weather_data_obj.weather_readings,
            key=lambda row: row.mean_humidity
        )
        print(f"Highest Average: {mean_max_temperature: .2f}C")
        print(f"Lowest Average: {mean_min_temperature: .2f}C")
        print(f"Average Mean Humidity: {mean_humidity: .2f}%")

    def draw_bar_charts(self):
        print(f"{self.weather_data_obj.month} {self.weather_data_obj.year}")
        for row in self.weather_data_obj.weather_readings:
            if row.max_temperature and row.min_temperature:
                day = row.pkt.strftime("%d")
                highest = f"\033[0;31;50m{'+' * row.max_temperature if row.max_temperature > 0 else '-' * row.max_temperature}"
                lowest = f"\033[0;34;50m{'+' * row.min_temperature if row.min_temperature > 0 else '-' * row.min_temperature}"
                print(f"\033[0;30;50m{day} {highest}\033[0;30;50m{row.max_temperature}C")
                print(f"\033[0;30;50m{day} {lowest}\033[0;30;50m{row.min_temperature}C")

    def draw_single_chart(self):
        print(f"{self.weather_data_obj.month} {self.weather_data_obj.year}")
        for row in self.weather_data_obj.weather_readings:
            if row.max_temperature and row.min_temperature:
                day = row.pkt.strftime("%d")
                highest = f"\033[0;31;50m{'+' * row.max_temperature if row.max_temperature > 0 else '-' * row.max_temperature}"
                lowest = f"\033[0;34;50m{'+' * row.min_temperature if row.min_temperature > 0 else '-' * row.min_temperature}"
                print(f"\033[0;30;50m{day} {lowest}{highest}\033[0;30;50m"
                      f"{row.min_temperature}C {row.max_temperature}C")
