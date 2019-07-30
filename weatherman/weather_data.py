"""Weather Data holder Module.

This module has a class that has all the attribute to hold weather data
"""
from datetime import datetime


class WeatherData:
    """Weather Data holder.

    This class has all the attribute to hold weather data
    """

    def __init__(self):
        """Weather_data object initilizer.

        it initialize all weather data attributes
        """
        self.max_temperature = ''
        self.low_temperature = ''
        self.max_humidity = ''
        self.average_humidity = ''
        self.weather_date = ''

    def get_weather_data_date(self):
        """Return weather data.

        This method extract date from the date list and
        return the date in words format
        """
        return datetime.strptime(self.weather_date, '%Y-%m-%d') \
            .strftime('%B %d')
