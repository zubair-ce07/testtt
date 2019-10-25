import datetime
from constants import Constants


def get_highest_temperature_reading(weather_readings):
    return max(weather_readings, key=lambda reading: reading.max_temperature_c)


def get_lowest_temperature_reading(weather_readings):
    return min(weather_readings, key=lambda reading: reading.min_temperature_c)


def get_most_humid_day(weather_readings):
    return max(weather_readings, key=lambda reading: reading.max_humidity)


def get_highest_temperature_average_value(weather_readings):
    sum_of_temperatures = 0
    no_of_readings = 0
    for reading in weather_readings:
        if reading.max_temperature_c != Constants.INVALID_DATA:
            sum_of_temperatures = sum_of_temperatures + reading.max_temperature_c
            no_of_readings = no_of_readings + 1

    return sum_of_temperatures // no_of_readings


def get_lowest_temperature_average_value(weather_readings):
    sum_of_temperatures = 0
    no_of_readings = 0
    for reading in weather_readings:
        if reading.min_temperature_c != Constants.INVALID_DATA:
            sum_of_temperatures = sum_of_temperatures + reading.min_temperature_c
            no_of_readings = no_of_readings + 1

    return sum_of_temperatures // no_of_readings


def get_mean_humid_day_average(weather_readings):
    sum_of_temperatures = 0
    no_of_readings = 0
    for reading in weather_readings:
        if reading.mean_humidity != Constants.INVALID_DATA:
            sum_of_temperatures = sum_of_temperatures + reading.mean_humidity
            no_of_readings = no_of_readings + 1

    return sum_of_temperatures // no_of_readings


