#!/usr/bin/python3
from datetime import datetime

class WeatherRecords:

    def __init__(self, day_weather):
        self.date = datetime.strptime(day_weather['PKT'], "%Y-%m-%d")
        self.min_temprature = int(day_weather['Min TemperatureC'])
        self.max_temprature = int(day_weather['Max TemperatureC'])
        self.mean_humidity = int(day_weather[' Mean Humidity'])
        self.max_humidity = int(day_weather['Max Humidity'])
