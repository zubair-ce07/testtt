#!/usr/bin/python3
from datetime import datetime

class WeatherResults:
    def __init__(self):

        self.date = datetime.strptime("2004-7-1", "%Y-%m-%d")
        self.max_temprature = 0
        self.min_temprature = 0
        self.most_humidity = 0
        self.highest_avg_temp = 0
        self.lowest_avg_temp = 0
        self.avg_mean_humidity = 0
