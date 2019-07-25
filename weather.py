from datetime import datetime


class WeatherReading:
    """Structure to store weather readings data"""

    def __init__(self, readings_row):
        if "PKT" in readings_row:
            self.date = datetime.strptime(readings_row["PKT"], '%Y-%m-%d')
        elif "PSKT" in readings_row:
            self.date = datetime.strptime(readings_row["PSKT"], '%Y-%m-%d')

        self.max_temperature = int(readings_row["Max TemperatureC"])
        self.mean_temperature = int(readings_row["Mean TemperatureC"])
        self.min_temperature = int(readings_row["Min TemperatureC"])
        # self.dew_point = int(readings_row["Dew PointC"])
        # self.mean_dew_point = readings_row["MeanDew PointC"]
        # self.min_dew_point = readings_row["Min DewpointC"]
        self.max_humidity = int(readings_row["Max Humidity"])
        self.mean_humidity = int(readings_row[" Mean Humidity"])
        self.min_humidity = int(readings_row[" Min Humidity"])
        # self.max_sea_level_pressure = readings_row[" Max Sea Level PressurehPa"]
        # self.mean_sea_level_pressure = readings_row[" Mean Sea Level PressurehPa"]
        # self.min_sea_level_pressure = readings_row[" Min Sea Level PressurehPa"]
        # self.max_visibility = readings_row[" Max VisibilityKm"]
        # self.mean_visibility = readings_row[" Mean VisibilityKm"]
        # self.min_visibility = readings_row[" Min VisibilitykM"]
        # self.max_wind_speed = readings_row[" Max Wind SpeedKm/h"]
        # self.mean_wind_speed = readings_row[" Mean Wind SpeedKm/h"]
        # self.max_gust_speed = readings_row[" Max Gust SpeedKm/h"]
        # self.precipitation = readings_row["Precipitationmm"]
        # self.cloud_cover = readings_row[" CloudCover"]
        # self.event = readings_row[" Events"]
        # self.wind_dir_degrees = readings_row["WindDirDegrees"]
