#!/usr/bin/python3
from datetime import datetime

class WeatherResults:
    def __init__(self, day_weather={}):

        if (day_weather):
            self.date = datetime.strptime(day_weather['PKT'], "%Y-%m-%d")
            self.max_temprature = int(day_weather['highest_temp'])
            self.min_temprature = int(day_weather['lowest_temp'])
            self.most_humidity = int(day_weather['most_humidity'])
            self.highest_avg_temp = int(day_weather['highest_avg_temp'])
            self.lowest_avg_temp = int(day_weather['lowest_avg_temp'])
            self.avg_mean_humidity = int(day_weather['avg_mean_humidity'])
