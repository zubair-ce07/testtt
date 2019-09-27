"""
File Reader Module.

This module returns the weather data
for the speficied file paths.
"""
import csv
import constants
from weather_data import WeatherData


class FileReader:
    """
    Class for file reader.

    This reads all the file paths and
    returns the weather data for it or
    returns an error if file not found.
    """

    def __init__(self, directory_file):
        """Initilizing attributes required for the class."""
        self.filenames = directory_file


    def read_file(self):
        """
        File read method.

        This method returns the weather data for
        the specified input files.
        """
        
        if  self.filenames:
            try:
                weather_records = []
                for file in self.filenames:
                    
                    with open(file, mode="r") as csv_file:
                        csv_reader = csv.DictReader(csv_file)
                        for index, row in enumerate(csv_reader):
                            weather_data = WeatherData()

                            if index == 0:
                                first_key = list(row.keys())[0]

                            weather_data.weather_date = row[first_key]
                            if not row[constants.max_temp]:
                                weather_data.highest_temp = 0
                            else:
                                weather_data.highest_temp = int(row[constants.max_temp])

                            if not row[constants.min_temp]:
                                weather_data.min_temp = 0
                            else:
                                weather_data.min_temp = int(row[constants.min_temp])
   
                            if not row[constants.max_humid]:
                                weather_data.max_humidity = 0
                            else:
                                weather_data.max_humidity = int(row[constants.max_humid])
                            weather_records.append(weather_data)   
                return weather_records
            except FileNotFoundError:
                print("File not found Error.")
                exit()

        else:
            print("File not found Error.")
            exit()

    