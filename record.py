class Record:
    """Common base class for all records"""

    def __init__(self):
        self.date = " "
        self.max_temp = 0
        self.mean_temp = 0
        self.min_temp = 0
        self.dew_point = 0
        self.mean_dew_point = 0
        self.min_dew_point = 0
        self.max_humidity = 0
        self.mean_humidity = 0
        self.min_humidity = 0
        self.max_sea_level_pressure = 0
        self.mean_sea_level_pressure = 0
        self.min_sea_level_pressure = 0
        self.max_sea_level_pressure = 0
        self.max_visibility = 0.0
        self.mean_visibility = 0.0
        self.min_visibility = 0.0
        self.max_wind_speed = 0
        self.mean_wind_speed = 0
        self.max_gust_speed = 0
        self.precipitation = 0
        self.cloud_cover = " "
        self.events = 0
        self.wind_direction_degree = 0

    def add(self, dict):

        self.date = dict.get('PKT') or dict.get('PKST')

        if dict['Max TemperatureC']:
            self.max_temp = int(dict['Max TemperatureC'])
        if dict['Min TemperatureC']:
            self.min_temp = int(dict['Min TemperatureC'])
        if dict['Mean TemperatureC']:
            self.mean_temp = int(dict['Mean TemperatureC'])

        self.dew_point = dict['Dew PointC']
        self.mean_dew_point = dict['MeanDew PointC']
        self.min_dew_point = dict['Min DewpointC']

        if dict['Max Humidity']:
            self.max_humidity = int(dict['Max Humidity'])
        if dict[' Min Humidity']:
            self.min_humidity = int(dict[' Min Humidity'])
        if dict[' Mean Humidity']:
            self.mean_humidity = int(dict[' Mean Humidity'])

        self.max_sea_level_pressure = dict[' Max Sea Level PressurehPa']
        self.mean_sea_level_pressure = dict[' Mean Sea Level PressurehPa']
        self.min_sea_level_pressure = dict[' Min Sea Level PressurehPa']
        self.max_visibility = dict[' Max VisibilityKm']
        self.mean_visibility = dict[' Mean VisibilityKm']
        self.min_visibility = dict[' Min VisibilitykM']
        self.max_wind_speed = dict[' Max Wind SpeedKm/h']
        self.mean_wind_speed = dict[' Mean Wind SpeedKm/h']
        self.max_gust_speed = dict[' Max Gust SpeedKm/h']
        self.precipitation = dict['Precipitationmm']
        self.cloud_cover = dict[' CloudCover']
        self.events = dict[' Events']
        self.wind_direction_degree = dict['WindDirDegrees']

    def get_date(self):
        return self.date

    def get_max_temp(self):
        return self.max_temp

    def get_mean_temp(self):
        return self.mean_temp

    def get_min_temp(self):
        return self.min_temp

    def get_max_humidity(self):
        return self.max_humidity

    def get_mean_humidity(self):
        return self.mean_humidity

    def get_min_humidity(self):
        return self.min_humidity

    def display_date(self):
        print("Date: {}".format(self.date))

    def display_temp(self):
        print("Temperature : {}".format(self.max_temp))


