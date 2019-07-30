#!/usr/bin/python3
from datetime import datetime

class WeatherResults:
    def __init__(self, max_temprature=0, \
                min_temprature=0, max_humidity=0, highest_avg_temp=0, \
                lowest_avg_temp=0, avg_mean_humidity=0):

        self.max_temprature = max_temprature
        self.min_temprature = min_temprature
        self.max_humidity = max_humidity
        self.highest_avg_temp = highest_avg_temp
        self.lowest_avg_temp = lowest_avg_temp
        self.avg_mean_humidity = avg_mean_humidity
