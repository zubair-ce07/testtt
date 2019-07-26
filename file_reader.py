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
        csv_file = open(path)
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)  # for skipping titles
        for row in csv_reader:
            # checking if a field data is empty
            if row[1]:
                weather_data.max_temperatures.append(int(row[1]))
            if row[3]:
                weather_data.low_temperatures.append(int(row[3]))
            if row[7]:
                weather_data.max_humidities.append(int(row[7]))
            if row[8]:
                weather_data.average_humidities.append(int(row[8]))
            weather_data.weather_data_dates.append(row[0])
        csv_file.close()
        return weather_data
    except FileNotFoundError:
        print("Data not found for this date")
        exit()
