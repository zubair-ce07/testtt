import csv
from fnmatch import fnmatch
from os import listdir

from weather_record import WeatherRecord


class WeatherDataReader:       
    @staticmethod
    def read_yearly_file_names(path, year):
        file_names = []

        for weather_file in listdir(path):
            if fnmatch(weather_file, f'*_{year}_*'):
                full_path = f'{path}/{weather_file}'
                file_names.append(full_path)

        return file_names

    @staticmethod
    def read_monthly_file_names(path, date):
        files_names = []
        year = date['year']
        month = date['month']

        for weather_file in listdir(path):
            if fnmatch(weather_file, f'*_{year}_{month}.txt'):
                full_path = f'{path}/{weather_file}'
                files_names.append(full_path)

        return files_names
                      
    def read_files(self, weather_files):
        max_temperature = []
        min_temperature = []
        max_humidity = []
        mean_humidity = []
        weather_record_date = []       

        for weather_file in weather_files:
            with open(weather_file) as weather_file:
                reader = csv.DictReader(weather_file)                
                for row in reader:                                                         
                    max_temperature.append(row['Max TemperatureC'])
                    weather_record_date.append(row.get('PKT') or row.get('PKST'))             
                    min_temperature.append(row['Min TemperatureC'])                   
                    max_humidity.append(row['Max Humidity'])                 
                    mean_humidity.append(row[' Mean Humidity'])

        weather_data = WeatherRecord(max_temperature, min_temperature,
            max_humidity, mean_humidity, weather_record_date)
        weather_record = weather_data.weather_record

        return weather_record
