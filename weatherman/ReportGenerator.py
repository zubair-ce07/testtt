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
        print("Highest: "+str(max_temperature.max_temperature)+"C on " +
              max_temperature.pkt.strftime("%d %b"))
        print("Lowest: "+str(min_temperature.min_temperature)+"C on " +
              min_temperature.pkt.strftime("%d %b"))
        print("Humidity: "+str(max_humidity.max_humidity)+"% on " +
              max_humidity.pkt.strftime("%d %b"))
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
        print("Highest Average: "+str(mean_max_temperature)+"C")
        print("Lowest Average: "+str(mean_min_temperature)+"C")
        print("Average Mean Humidity: "+str(mean_humidity)+"%")
        print("\n")

    def draw_bar_charts(self):
        print(self.weather_data_obj.month+" "+self.weather_data_obj.year)
        for row in self.weather_data_obj.weather_readings:
            if row.max_temperature and row.min_temperature:
                day = row.pkt.strftime("%d")
                highest = "\033[0;34;50m" + ("+" * row.max_temperature)
                lowest = "\033[0;31;50m" + ("+" * row.min_temperature)
                print(f"\033[0;30;50m{day} {highest}\033[0;30;50m{row.max_temperature}C")
                print(f"\033[0;30;50m{day} {lowest}\033[0;30;50m{row.min_temperature}C")

        print("\n")

    def draw_single_chart(self):
        print(self.weather_data_obj.month+" "+self.weather_data_obj.year)
        for row in self.weather_data_obj.weather_readings:
            if row.max_temperature and row.min_temperature:
                day = row.pkt.strftime("%d")
                highest = "\033[0;34;50m"+("+" * row.max_temperature if row.max_temperature > 0
                                           else "-" * row.max_temperature)
                lowest = "\033[0;31;50m"+("+" * row.min_temperature if row.min_temperature > 0
                                          else "-" * row.min_temperature)
                print(f"\033[0;30;50m{day} {lowest}{highest}\033[0;30;50m"
                      f"{row.min_temperature}C {row.max_temperature}C")
        print("\n")
