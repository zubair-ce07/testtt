from datetime import datetime
import Calculator


class ReportGenerator:

    def __init__(self, weather_data_obj):
        self.weather_data_obj = weather_data_obj

    def year_report(self):
        high_temp = Calculator.maximum_value(
            (i for i in self.weather_data_obj.all_data_obj if i.max_temperature),
            key=lambda j: j.max_temperature
        )
        low_temp = Calculator.minimum_value(
            (i for i in self.weather_data_obj.all_data_obj if i.min_temperature),
            key=lambda j: j.min_temperature
        )
        humidity = Calculator.maximum_value(
            (i for i in self.weather_data_obj.all_data_obj if i.max_humidity),
            key=lambda j: j.max_humidity
        )
        print("Highest: "+str(high_temp.max_temperature)+"C on " +
              datetime.strptime(high_temp.pkt, '%Y-%m-%d').strftime("%d %b"))
        print("Lowest: "+str(low_temp.min_temperature)+"C on " +
              datetime.strptime(low_temp.pkt, '%Y-%m-%d').strftime("%d %b"))
        print("Humidity: "+str(humidity.max_humidity)+"% on " +
              datetime.strptime(humidity.pkt, '%Y-%m-%d').strftime("%d %b"))
        print("\n")

    def month_report(self):
        high_temp = Calculator.mean_value(
            self.weather_data_obj.all_data_obj,
            key=lambda j: j.max_temperature
        )
        low_temp = Calculator.mean_value(
            self.weather_data_obj.all_data_obj,
            key=lambda j: j.min_temperature
        )
        humidity = Calculator.mean_value(
            self.weather_data_obj.all_data_obj,
            key=lambda j: j.mean_humidity
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
