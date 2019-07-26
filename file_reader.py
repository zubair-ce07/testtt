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
    weather_data = WeatherData()
    try:
        input_file = csv.DictReader(open(path))
        for row in input_file:
            if row['Max TemperatureC']:
                weather_data.max_temperatures.append(
                    int(row['Max TemperatureC']))
            if row['Min TemperatureC']:
                weather_data.low_temperatures.append(
                    int(row['Min TemperatureC']))
            if row['Max Humidity']:
                weather_data.max_humidities.append(int(row['Max Humidity']))
            if row[' Mean Humidity']:
                weather_data.average_humidities.append(
                    int(row[' Mean Humidity']))
            weather_data.weather_data_dates.append(row['PKT'])
        return weather_data
    except FileNotFoundError:
        print("Data not found for this date")
        exit()
