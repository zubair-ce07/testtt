import csv
import glob

from wheatherman.forcast import Forecast


class DataReader:
    wheather_data = []

    def extract_year(self, directory):
        for file_name in glob.glob(directory):
            self.extract_files_data(file_name)
        return self.wheather_data

    def extract_monthly(self, directory):
        self.wheather_data.clear()
        self.extract_files_data(directory)
        return self.wheather_data

    def extract_files_data(self, file_name):
        with open(file_name) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.wheather_data.append(self.fill_data(row))

    @staticmethod
    def fill_data(row):
        maximum_temperature = None
        minimum_temperature = None
        maximum_humidity = None
        average_humidity = None

        if row['Max TemperatureC']:
            maximum_temperature = int(row['Max TemperatureC'])
        if row['Min TemperatureC']:
            minimum_temperature = int(row['Min TemperatureC'])
        if row['Max Humidity']:
            maximum_humidity = int(row['Max Humidity'])
        if row[' Mean Humidity']:
            average_humidity = int(row[' Mean Humidity'])
        daily_weather = Forecast(
            row['PKT'], maximum_temperature, minimum_temperature, maximum_humidity, average_humidity)
        return daily_weather
