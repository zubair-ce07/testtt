import datetime


class Record:
    def __init__(self, line):
        self.date = self.get_datatime(line.get('PKT', line.get('PKST')))
        self.max_temperature = self.convert_datatype(line['Max TemperatureC'], int)
        self.min_temperature = self.convert_datatype(line['Min TemperatureC'], int)
        self.max_humidity = self.convert_datatype(line['Max Humidity'], int)
        self.mean_humidity = self.convert_datatype(line[' Mean Humidity'], float)
        self.mean_temperature = self.convert_datatype(line['Mean TemperatureC'], float)
        self.dew_point = self.convert_datatype(line['Dew PointC'], float)
        self.mean_dew_point = self.convert_datatype(line['MeanDew PointC'], float)
        self.min_dew_point = self.convert_datatype(line['Min DewpointC'], float)
        self.min_humidity = self.convert_datatype(line[' Min Humidity'], float)
        self.max_sea_level_pressure = self.convert_datatype(line[' Max Sea Level PressurehPa'], float)
        self.mean_sea_level_pressure = self.convert_datatype(line[' Mean Sea Level PressurehPa'], float)
        self.min_sea_level_pressure = self.convert_datatype(line[' Min Sea Level PressurehPa'], float)
        self.max_visibility = self.convert_datatype(line[' Max VisibilityKm'], float)
        self.mean_visibility = self.convert_datatype(line[' Mean VisibilityKm'], float)
        self.min_visibility = self.convert_datatype(line[' Min VisibilitykM'], float)
        self.max_wind_speed = self.convert_datatype(line[' Max Wind SpeedKm/h'], float)
        self.mean_wind_speed = self.convert_datatype(line[' Mean Wind SpeedKm/h'], float)
        self.max_gust_speed = self.convert_datatype(line[' Max Gust SpeedKm/h'], float)
        self.precipitationmm = self.convert_datatype(line['Precipitationmm'], float)
        self.cloud_cover = self.convert_datatype(line[' CloudCover'], float)
        self.events = line[' Events']
        self.wind_dir_degrees = self.convert_datatype(line['WindDirDegrees'], float)

    def convert_datatype(self, value, datatype):
        return datatype(value) if value is not '' else None

    def get_datatime(self, date):
        return datetime.datetime.strptime(date, '%Y-%m-%d').date()
