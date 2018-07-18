import datetime


class Record:
    def __init__(self, line):
        date = line.get('PKT', line.get('PKST'))
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        self.date = date
        self.max_temperature = line['Max TemperatureC']
        self.min_temperature = line['Min TemperatureC']
        self.max_humidity = line['Max Humidity']
        self.mean_humidity = line[' Mean Humidity']
        self.mean_temperature = line['Mean TemperatureC']
        self.dew_point = line['Dew PointC']
        self.mean_dew_point = line['MeanDew PointC']
        self.min_dew_point = line['Min DewpointC']
        self.min_humidity = line[' Min Humidity']
        self.max_sea_level_pressure = line[' Max Sea Level PressurehPa']
        self.mean_sea_level_pressure = line[' Mean Sea Level PressurehPa']
        self.min_sea_level_pressure = line[' Min Sea Level PressurehPa']
        self.max_visibility = line[' Max VisibilityKm']
        self.mean_visibility = line[' Mean VisibilityKm']
        self.min_visibility = line[' Min VisibilitykM']
        self.max_wind_speed = line[' Max Wind SpeedKm/h']
        self.mean_wind_speed = line[' Mean Wind SpeedKm/h']
        self.max_gust_speed = line[' Max Gust SpeedKm/h']
        self.precipitationmm = line['Precipitationmm']
        self.cloud_cover = line[' CloudCover']
        self.events = line[' Events']
        self.wind_dir_degrees = line['WindDirDegrees']
