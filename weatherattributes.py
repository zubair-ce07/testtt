"""This class is to get requried attributes for generating weather reports."""


class WeatherAttributes:
    def __init__(self, **kwargs):

        self.date = str(kwargs.get('PKT', kwargs.get('PKST')))
        self.max_temp_date = str(kwargs.get('PKT', kwargs.get('PKST')))
        self.min_temp_date = str(kwargs.get('PKT', kwargs.get('PKST')))
        self.max_humidity_date = str(kwargs.get('PKT', kwargs.get('PKST')))

        if kwargs and kwargs.get('Max TemperatureC') != "":
            self.max_temp = int(kwargs.get('Max TemperatureC'))
        else:
            self.max_temp = 200  # Dump value to avoid exception incase of empty max Temperature.

        if kwargs and kwargs.get('Min TemperatureC') != "":
            self.min_temp = int(kwargs.get('Min TemperatureC'))
        else:
            self.min_temp = 200  # Dump value to avoid exception incase of empty min Temperature.

        if kwargs and kwargs.get('Max Humidity') != "":
            self.max_humidity = int(kwargs.get('Max Humidity'))
        else:
            self.max_humidity = 200  # Dump value to avoid exception incase of empty max humidity.

        if kwargs and kwargs.get(' Mean Humidity') != "":
            self.mean_humidity = int(kwargs.get(' Mean Humidity'))
        else:
            self.mean_humidity = 200  # Dump value to avoid exception incase of empty mean humidity.
