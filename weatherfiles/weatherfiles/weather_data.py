
"""Module for weather data."""

from datetime import datetime

class WeatherData:
    """Class for weather data."""

    def __init__(self):
        """Iniatilizes lists for output."""
        self.highest_temp = []
        self.min_temp = []
        self.max_humidity = []
        self.average_humidity = []
        self.date = []

    def format_date(self):
        """Format date display by taking input from console."""
        return datetime.strptime(self, '%Y-%m-%d') \
            .strftime('%B %d')
