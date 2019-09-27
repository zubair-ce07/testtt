"""
File Reader Module.

This module returns the weather data
for the speficied file paths.
"""
import csv
from weather_data import WeatherData



class FileReader:
    """
    Class for file reader.

    This reads all the file paths and
    returns the weather data for it or
    returns an error if file not found.
    """

    def __init__(self, directory_files):
        """Initilizing attributes required for the class."""
        self.filenames = directory_files

    def read_file(self):
        """
        File read method.

        This method returns the weather data for
        the specified input files.
        """
        if  not self.filenames:
            print("File not found Error.")
            exit()
        weather_records = []
        for file in self.filenames:      
            with open(file, mode="r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    weather_data = WeatherData(row)
                    weather_records.append(weather_data)
        return weather_records
