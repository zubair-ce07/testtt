import datetime
import csv
import os


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
                if os.path.exists(file_path):
                    file = open(file_path, 'r')
                    files.append(file)
        else:
            month_abr = datetime.date(2000, int(month), 1).strftime('%b')
            file_path = directory + '/Murree_weather_' + year + "_" + month_abr + '.txt'
            if os.path.exists(file_path):
                file = open(file_path, 'r')
                files.append(file)

        for file in files:
            weather_csv = csv.DictReader(file)
            for row in weather_csv:
                self.daily_weather.append(DayData(row))


class DayData:

    def __init__(self, conditions):
        self.pkt: str = None
        self.max_temperature: int = None
        self.min_temperature: int = None
        self.mean_temperature: int = None
        self.max_humidity: int = None
        self.mean_humidity: int = None
        self.min_humidity: int = None

        if conditions['PKT']:
            self.pkt = conditions['PKT']
        if conditions['Max TemperatureC']:
            self.max_temperature = int(conditions['Max TemperatureC'])
        if conditions['Min TemperatureC']:
            self.min_temperature = int(conditions['Min TemperatureC'])
        if conditions['Mean TemperatureC']:
            self.mean_temperature = int(conditions['Mean TemperatureC'])
        if conditions['Max Humidity']:
            self.max_humidity = int(conditions['Max Humidity'])
        if conditions[' Mean Humidity']:
            self.mean_humidity = int(conditions[' Mean Humidity'])
            

class ResultData:
    """"Data structure to hold the results calculated by calculation module"""
    def __init__(self, min_temperature, max_temperature, humidity):
        self.temperature_highest = max_temperature
        self.temperature_lowest = min_temperature
        self.humidity = humidity


