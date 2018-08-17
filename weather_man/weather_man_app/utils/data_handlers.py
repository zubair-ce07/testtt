# -*- coding: utf-8 -*-
"""
Data handlers to getting results from file utils and processed it into required form to provide the data to the
application.
"""
from weather_man_app.utils.file_utils import FileParser
from weather_man_app.utils.global_content import MathHelper


class WeatherReading:
    """
    Data structure for holding each weather reading
    """

    def __init__(self, **kwargs):
        self.file_path = kwargs.get('file_path', '')
        self.period = kwargs.get('period', '')

    @property
    def weather_readings(self):
        """
        This property get data from file.
        :return: List of data entries.
        """
        file_parser = FileParser.parse_data(self.file_path, self.period)
        weather_file_data = {
            'max_temp': list(),
            'min_temp': list(),
            'max_humidity': list(),
            'mean_humidity': list(),
            'day': list(),
        }
        for weather_data_entry in file_parser:
            for row in weather_data_entry:
                if self.check_corrupted_data(row):
                    continue
                weather_file_data['mean_humidity'].append(
                    MathHelper.parse_int(row[' Mean Humidity']))
                weather_file_data['max_temp'].append(
                    MathHelper.parse_int(row['Max TemperatureC']))
                weather_file_data['min_temp'].append(
                    MathHelper.parse_int(row['Min TemperatureC']))
                weather_file_data['max_humidity'].append(
                    MathHelper.parse_int(row['Max Humidity']))
                weather_file_data['day'].append(row.get('PKT', row.get('PKST')))
        return weather_file_data

    @staticmethod
    def check_corrupted_data(row):
        if not all([row[' Mean Humidity'], row['Max TemperatureC'], row['Min TemperatureC'], row['Max Humidity']]):
            return True
        return False
