from datetime import datetime
from Calculator import *


class ReportGenerator:

    def __init__(self, weather_data_obj):
        self.weather_data_obj = weather_data_obj

    def year_report(self):
        high_temp = maximum_value(
            (i for i in self.weather_data_obj.weather_readings if i.max_temperature),
            key=lambda j: j.max_temperature
        )
        low_temp = minimum_value(
            (i for i in self.weather_data_obj.weather_readings if i.min_temperature),
            key=lambda j: j.min_temperature
        )
        humidity = maximum_value(
            (i for i in self.weather_data_obj.weather_readings if i.max_humidity),
            key=lambda j: j.max_humidity
        )
        print("Highest: "+str(high_temp.max_temperature)+"C on " +
              high_temp.pkt.strftime("%d %b"))
        print("Lowest: "+str(low_temp.min_temperature)+"C on " +
              low_temp.pkt.strftime("%d %b"))
        print("Humidity: "+str(humidity.max_humidity)+"% on " +
              humidity.pkt.strftime("%d %b"))
        print("\n")

    def month_report(self):
        high_temp = mean_value(
            self.weather_data_obj.weather_readings,
            key=lambda j: j.max_temperature
        )
        low_temp = mean_value(
            self.weather_data_obj.weather_readings,
            key=lambda j: j.min_temperature
        )
        humidity = mean_value(
            self.weather_data_obj.weather_readings,
            key=lambda j: j.mean_humidity
        )
        print("Highest Average: "+str(high_temp)+"C")
        print("Lowest Average: "+str(low_temp)+"C")
        print("Average Mean Humidity: "+str(humidity)+"%")
        print("\n")

    def draw_bar_charts(self):
        print(self.weather_data_obj.month+" "+self.weather_data_obj.year)
        for i in self.weather_data_obj.weather_readings:
            if i.max_temperature and i.min_temperature:
                day = i.pkt.strftime("%d")
                highest = "\033[0;34;50m" + ("+" * i.max_temperature)
                lowest = "\033[0;31;50m" + ("+" * i.min_temperature)
                print("\033[0;30;50m"+day+" "+highest+"\033[0;30;50m"+str(i.max_temperature)+"C")
                print("\033[0;30;50m"+day+" "+lowest+"\033[0;30;50m"+str(i.min_temperature)+"C")

        print("\n")

    def draw_single_chart(self):
        print(self.weather_data_obj.month+" "+self.weather_data_obj.year)
        for i in self.weather_data_obj.weather_readings:
            if i.max_temperature and i.min_temperature:
                day = i.pkt.strftime("%d")
                highest = "\033[0;34;50m"+"+" * i.max_temperature
                lowest = "\033[0;31;50m"+"+" * i.min_temperature
                print("\033[0;30;50m"+day+" "+lowest+highest+"\033[0;30;50m" +
                      str(i.min_temperature)+"C"+" "+str(i.max_temperature)+"C")
        print("\n")

    def change_weather_data(self, weather_data_obj):
        self.weather_data_obj = weather_data_obj
