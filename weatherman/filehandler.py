"""This class handles file operations"""
import os
import csv
import logging
from datetime import date
from weather_reading import WeatherReading
import constants


def get_file_path(path_to_files, city_name, year, month):
    """Return path to the required file given the city and date"""
    file_path = "{}{}_weather_{}_{}.txt".format(path_to_files,
                                                city_name,
                                                year,
                                                date(year, month, 1).strftime("%b"))
    return file_path


# Skips leading spaces in the input if any.
csv.register_dialect('spaceDialect', delimiter=',', skipinitialspace=True)


class WeatherFileHandler:
    """File handler for weatherman. Reads entries from files
    depending upon the date and city provided.
    """

    def __init__(self, path_to_files, city):
        """
        Constructiod
        :param path_to_files: string, Path to directory containing weather records.
        :param city: string, name of the city for which weather data is required.
        """
        self.path_to_files = path_to_files
        self.city = city

    def read_month_file(self, year, month):
        """
        Read weather records for given year and month as list of
        WeatherReading objects.

        :param year: int
        :param month: int
        :return: list of WeatherReading objects
        """
        file_path = get_file_path(self.path_to_files, self.city, year, month)
        if os.path.isfile(file_path):
            readings = []
            with open(file_path) as csvfile:
                next(csvfile)
                for row in csv.reader(csvfile, dialect='spaceDialect'):
                    reading = WeatherReading(
                        pkt=row[constants.PKT_INDEX],
                        min_temperature=row[constants.MIN_TEMPERATURE_INDEX],
                        max_temperature=row[constants.MAX_TEMPERATURE_INDEX],
                        mean_humidity=row[constants.MEAN_HUMIDITY_INDEX],
                        min_humidity=row[constants.MIN_HUMIDITY_INDEX],
                        max_humidity=row[constants.MAX_HUMIDITY_INDEX]
                    )
                    readings.append(reading)
                return readings
            logging.error("Cannot open file : %s", file_path)
        logging.error("File does not exist : %s", file_path)
        return None

    def read_year_files(self, year):
        """Read weather records for given year as list of
        WeatherReading objects.

        :param year: int
        :return: list of WeatherReading objects
        """
        readings = []
        for month in range(1, 13):
            reading = self.read_month_file(year, month)
            if reading:
                readings = readings + reading
        return readings
