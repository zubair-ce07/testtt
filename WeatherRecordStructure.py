"""This Module contains DataStructure for each record from the files"""


class WeatherRecord:

    def __init__(
            self,
            date_pkt=None,
            max_temperature_c=None,
            mean_temperature_c=None,
            min_temperature_c=None,
            dew_point_c=None,
            mean_dew_point_c=None,
            min_dew_point_c=None,
            max_humidity=None,
            mean_humidity=None,
            min_humidity=None,
            max_sea_level_pressure_hpa=None,
            mean_sea_level_pressure_hpa=None,
            min_sea_level_pressure_hpa=None,
            max_visibility_km=None,
            mean_visibility_km=None,
            min_visibility_km=None,
            max_wind_speed_kmph=None,
            mean_wind_speed_kmph=None,
            max_gust_speed_kmph=None,
            precipitationmm=None,
            cloud_cover=None,
            events=None,
            wind_dir_degrees=None,
    ):
        self.date_pkt = date_pkt

        # Temperatures
        if max_temperature_c[0] == '':
            self.max_temperature_c = None
        else:
            self.max_temperature_c = int(max_temperature_c[0])

        if mean_temperature_c[0] == '':
            self.mean_temperature_c = None
        else:
            self.mean_temperature_c = int(mean_temperature_c[0])

        if min_temperature_c[0] == '':
            self.min_temperature_c = None
        else:
            self.min_temperature_c = int(min_temperature_c[0])

        # Dew Points
        if dew_point_c[0] == '':
            self.dew_point_c = None
        else:
            self.dew_point_c = int(dew_point_c[0])
        if mean_dew_point_c[0] == '':
            self.mean_dew_point_c = None
        else:
            self.mean_dew_point_c = float(mean_dew_point_c[0])

        if min_dew_point_c[0] == '':
            self.min_dew_point_c = None
        else:
            self.min_dew_point_c = float(min_dew_point_c[0])

        # Humidity
        if max_humidity[0] == '':
            self.max_humidity = None
        else:
            self.max_humidity = float(max_humidity[0])

        if mean_humidity[0] == '':
            self.mean_humidity = None
        else:
            self.mean_humidity = float(mean_humidity[0])

        if min_humidity[0] == '':
            self.min_humidity = None
        else:
            self.min_humidity = float(min_humidity[0])

        # Sea Level
        if max_sea_level_pressure_hpa[0] == '':
            self.max_sea_level_pressure_hpa = None
        else:
            self.max_sea_level_pressure_hpa = float(max_sea_level_pressure_hpa[0])

        if mean_sea_level_pressure_hpa[0] == '':
            self.mean_sea_level_pressure_hpa = None
        else:
            self.mean_sea_level_pressure_hpa = float(mean_sea_level_pressure_hpa[0])

        if min_sea_level_pressure_hpa[0] == '':
            self.min_sea_level_pressure_hpa = None
        else:
            self.min_sea_level_pressure_hpa = float(min_sea_level_pressure_hpa[0])

        # Visibility
        if max_visibility_km[0] == '':
            self.max_visibility_km = None
        else:
            self.max_visibility_km = float(max_visibility_km[0])

        if mean_visibility_km[0] == '':
            self.mean_visibility_km = None
        else:
            self.mean_visibility_km = float(mean_visibility_km[0])

        if min_visibility_km[0] == '':
            self.min_visibility_km = None
        else:
            self.min_visibility_km = float(min_visibility_km[0])

        # Wind Speed
        if max_wind_speed_kmph[0] == '':
            self.max_wind_speed_kmph = None
        else:
            self.max_wind_speed_kmph = float(max_wind_speed_kmph[0])

        if mean_wind_speed_kmph[0] == '':
            self.mean_wind_speed_kmph = None
        else:
            self.mean_wind_speed_kmph = float(mean_wind_speed_kmph[0])

        # Gust Speed
        if max_gust_speed_kmph[0] == '':
            self.max_gust_speed_kmph = None
        else:
            self.max_gust_speed_kmph = float(max_gust_speed_kmph[0])

        # Precipitationmm
        if precipitationmm[0] == '':
            self.precipitationmm = None
        else:
            self.precipitationmm = float(precipitationmm[0])

        # Cloud Cover
        if cloud_cover[0] == '':
            self.cloud_cover = None
        else:
            self.cloud_cover = float(cloud_cover[0])

        # Events
        if events[0] == '':
            self.events = None
        else:
            self.events = events[0]

        # Wind Direction
        if wind_dir_degrees[0] == '':
            self.wind_dir_degrees = None
        else:
            self.wind_dir_degrees = wind_dir_degrees[0]

    def __str__(self):

        return "Date : " + str(self.date_pkt) + " Max Temprature: " \
               + str(self.max_temperature_c) + " Cloud Cover: " \
               + str(self.cloud_cover)
