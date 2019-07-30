"""File Reading Module.

This module has a method which take file path and return it's data
"""
import csv

from weather_data import WeatherData


def read_file(path):
    """Read File by path.

    This method recieve file path through arguments and read data from the
    file and return it in a weather data object
    """
    weather_data = []
    try:
        input_file = csv.DictReader(open(path))
        for row in input_file:
            weather_data_object = WeatherData()
            weather_data_object.max_temperature = row['Max TemperatureC']
            weather_data_object.low_temperature = row['Min TemperatureC']
            weather_data_object.max_humidity = row['Max Humidity']
            weather_data_object.average_humidity = row[' Mean Humidity']
            weather_data_object.weather_date = row['PKT']
            weather_data.append(weather_data_object)
        return weather_data
    except FileNotFoundError:
        print("Data not found for this date")
        exit()
