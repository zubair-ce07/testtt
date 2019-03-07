"""
This module structures weather data into requried attributes
for generating reports.
"""


class Weather:
    def __init__(self, **kwargs):
        self.date = kwargs.get('PKT', kwargs.get('PKST'))
        self.max_temp = kwargs.get('Max TemperatureC')
        self.min_temp = kwargs.get('Min TemperatureC')
        self.max_humidity = kwargs.get('Max Humidity')
        self.min_humidity = kwargs.get(' Min Humidity')
