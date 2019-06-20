from datetime import datetime


class WeatherRecord:

    def __init__(self, weather_record):
        self.pkt = datetime.strptime(weather_record.get("PKT", weather_record.get('PKST')),
                                     "%Y-%m-%d")
        self.max_temperature = int(weather_record["Max TemperatureC"])
        self.mean_temperature = weather_record["Mean TemperatureC"]
        self.min_temperature = int(weather_record["Min TemperatureC"])
        self.dew_point = weather_record["Dew PointC"]
        self.mean_dew_point = weather_record["MeanDew PointC"]
        self.min_dew_point = weather_record["Min DewpointC"]
        self.max_humidity = int(weather_record["Max Humidity"])
        self.mean_humidity = int(weather_record[" Mean Humidity"])
        self.min_humidity = weather_record[" Min Humidity"]
        self.max_sea_level_pressure = weather_record[" Max Sea Level PressurehPa"]
        self.mean_sea_level_pressure = weather_record[" Mean Sea Level PressurehPa"]
        self.min_sea_level_pressure = weather_record[" Min Sea Level PressurehPa"]
        self.max_visibility = weather_record[" Max VisibilityKm"]
        self.mean_visibility = weather_record[" Mean VisibilityKm"]
        self.min_visibility = weather_record[" Min VisibilitykM"]
        self.max_wind_speed = weather_record[" Max Wind SpeedKm/h"]
        self.mean_wind_speed = weather_record[" Mean Wind SpeedKm/h"]
        self.max_gust_speed = weather_record[" Max Gust SpeedKm/h"]
        self.precipitation = weather_record["Precipitationmm"]
        self.cloud_cover = weather_record[" CloudCover"]
        self.events = weather_record[" Events"]
        self.wind_dir_degrees = weather_record["WindDirDegrees"]
