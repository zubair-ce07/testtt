class WeatherEntity:

    __list_of_weather_entities = []

    def __init__(self, string):
        # if given str is not empty, split it and all
        # entries to its respective key in dictionary
        # and append in parent array
        if not string == "":
            arr = string.split(',')
            arr[-1] = arr[-1].split('\n')[0]
            obj = dict(pkt=arr[0], temperature_c=arr[1],
                       min_temperature_c=arr[2], dew_point_c=arr[3],
                       mean_dev_point_c=arr[4], min_dew_point_c=arr[5],
                       max_humidity=arr[6], mean_humidity=arr[7],
                       min_humidity=arr[8], max_sea_level_pressure_hpa=arr[9],
                       mean_sea_level_pressure_hpa=arr[10], min_sea_level_pressure_hpa=arr[11],
                       max_visibility_km=arr[12], mean_visibility_km=arr[13],
                       min_visibility_km=arr[14], max_wind_speed_kmh=arr[15],
                       mean_wind_speed_kmh=arr[16], max_gust_speed_kmh=arr[17],
                       precipitationmm=arr[18], cloud_cover=arr[19], events=arr[20],
                       wind_dir_degree=arr[21]
                       )
            WeatherEntity.__list_of_weather_entities.append(obj)

    @staticmethod
    def get_data():
        return WeatherEntity.__list_of_weather_entities

    @staticmethod
    def clear():
        WeatherEntity.__list_of_weather_entities = []
