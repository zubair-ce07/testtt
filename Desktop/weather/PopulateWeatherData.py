import os
import pandas as pd


class WeatherFilesData:

    def populate_file_names_list(self, path_to_folder):
        files = []
        for i in os.listdir(path_to_folder):
            if i.endswith('.txt'):
                files.append(path_to_folder + i)
        return files

    def populate_data_structures(self, path):
        weather_files = self.populate_file_names_list(path)
        count = 0
        weather_list_all_files = []
        for data in weather_files:
            with open(data, "r") as f:
                reader = pd.read_csv(f, sep=',')
                reader.columns = ['pkt', 'max_temperature_c', 'mean_temperature_c',
                                  'min_temperature_c', 'max_dew_point_c', 'mean_dew_point_c',
                                  'min_dewpoint_c', 'max_humidity', 'mean_humidity',
                                  'min_humidity', 'max_sea_pressureh_pa', 'mean_sea_pressureh_pa',
                                  'min_sea_pressureh_pa', 'max_visibility_km', 'mean_visibility_km',
                                  'min_visibility_km', 'max_wind_speed_kmper_h', 'mean_wind_speed_kmper_h',
                                  'max_gust_speed_kmper_h', 'Precipitation_mm', 'cloud_cover',
                                  'events', 'wind_dir_degrees']
                weather_list_all_files.append(reader)

        return weather_list_all_files
