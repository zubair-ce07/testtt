import datetime


class Record:
    def __init__(self, line):
        date = line.get('PKT', line.get('PKST'))
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        self.date = date
        self.max_temperature = self.convert_datatype_to_int(line['Max TemperatureC'])
        self.min_temperature = self.convert_datatype_to_int(line['Min TemperatureC'])
        self.max_humidity = self.convert_datatype_to_float(line['Max Humidity'])
        self.mean_humidity = self.convert_datatype_to_float(line[' Mean Humidity'])
        self.mean_temperature = self.convert_datatype_to_float(line['Mean TemperatureC'])
        self.dew_point = self.convert_datatype_to_float(line['Dew PointC'])
        self.mean_dew_point = self.convert_datatype_to_float(line['MeanDew PointC'])
        self.min_dew_point = self.convert_datatype_to_float(line['Min DewpointC'])
        self.min_humidity = self.convert_datatype_to_float(line[' Min Humidity'])
        self.max_sea_level_pressure = self.convert_datatype_to_float(line[' Max Sea Level PressurehPa'])
        self.mean_sea_level_pressure = self.convert_datatype_to_float(line[' Mean Sea Level PressurehPa'])
        self.min_sea_level_pressure = self.convert_datatype_to_float(line[' Min Sea Level PressurehPa'])
        self.max_visibility = self.convert_datatype_to_float(line[' Max VisibilityKm'])
        self.mean_visibility = self.convert_datatype_to_float(line[' Mean VisibilityKm'])
        self.min_visibility = self.convert_datatype_to_float(line[' Min VisibilitykM'])
        self.max_wind_speed = self.convert_datatype_to_float(line[' Max Wind SpeedKm/h'])
        self.mean_wind_speed = self.convert_datatype_to_float(line[' Mean Wind SpeedKm/h'])
        self.max_gust_speed = self.convert_datatype_to_float(line[' Max Gust SpeedKm/h'])
        self.precipitationmm = self.convert_datatype_to_float(line['Precipitationmm'])
        self.cloud_cover = self.convert_datatype_to_float(line[' CloudCover'])
        self.events = line[' Events']
        self.wind_dir_degrees = self.convert_datatype_to_float(line['WindDirDegrees'])

    def convert_datatype_to_float(self, value):
        return float(value) if value else None

    def convert_datatype_to_int(self, value):
        return int(value) if value else None
