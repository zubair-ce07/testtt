"""
Utils Module.

This module has the get methods for max,
min temperatures and max humidity.
"""

from datetime import datetime

class Utils:
    """Utils class."""

    @staticmethod
    def get_max_temperature(weather_records):
        """
        To get maximum temperature for input files.

        This method returns the maximum of the maximum
        temperatures list.
        """
        highest_temp_value = weather_records[0]
        for weather in weather_records:
            if weather.highest_temp and int(weather.highest_temp) > int(highest_temp_value.highest_temp):
                highest_temp_value = weather
        return highest_temp_value

    @staticmethod
    def get_min_temperature(weather_records):
        """
        To get minimum temperature for input files.

        This method returns the minimum of the minimum
        temperatures list.
        """
        min_temp_value = weather_records[0]
        for weather in weather_records:
            if weather.min_temp and int(weather.min_temp) < int(min_temp_value.min_temp):
                min_temp_value = weather
        return min_temp_value

    @staticmethod
    def get_max_humidity(weather_records):
        """
        To get maximum humity for input files.

        This method returns the maximum of the
        maximum humidity list.
        """
        max_humidity_value = weather_records[0]
        for weather in weather_records:
            if weather.max_humidity:
                if int(weather.max_humidity) > int(max_humidity_value.max_humidity):
                    max_humidity_value = weather
        return max_humidity_value

    @staticmethod
    def format_date(date):
        """Format date display by taking input from console."""
        return datetime.strptime(date, '%Y-%m-%d') \
            .strftime('%B %d')
