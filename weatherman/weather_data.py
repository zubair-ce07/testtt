
"""Module for weather data."""
from datetime import datetime
import constants


class WeatherData:
    """Class for weather data."""

    def __init__(self, row):
        """Iniatilizes lists for output."""
        self.row = row
        self.highest_temp = int(row.get(constants.MAX_TEMP)) if row.get(constants.MAX_TEMP) else 0
        self.min_temp = int(row.get(constants.MIN_TEMP)) if row.get(constants.MIN_TEMP) else 0
        self.max_humidity = int(row.get(constants.MAX_HUMID)) if row.get(constants.MAX_HUMID) else 0
        self.weather_date = datetime.strptime(row.get("PKT" if row.get("PKT") else "PKST"), '%Y-%m-%d')
