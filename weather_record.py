from datetime import datetime


class WeatherRecord:

    def __init__(self, day_weather_record):
        self.pkt = datetime.strptime(
            day_weather_record.get("PKT", day_weather_record.get('PKST')),
            "%Y-%m-%d")
        self.max_temperature = day_weather_record["Max TemperatureC"]
        self.mean_temperature = day_weather_record["Mean TemperatureC"]
        self.min_temperature = day_weather_record["Min TemperatureC"]
        self.dew_point = day_weather_record["Dew PointC"]
        self.mean_dew_point = day_weather_record["MeanDew PointC"]
        self.min_dew_point = day_weather_record["Min DewpointC"]
        self.max_humidity = day_weather_record["Max Humidity"]
        self.mean_humidity = day_weather_record[" Mean Humidity"]
        self.min_humidity = day_weather_record[" Min Humidity"]
        self.max_sea_level_pressure = day_weather_record[" Max Sea Level PressurehPa"]
        self.mean_sea_level_pressure = day_weather_record[" Mean Sea Level PressurehPa"]
        self.min_sea_level_pressure = day_weather_record[" Min Sea Level PressurehPa"]
        self.max_visibility = day_weather_record[" Max VisibilityKm"]
        self.mean_visibility = day_weather_record[" Mean VisibilityKm"]
        self.min_visibility = day_weather_record[" Min VisibilitykM"]
        self.max_wind_speed = day_weather_record[" Max Wind SpeedKm/h"]
        self.mean_wind_speed = day_weather_record[" Mean Wind SpeedKm/h"]
        self.max_gust_speed = day_weather_record[" Max Gust SpeedKm/h"]
        self.precipitation = day_weather_record["Precipitationmm"]
        self.cloud_cover = day_weather_record[" CloudCover"]
        self.events = day_weather_record[" Events"]
        self.wind_dir_degrees = day_weather_record["WindDirDegrees"]
