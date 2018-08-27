from datetime import datetime
from weather import Weather


class ReadWeather:

    def __init__(self):
        pass

    def read_weather(self, month_weather, file_full_path):
        file = open(file_full_path, "r")

        file.readline()

        for line in file:
            weather = Weather()
            weather_data = line.split(',')

            counter = 0
            while counter < len(weather_data):
                if weather_data[counter] == "":
                    weather_data[counter] = None

                counter = counter+1

            weather.pkt_dt = datetime.strptime(weather_data[0], '%Y-%m-%d')
            weather.tempC.append(weather_data[1])
            weather.tempC.append(weather_data[2])
            weather.tempC.append(weather_data[3])
            weather.dew_pointC.append(weather_data[4])
            weather.dew_pointC.append(weather_data[5])
            weather.dew_pointC.append(weather_data[6])
            weather.humidity.append(weather_data[7])
            weather.humidity.append(weather_data[8])
            weather.humidity.append(weather_data[9])
            weather.sea_level_pressurehPa.append(weather_data[10])
            weather.sea_level_pressurehPa.append(weather_data[11])
            weather.sea_level_pressurehPa.append(weather_data[12])
            weather.visibilitykm.append(weather_data[13])
            weather.visibilitykm.append(weather_data[14])
            weather.visibilitykm.append(weather_data[15])
            weather.wind_speedkmph.append(weather_data[16])
            weather.wind_speedkmph.append(weather_data[17])
            weather.max_gust_speedkmph = weather_data[18]
            weather.percipitaionmm = (weather_data[19])
            weather.cloud_cover = (weather_data[20])
            weather.event = (weather_data[21])
            weather.wind_directionD = (weather_data[22])
            month_weather.add_weather(weather, weather.pkt_dt.day)
            del weather
        file.close()
