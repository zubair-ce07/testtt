"""
File Reader Module.

This module returns the weather data
for the speficied file paths.
"""
import csv
from datetime import datetime
import constants
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
        highest_temp, min_temp, max_humidity, weather_date = '' * 4
        for file in self.filenames:      
            with open(file, mode="r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    weather_data = WeatherData(highest_temp, min_temp, max_humidity, weather_date)
                    weather_data.weather_date = datetime.strptime(row.get("PKT" if row.get("PKT") else "PKST"), '%Y-%m-%d')
                    weather_data.highest_temp = int(row.get(constants.MAX_TEMP)) if row.get(constants.MAX_TEMP) else 0
                    weather_data.min_temp = int(row.get(constants.MIN_TEMP)) if row.get(constants.MIN_TEMP) else 0
                    weather_data.max_humidity = int(row.get(constants.MAX_HUMID)) if row.get(constants.MAX_HUMID) else 0
                    weather_records.append(weather_data)
        return weather_records

            

    