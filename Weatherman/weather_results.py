#!/usr/bin/python3
from datetime import datetime

class WeatherResults:
    def __init__(self, results):

        self.max_temprature = results.get('max_temprature', 0)
        self.min_temprature = results.get('min_temprature', 0)
        self.max_humidity = results.get('max_humidity', 0)
        self.highest_avg_temp = results.get('highest_avg_temp', 0)
        self.lowest_avg_temp = results.get('lowest_avg_temp', 0)
        self.avg_mean_humidity = results.get('avg_mean_humidity', 0)
