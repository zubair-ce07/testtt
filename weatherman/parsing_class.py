from os import listdir
from os.path import isfile, join
import csv
import datetime

from weather_data import WeatherData


class ParsingFiles:
    def __init__(self, path, argument_list):
        self.path = path
        self.argument_list = argument_list
        self.all_files_names = self.get_all_files_names()

    def get_all_files_names(self):
        return [file_name for file_name in listdir(self.path) for arg in self.argument_list
                if isfile(join(self.path, file_name)) and arg in file_name]

    def reading_files(self):
        all_weather_readings = {}
        for file_name in self.all_files_names:
            month_record = []
            file_name_key = file_name.replace('.txt', '')
            with open(''.join([self.path, file_name]), 'r') as in_file:
                file_reader = csv.DictReader(in_file)
                for line in file_reader:
                    one_record = WeatherData()
                    date = line.get('PKT')
                    if date is None:
                        date = line.get('PKST')
                    one_record.pkt = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                    one_record.max_temperature = line['Max TemperatureC']
                    one_record.max_humidity = line['Max Humidity']
                    one_record.mean_humidity = line[' Mean Humidity']
                    one_record.min_temperature = line['Min TemperatureC']
                    # one_record.mean_temperature = line['Mean TemperatureC']
                    # one_record.dew_point = line['Dew PointC']
                    # one_record.mean_dew_point = line['MeanDew PointC']
                    # one_record.min_dew_point = line['Min DewpointC']
                    # one_record.min_humidity = line[' Min Humidity']
                    # one_record.max_sea_level_pressure = line[' Max Sea Level PressurehPa']
                    # one_record.mean_sea_level_pressure = line[' Mean Sea Level PressurehPa']
                    # one_record.min_sea_level_pressure = line[' Min Sea Level PressurehPa']
                    # one_record.max_visibility = line[' Max VisibilityKm']
                    # one_record.mean_visibility = line[' Mean VisibilityKm']
                    # one_record.min_visibility = line[' Min VisibilitykM']
                    # one_record.max_wind_speed = line[' Max Wind SpeedKm/h']
                    # one_record.mean_wind_speed = line[' Mean Wind SpeedKm/h']
                    # one_record.max_gust_speed = line[' Max Gust SpeedKm/h']
                    # one_record.precipitationmm = line['Precipitationmm']
                    # one_record.cloud_cover = line[' CloudCover']
                    # one_record.events = line[' Events']
                    # one_record.wind_dir_degrees = line['WindDirDegrees']
                    month_record.append(one_record)
            all_weather_readings[file_name_key] = month_record

        return all_weather_readings
