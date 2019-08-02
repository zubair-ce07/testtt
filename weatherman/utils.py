"""Utils Module.

This module has differnet utility functions
"""
import re


def date_validation(date):
    """Validate Date.

    this meethod is for date validation format: 2014/12
    """
    regexp = re.compile(r'^[1-2][0-9]{3}/((0)?[1-9]|1[0-2])$')
    if regexp.search(str(date)):
        return
    print('Not a proper format or date')
    exit()


def year_validation(year):
    """Validate Year.

    This method is for year validation
    """
    regexp = re.compile(r'^[1-2][0-9]{3}$')
    if regexp.search(str(year)):
        return True
    return False


def get_max_temperature(weather_data):
    """Return Max Temperature.

    This method find and return max temperature weatherobject
    """
    max_temperature_weather = weather_data[0]
    for weather in weather_data:
        if weather.max_temperature and int(weather.max_temperature) > int(max_temperature_weather.max_temperature):
            max_temperature_weather = weather
    return max_temperature_weather


def get_min_temperature(weather_data):
    """Return Min Temperature.

    This method find and return min temperature weather object
    """
    min_temperature_weather = weather_data[0]
    for weather in weather_data:
        if weather.max_temperature and int(weather.max_temperature) > int(max_temperature_weather.max_temperature):
            min_temperature_weather = weather
    return min_temperature_weather


def get_max_humidity(weather_data):
    """Return Max Humidity.

    This method find and return max humidity weather object
    """
    max_humidity_weather = weather_data[0]
    for weather in weather_data:
        if weather.max_humidity:
            if int(weather.max_humidity) > int(max_humidity_weather.
                                               max_humidity):
                max_humidity_weather = weather
    return max_humidity_weather
