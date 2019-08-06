class Reading:
    def __init__(self, pkt, max_temperature_c, mean_temperature_c, min_temperature_c,
                 dew_point_c, mean_dew_point_c, min_dew_point_c,
                 max_humidity, mean_humidity, min_humidity,
                 max_sealevel_pressure_hpa, mean_sealevel_pressure_hpa, min_sealevel_pressure_hpa,
                 max_visibility_km, mean_visibility_km, min_visibility_km,
                 max_windspeed_kmh, mean_windspeed_kmh, max_gustspeed_kmh, precipitation_mm,
                 cloud_cover, events, wind_dir_degrees):
        self.pkt = pkt
        self.max_temperature_c = max_temperature_c
        self.mean_temperature_c = mean_temperature_c
        self.min_temperature_c = min_temperature_c
        self.dew_point_c = dew_point_c
        self.mean_dew_point_c = mean_dew_point_c
        self.mean_dew_point_c = min_dew_point_c
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.min_humidity = min_humidity
        self.max_sealevel_pressure_hpa = max_sealevel_pressure_hpa
        self.mean_sealevel_pressure_hpa = mean_sealevel_pressure_hpa
        self.min_sealevel_pressure_hpa = min_sealevel_pressure_hpa
        self.max_visibility_km = max_visibility_km
        self.mean_visibility_km = mean_visibility_km
        self.min_visibility_km = min_visibility_km
        self.max_windspeed_kmh = max_windspeed_kmh
        self.mean_windspeed_kmh = mean_windspeed_kmh
        self.max_gustspeed_kmh = max_gustspeed_kmh
        self.precipitation_mm = precipitation_mm
        self.cloud_cover = cloud_cover
        self.events = events
        self.wind_dir_degrees = wind_dir_degrees
