import datetime


class Record:
    def __init__(self, line):
        date = line.get('PKT', line.get('PKST'))
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        self.date = date
        self.max_temperature = self.get_int_or_none(line['Max TemperatureC'])
        self.min_temperature = self.get_int_or_none(line['Min TemperatureC'])
        self.max_humidity = self.get_int_or_none(line['Max Humidity'])
        self.mean_humidity = self.get_float_or_none(line[' Mean Humidity'])
        self.mean_temperature = self.get_float_or_none(line['Mean TemperatureC'])
        self.dew_point = self.get_float_or_none(line['Dew PointC'])
        self.mean_dew_point = self.get_float_or_none(line['MeanDew PointC'])
        self.min_dew_point = self.get_float_or_none(line['Min DewpointC'])
        self.min_humidity = self.get_float_or_none(line[' Min Humidity'])
        self.max_sea_level_pressure = self.get_float_or_none(line[' Max Sea Level PressurehPa'])
        self.mean_sea_level_pressure = self.get_float_or_none(line[' Mean Sea Level PressurehPa'])
        self.min_sea_level_pressure = self.get_float_or_none(line[' Min Sea Level PressurehPa'])
        self.max_visibility = self.get_float_or_none(line[' Max VisibilityKm'])
        self.mean_visibility = self.get_float_or_none(line[' Mean VisibilityKm'])
        self.min_visibility = self.get_float_or_none(line[' Min VisibilitykM'])
        self.max_wind_speed = self.get_float_or_none(line[' Max Wind SpeedKm/h'])
        self.mean_wind_speed = self.get_float_or_none(line[' Mean Wind SpeedKm/h'])
        self.max_gust_speed = self.get_float_or_none(line[' Max Gust SpeedKm/h'])
        self.precipitationmm = self.get_float_or_none(line['Precipitationmm'])
        self.cloud_cover = self.get_float_or_none(line[' CloudCover'])
        self.events = line[' Events']
        self.wind_dir_degrees = self.get_float_or_none(line['WindDirDegrees'])

    def get_float_or_none(self, value):
        if value:
            return float(value)
        return None

    def get_int_or_none(self, value):
        if value:
            return int(value)
        return None
