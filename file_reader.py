"""File Reading Module.

This module has a method which take file path and return it's data
"""
import csv


def read_file(path):
    """Read File by path.

    This method recieve file path through arguments and read data from the
    file and return it in a list's tuple
    """
    max_temperatures = []
    low_temperatures = []
    weather_data_dates = []
    max_humidities = []
    average_humidities = []

    try:
        csv_file = open(path)
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)  # for skipping titles
        for row in csv_reader:
            # checking if a field data is empty
            if row[1]:
                max_temperatures.append(int(row[1]))
            if row[3]:
                low_temperatures.append(int(row[3]))
            if row[7]:
                max_humidities.append(int(row[7]))
            if row[8]:
                average_humidities.append(int(row[8]))
            weather_data_dates.append(row[0])
        csv_file.close()
        return (max_temperatures, low_temperatures, max_humidities,
                average_humidities, weather_data_dates)
    except FileNotFoundError:
        print("Data not found for this date")
        exit()
