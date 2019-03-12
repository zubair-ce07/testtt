"""This class is to get requried attributes for generating weather reports."""
from datetime import datetime


class WeatherAttributes:
    def __init__(self, **kwargs):
        if (kwargs and kwargs.get('Max TemperatureC') != "" and kwargs.get('Min TemperatureC') != "" and
                kwargs.get('Max Humidity') != "" and kwargs.get(' Mean Humidity') != ""):
            self.date = datetime.strptime(kwargs.get('PKT', kwargs.get('PKST')), '%Y-%m-%d')
            self.max_temp_date = datetime.strptime(kwargs.get('PKT', kwargs.get('PKST')), '%Y-%m-%d')
            self.min_temp_date = datetime.strptime(kwargs.get('PKT', kwargs.get('PKST')), '%Y-%m-%d')
            self.max_humidity_date = datetime.strptime(kwargs.get('PKT', kwargs.get('PKST')), '%Y-%m-%d')
            self.max_temp = int(kwargs.get('Max TemperatureC'))
            self.min_temp = int(kwargs.get('Min TemperatureC'))
            self.max_humidity = int(kwargs.get('Max Humidity'))
            self.mean_humidity = int(kwargs.get(' Mean Humidity'))

