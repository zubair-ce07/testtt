"""
File Reader Module.

This module returns the weather data
for the speficied file paths.
"""
import csv
from constants import Constants
from weather_data import WeatherData


class FileReader:
    """
    Class for file reader.

    This reads all the file paths and
    returns the weather data for it or
    returns an error if file not found.
    """

    def __init__(self, file):
        """Initilizing attributes required for the class."""
        self.filenames = file

    def read_file(self):
        """
        File read method.

        This method returns the weather data for
        the specified input files.
        """
        if  self.filenames:
            try:
                weather_data = []
                weather_data = WeatherData()
                for file in self.filenames:
                    csv_reader = csv.DictReader(open(file))
                    line_count = 0
                    for row in csv_reader:
                        constants = Constants()
                        if line_count == 0:
                            first_key = list(row.keys())[0]
                            line_count += 1

                        weather_data.date.append(row[first_key])
                        if not row[constants.max_temp]:
                            weather_data.highest_temp.append(0)
                        else:
                            weather_data.highest_temp.append(
                                int(row[constants.max_temp])
                            )

                        if not row[constants.min_temp]:
                            weather_data.min_temp.append(0)
                        else:
                            weather_data.min_temp.append(
                                int(row[constants.min_temp])
                            )

                        if not row[constants.max_humid]:
                            weather_data.max_humidity.append(0)
                        else:
                            weather_data.max_humidity.append(
                                int(row[constants.max_humid])
                            )
                        line_count += 1
                return weather_data
            except FileNotFoundError:
                return "File not found Error."
        else:
            return "File not found Error."
