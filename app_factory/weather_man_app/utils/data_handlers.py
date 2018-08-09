# -*- coding: utf-8 -*-
"""
Data handlers to getting results from file utils and processed it into required form to provide the data to the
application.
"""
from app_factory.weather_man_app.utils.file_utils import ParseFiles


class WeatherReadingData(object):
    """
    Data structure for holding each weather reading
    """

    def __init__(self, *args, **kwargs):
        self.file_path = kwargs.get('file_path', '')
        self.period = kwargs.get('period', '')

    @property
    def weather_data(self):
        """
        This property get data from file.
        :return: List of data entries.
        """
        file_parser = ParseFiles.parse_data(self.file_path, self.period)
        weather_file_data = list()
        for weather_data_entry in file_parser:
            for row in weather_data_entry:
                weather_file_data.append(row)
        return weather_file_data
