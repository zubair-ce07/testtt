from datetime import datetime
from Weather import Weather


class ReadWeather:

    def __init__(self):
        pass

    def read_weather(self, mw, filefullpath):
        f = open(filefullpath, "r")

        f.readline()

        for line in f:
            w = Weather()
            weather_data = line.split(',')

            i = 0
            while i < len(weather_data):
                if weather_data[i] == "":
                    weather_data[i] = None

                i = i+1

            w.pkt_dt = datetime.strptime(weather_data[0], '%Y-%m-%d')
            w.tempC.append(weather_data[1])
            w.tempC.append(weather_data[2])
            w.tempC.append(weather_data[3])
            w.dew_pointC.append(weather_data[4])
            w.dew_pointC.append(weather_data[5])
            w.dew_pointC.append(weather_data[6])
            w.humidity.append(weather_data[7])
            w.humidity.append(weather_data[8])
            w.humidity.append(weather_data[9])
            w.sea_level_pressurehPa.append(weather_data[10])
            w.sea_level_pressurehPa.append(weather_data[11])
            w.sea_level_pressurehPa.append(weather_data[12])
            w.visibilitykm.append(weather_data[13])
            w.visibilitykm.append(weather_data[14])
            w.visibilitykm.append(weather_data[15])
            w.winde_speedkmph.append(weather_data[16])
            w.winde_speedkmph.append(weather_data[17])
            w.max_gust_speedkmph = weather_data[18]
            w.percipitaionmm = (weather_data[19])
            w.cloud_cover = (weather_data[20])
            w.event = (weather_data[21])
            w.wind_directionD = (weather_data[22])
            mw.add_weather(w, w.pkt_dt.day)
            del w
        f.close()
