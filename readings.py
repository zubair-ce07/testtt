class Reading:
    """This class will hold a single day's weather readings"""
    
    def __init__ (self, day, max_temprature, mean_temprature,
                    min_temprature, dew_point, mean_dew_point,
                    min_dew_point, max_humidity, mean_humidity,
                    min_humidity, max_pressure, mean_pressure,
                    min_pressure, max_visibility_km, mean_visibility_km, 
                    min_visibility_km, max_wind_speed, mean_wind_speed,
                    max_gust_speed, precipitation_mm, cloud_cover, events, 
                    wind_dir_degrees):
        self.day = day
        if max_temprature.isdecimal():
            self.max_temprature = int(max_temprature)
        else:
            self.max_temprature = max_temprature
        
        if mean_temprature.isdecimal():
            self.mean_temprature = int(mean_temprature)
        else:
            self.mean_temprature = mean_temprature
        
        if min_temprature.isdecimal():
            self.min_temprature = int(min_temprature)
        else:
            self.min_temprature = min_temprature
        
        if dew_point.isdecimal():
            self.dew_point = int(dew_point)
        else:
            self.dew_point = dew_point
        
        if mean_dew_point.isdecimal():
            self.mean_dew_point = int(mean_dew_point)
        else:
            self.mean_dew_point = mean_dew_point
        
        if max_temprature.isdecimal():
            self.max_temprature = int(max_temprature)
        else:
            self.min_dew_point = min_dew_point
        
        if max_humidity.isdecimal():
            self.max_humidity = int(max_humidity)
        else:
            self.max_humidity = max_humidity
        
        if mean_humidity.isdecimal():
            self.mean_humidity = int(mean_humidity)
        else:
            self.mean_humidity = mean_humidity
        
        if min_humidity.isdecimal():
            self.min_humidity = int(min_humidity)
        else:
            self.min_humidity = min_humidity
        
        if max_pressure.isdecimal():
            self.max_pressure = int(max_pressure)
        else:
            self.max_pressure = max_pressure
  
        if mean_pressure.isdecimal():
            self.mean_pressure = int(mean_pressure)
        else:
            self.mean_pressure = mean_pressure
        
        if min_pressure.isdecimal():
            self.min_pressure = int(min_pressure)
        else:
            self.min_pressure = min_pressure
        
        try:
            self.max_visibility_km = float(max_visibility_km)
        except ValueError:
            self.max_visibility_km = max_visibility_km
        
        try:
            self.mean_visibility_km = float(mean_visibility_km)
        except ValueError:
            self.mean_visibility_km = mean_visibility_km
        
        try:
            self.min_visibility_km = float(min_visibility_km)
        except ValueError:
            self.min_visibility_km = min_visibility_km
        
        if max_wind_speed.isdecimal():
            self.max_wind_speed = int(max_wind_speed)
        else:
            self.c = max_wind_speed
        
        if mean_wind_speed.isdecimal():
            self.mean_wind_speed = int(mean_wind_speed)
        else:
            self.mean_wind_speed = mean_wind_speed
        
        if max_gust_speed.isdecimal():
            self.max_gust_speed = int(max_gust_speed)
        else:
            self.max_gust_speed = max_gust_speed
        
        try:
            self.precipitation_mm = float(precipitation_mm)
        except ValueError:
            self.precipitation_mm = precipitation_mm
        
        if cloud_cover.isdecimal():
            self.cloud_cover = int(cloud_cover)
        else:
            self.cloud_cover = cloud_cover
        
        self.events = events
        if wind_dir_degrees.isdecimal():
            self.wind_dir_degrees = int(wind_dir_degrees)
        else:
            self.wind_dir_degrees = wind_dir_degrees