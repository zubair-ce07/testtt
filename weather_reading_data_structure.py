from typing import List


class WeatherReading:
    def __init__(self,
                 date,
                 max_temperature,
                 mean_temperature,
                 min_temperature,
                 max_humidity,
                 mean_humidity,
                 min_humidity):
        self.date = date
        self.max_temperature = max_temperature
        self.mean_temperature = mean_temperature
        self.min_temperature = min_temperature
        self.mean_humidity = mean_humidity
        self.max_humidity = max_humidity
        self.min_humidity = min_humidity
