"""
this module read data from csv file and return result
"""
import csv
from utils import weather_data
from weather import Weather
import constants


class WeatherCsvHandler:
    """
    This class read the csv file and return result
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def read_csv_and_fill_data(self):
        """
        this method read a csv file, create a list and return it
        :return:
        """
        with open(self.file_path) as csvfile:
            weather_data_csv = csv.DictReader(csvfile, delimiter=',')
            for row in weather_data_csv:
                max_temp = constants.EMPTY_STRING
                if row['Max TemperatureC']:
                    max_temp = row['Max TemperatureC']
                min_temp = constants.EMPTY_STRING
                if row['Min TemperatureC']:
                    min_temp = row['Min TemperatureC']
                max_humid = constants.EMPTY_STRING
                if row['Max Humidity']:
                    max_humid = row['Max Humidity']
                mean_humid = constants.EMPTY_STRING
                if row[' Mean Humidity']:
                    mean_humid = row[' Mean Humidity']
                date = constants.EMPTY_STRING
                if row['PKT']:
                    date = row['PKT']
                weather_data.append(Weather(max_temp, min_temp, max_humid, mean_humid, date))
                # weather_data = list(read_csv)
