class DayWeather:
    def __init__(self, pkt, max_temperaturec, mean_temperaturec
                 , min_temperaturec, dew_pointc, meandew_pointc
                 , min_dewpointc, max_humidity, mean_humidity
                 , min_humidity, max_sea_level_pressurehpa
                 , mean_sea_level_pressurehpa
                 , min_sea_level_pressurehpa
                 , max_visibilitykm, mean_visibilitykm
                 , min_visibilitykm, max_wind_speedkm
                 , mean_wind_speedkm, max_gust_speedkm
                 , precipitationcm, cloudcover
                 , events, winddirdegrees
                 ):
        self.pkt = pkt
        self.max_temperaturec = max_temperaturec
        self.mean_temperaturec = mean_temperaturec
        self.min_temperaturec = min_temperaturec
        self.dew_pointc = dew_pointc
        self.meandew_pointc = meandew_pointc
        self.min_dewpointc = min_dewpointc
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.min_humidity = min_humidity
        self.max_sea_level_pressurehpa = max_sea_level_pressurehpa
        self.mean_sea_level_pressurehpa = mean_sea_level_pressurehpa
        self.min_sea_level_pressurehpa = min_sea_level_pressurehpa
        self.max_visibilitykm = max_visibilitykm
        self.mean_visibilitykm = mean_visibilitykm
        self.min_visibilitykm = min_visibilitykm
        self.max_wind_speedkm = max_wind_speedkm
        self.mean_wind_speedkm = mean_wind_speedkm
        self.max_gust_speedkm = max_gust_speedkm
        self.precipitationcm = precipitationcm
        self.cloudcover = cloudcover
        self.events = events
        self.winddirdegrees = winddirdegrees
