"""Weather Data holder Module.

This module has a class that has all the attribute to hold weather data
"""


class WeatherData:
    """Weather Data holder.

    This class has all the attribute to hold weather data
    """

    def __init__(self):
        """Weather_data object initilizer.

        it initialize all weather data attributes
        """
        self.max_temperatures = []
        self.low_temperatures = []
        self.max_humidities = []
        self.average_humidities = []
        self.weather_data_dates = []
