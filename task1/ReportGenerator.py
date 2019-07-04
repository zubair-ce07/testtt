from datetime import datetime
from CalculationsResults import CalculationsResults


class ReportGenerator:
    calculations_object = CalculationsResults()

    def __init__(self, weather_data_obj):
        self.weather_data_obj = weather_data_obj

    def year_report(self):
        high_temp, high_temp_day = self.calculations_object.highest_temp_in_year(
            self.weather_data_obj
        )
        low_temp, low_temp_day = self.calculations_object.lowest_temp_in_year(
            self.weather_data_obj
        )
        humidity, humid_day = self.calculations_object.most_humid_day_of_year(
            self.weather_data_obj
        )
        print("Highest: "+str(high_temp)+"C on "+high_temp_day)
        print("Lowest: "+str(low_temp)+"C on "+low_temp_day)
        print("Humidity: "+str(humidity)+"% on "+humid_day)
        print("\n")

    def month_report(self):
        high_temp = self.calculations_object.avg_highest_temp(
            self.weather_data_obj
        )
        low_temp = self.calculations_object.avg_lowest_temp(
            self.weather_data_obj
        )
        humidity = self.calculations_object.avg_mean_humidity(
            self.weather_data_obj
        )
        print("Highest Average: "+str(high_temp)+"C")
        print("Lowest Average: "+str(low_temp)+"C")
        print("Average Mean Humidity: "+str(humidity)+"%")
        print("\n")

    def draw_bar_charts(self):
        print(self.weather_data_obj.month+" "+self.weather_data_obj.year)
        for i in self.weather_data_obj.all_data_obj:
            if i.max_temperature and i.min_temperature:
                day = datetime.strptime(i.pkt, '%Y-%m-%d').strftime("%d")
                highest = "\033[0;34;50m" + ("+" * i.max_temperature)
                lowest = "\033[0;31;50m" + ("+" * i.min_temperature)
                print("\033[0;30;50m"+day+" "+highest+"\033[0;30;50m"+str(i.max_temperature)+"C")
                print("\033[0;30;50m"+day+" "+lowest+"\033[0;30;50m"+str(i.min_temperature)+"C")

        print("\n")

    def draw_single_chart(self):
        print(self.weather_data_obj.month+" "+self.weather_data_obj.year)
        for i in self.weather_data_obj.all_data_obj:
            if i.max_temperature and i.min_temperature:
                day = datetime.strptime(i.pkt, '%Y-%m-%d').strftime("%d")
                highest = "\033[0;34;50m"+"+" * i.max_temperature
                lowest = "\033[0;31;50m"+"+" * i.min_temperature
                print("\033[0;30;50m"+day+" "+lowest+highest+"\033[0;30;50m" +
                      str(i.min_temperature)+"C"+" "+str(i.max_temperature)+"C")

        print("\n")

    def change_weather_data(self, weather_data_obj):
        self.weather_data_obj = weather_data_obj
