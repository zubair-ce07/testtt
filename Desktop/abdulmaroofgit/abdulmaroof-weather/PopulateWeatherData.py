import os
from Weather import Weather


class WeatherFilesData:

    def populate_file_names_list(self, files=[]):
        path_to_folder = "/home/weather/Desktop/pythontraining/the-lab/weatherfiles/weatherfiles/"
        for i in os.listdir(path_to_folder):
            if i.endswith('.txt'):
                files.append(path_to_folder + i)
        return files

    def populate_data_structures(self):
        weather_files = self.populate_file_names_list(files = [])
        count = 0
        weather_list_all_files = []
        for data in weather_files:
            with open(data, "r") as f:
                index = -1
                weather_attribs = Weather()
                for line in f:
                    if(index != -1):
                        checkstr = [x.strip() for x in line.split(',')]
                        lineSplit = [None if i == '' else i for i in checkstr]
                        weather_attribs.pkt[index] = lineSplit[0]
                        weather_attribs.max_temperature_c[index] = lineSplit[1]
                        weather_attribs.mean_temperature_c[index] = lineSplit[2]
                        weather_attribs.min_temperature_c[index] = lineSplit[3]
                        weather_attribs.dew_point_c[index] = lineSplit[4]
                        weather_attribs.mean_dew_point_c[index] = lineSplit[5]
                        weather_attribs.min_dewpoint_c[index] = lineSplit[6]
                        weather_attribs.max_humidity[index] = lineSplit[7]
                        weather_attribs.mean_humidity[index] = lineSplit[8]
                        weather_attribs.min_humidity[index] = lineSplit[9]
                        weather_attribs.max_sea_pressureh_pa[index] = lineSplit[10]
                        weather_attribs.mean_sea_pressureh_pa[index] = lineSplit[11]
                        weather_attribs.min_sea_pressureh_pa[index] = lineSplit[12]
                        weather_attribs.max_visibility_km[index] = lineSplit[13]
                        weather_attribs.mean_visibility_km[index] = lineSplit[14]
                        weather_attribs.min_visibility_km[index] = lineSplit[15]
                        weather_attribs.max_wind_speed_kmper_h[index] = lineSplit[16]
                        weather_attribs.mean_wind_speed_kmper_h[index] = lineSplit[17]
                        weather_attribs.max_gust_speed_kmper_h[index] = lineSplit[18]
                        weather_attribs.Precipitation_mm[index] = lineSplit[19]
                        weather_attribs.cloud_cover[index] = lineSplit[20]
                        weather_attribs.events[index] = lineSplit[21]
                        weather_attribs.wind_dir_degrees[index] = lineSplit[22]
                    index+=1

                weather_list_all_files.insert(count, weather_attribs)
                count += 1

        i = -1
        while i < 145:
            j = 0
            i += 1
            while j < 32:
                j += 1

        return weather_list_all_files
