#!/usr/bin/python3
from datetime import datetime

class WeatherRecords:

    def __init__(self, day_weather):
        if day_weather['PKT']:
            self.date = datetime.strptime(day_weather['PKT'], "%Y-%m-%d")
        if day_weather['Min TemperatureC']:
            self.min_temprature = int(day_weather['Min TemperatureC'])
        if day_weather['Max TemperatureC']:
            self.max_temprature = int(day_weather['Max TemperatureC'])
        if day_weather[' Mean Humidity']:
            self.mean_humidity = int(day_weather[' Mean Humidity'])
        if day_weather['Max Humidity']:
            self.max_humidity = int(day_weather['Max Humidity'])

class WeatherResults:
    def __init__(self, day_weather={}):
        if (day_weather):
            if day_weather['date']:
                self.date = datetime.strptime(day_weather['PKT'], "%Y-%m-%d")
            if day_weather['highest_temp']:
                self.max_temprature = int(day_weather['highest_temp'])
            if day_weather['lowest_temp']:
                self.min_temprature = int(day_weather['lowest_temp'])
            if day_weather['most_humidity']:
                self.most_humidity = int(day_weather['most_humidity'])
            if day_weather['highest_avg_temp']:
                self.highest_avg_temp = int(day_weather['highest_avg_temp'])
            if day_weather['lowest_avg_temp']:
                self.lowest_avg_temp = int(day_weather['lowest_avg_temp'])
            if day_weather['avg_mean_humidity']:
                self.avg_mean_humidity = int(day_weather['avg_mean_humidity'])
