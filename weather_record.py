class WeatherRecord:
    def __init__(self):
        self.date = ""
        self.max_temperature = ""
        self.mean_temperature = ""
        self.min_temperature = ""
        self.max_dew_point = ""
        self.mean_dew_point = ""
        self.min_dew_point = ""
        self.max_humidity = ""
        self.mean_humidity = ""
        self.min_humidity = ""
        self.max_sea_level_pressure = ""
        self.mean_sea_level_pressure = ""
        self.min_sea_level_pressure = ""
        self.max_visibility = ""
        self.mean_visibility = ""
        self.min_visibility = ""
        self.max_wind_speed = ""
        self.mean_wind_speed = ""
        self.max_gust_speed = ""
        self.precipitation = ""
        self.cloud_cover = ""
        self.events = ""
        self.wind_dir_degrees = ""



    def load_weather_record(self, date, max_temperature, mean_temperature, min_temperature, max_dew_point,
                            mean_dew_point, min_dew_point, max_humidity, mean_humidity, min_humidity,
                            max_sea_level_pressure,
                            mean_sea_level_pressure, min_sea_level_pressure, max_visibility, mean_visibility,
                            min_visibility, max_wind_speed, mean_wind_speed, max_gust_speed, precipitation,
                            cloud_cover, events, wind_dir_degrees):
        self.date = date
        self.max_temperature = max_temperature
        self.mean_temperature = mean_temperature
        self.min_temperature = min_temperature
        self.max_dew_point = max_dew_point
        self.mean_dew_point = mean_dew_point
        self.min_dew_point = min_dew_point
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.min_humidity = min_humidity
        self.max_sea_level_pressure = max_sea_level_pressure
        self.mean_sea_level_pressure = mean_sea_level_pressure
        self.min_sea_level_pressure = min_sea_level_pressure
        self.max_visibility = max_visibility
        self.mean_visibility = mean_visibility
        self.min_visibility = min_visibility
        self.max_wind_speed = max_wind_speed
        self.mean_wind_speed = mean_wind_speed
        self.max_gust_speed = max_gust_speed
        self.precipitation = precipitation
        self.cloud_cover = cloud_cover
        self.events = events
        self.wind_dir_degrees = wind_dir_degrees
