"""This class is to get requried attributes for generating weather reports."""


class WeatherAttributes:
    def __init__(self, **kwargs):
        self.date = str(kwargs.get('PKT', kwargs.get('PKST')))
        self.max_temp_date = str(kwargs.get('PKT', kwargs.get('PKST')))
        self.min_temp_date = str(kwargs.get('PKT', kwargs.get('PKST')))
        self.max_humidity_date = str(kwargs.get('PKT', kwargs.get('PKST')))
        self.max_temp = str(kwargs.get('Max TemperatureC'))
        self.min_temp = str(kwargs.get('Min TemperatureC'))
        self.max_humidity = str(kwargs.get('Max Humidity'))
        self.mean_humidity = str(kwargs.get(' Mean Humidity'))
