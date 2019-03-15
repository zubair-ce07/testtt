"""This class is to get requried attributes for generating weather reports."""


class WeatherAttributes:
    def __init__(self, **kwargs):
        self.date = kwargs.get('date')
        self.max_temp = kwargs.get('max_temp')
        self.min_temp = kwargs.get('min_temp')
        self.max_humidity = kwargs.get('max_humidity')
        self.mean_humidity = kwargs.get('mean_humidity')

