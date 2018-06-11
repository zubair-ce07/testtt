

class Weather:

    def __init__(self):
        self.pkt = [None] * 32
        self.max_temperature_c = [None] * 32
        self.mean_temperature_c = [None] * 32
        self.min_temperature_c = [None] * 32
        self.dew_point_c = [None] * 32
        self.mean_dew_point_c = [None] * 32
        self.min_dewpoint_c = [None] * 32
        self.max_humidity = [None] * 32
        self.mean_humidity = [None] * 32
        self.min_humidity = [None] * 32
        self.max_sea_pressureh_pa = [None] * 32
        self.mean_sea_pressureh_pa = [None] * 32
        self.min_sea_pressureh_pa = [None] * 32
        self.max_visibility_km = [None] * 32
        self.mean_visibility_km = [None] * 32
        self.min_visibility_km = [None] * 32
        self.max_wind_speed_kmper_h = [None] * 32
        self.mean_wind_speed_kmper_h = [None] * 32
        self.max_gust_speed_kmper_h = [None] * 32
        self.Precipitation_mm = [None] * 32
        self.cloud_cover = [None] * 32
        self.events = [None] * 32
        self.wind_dir_degrees = [None] * 32