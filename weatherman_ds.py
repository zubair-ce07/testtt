import datetime
import csv


class WeatherData:
    """Data structure for storing data weather conditions"""

    def __init__(self):
        self.daily_weather = []

    def load_data(self, directory='', year='', month=''):
        """Loads a given months data in the data structure"""
        files = []
        if not month:
            for i in range(1, 13):
                month_abr = datetime.date(2000, i, 1).strftime('%b')
                file_path = directory + '/Murree_weather_' + year + "_" + month_abr + '.txt'
                file = open(file_path, 'r')
                if file:
                    files.append(file)
        else:
            month_abr = datetime.date(2000, int(month), 1).strftime('%b')
            file_path = directory + '/Murree_weather_' + year + "_" + month_abr + '.txt'
            file = open(file_path, 'r')
            if file:
                files.append(file)

        for file in files:
            weather_csv = csv.DictReader(file)
            for row in weather_csv:
                self.daily_weather.append(row)


class ResultData:
    """"Data structure to hold the results calculated by calculation module"""
    def __init__(self, min_temperature, max_temperature, humidity):
        self.temperature_highest = max_temperature
        self.temperature_lowest = min_temperature
        self.humidity = humidity


