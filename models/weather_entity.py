class WeatherEntity:
    """

    """
    __list_of_weather_entities = []

    def __init__(self, string):
        # if given str is not empty, split it and all
        # entries to its respective key in dictionary
        # and append in parent array
        if not string == "":
            arr = string.split(',')
            arr[-1] = arr[-1].split('\n')[0]
            if arr[1] == '' or arr[1] is None:
                max_temp = 0.0
            else:
                max_temp = float(arr[1])

            if arr[3] == '' or arr[3] is None:
                min_temp = 0.0
            else:
                min_temp = float(arr[3])

            if arr[7] == '' or arr[7] is None:
                max_humidity = 0.0
            else:
                max_humidity = float(arr[7])
            obj = {'pkt': arr[0], 'max_temperature_c': max_temp, 'mean_temperature_c': arr[2],
                   'min_temperature_c': min_temp, 'dew_point_c': arr[4], 'mean_dev_point_c': arr[5],
                   'min_dew_point_c': arr[6], 'max_humidity': max_humidity, 'mean_humidity': arr[8],
                   'min_humidity': arr[9], 'max_sea_level_pressure_hpa': arr[10],
                   'mean_sea_level_pressure_hpa': arr[11], 'min_sea_level_pressure_hpa': arr[12],
                   'max_visibility_km': arr[13], 'mean_visibility_km': arr[14], 'min_visibility_km': arr[15],
                   'max_wind_speed_kmh': arr[16], 'mean_wind_speed_kmh': arr[17], 'max_gust_speed_kmh': arr[18],
                   'precipitation_mm': arr[19], 'cloud_cover': arr[20], 'events': arr[21], 'wind_dir_degree': arr[22]}
            WeatherEntity.__list_of_weather_entities.append(obj)

    @staticmethod
    def get_data():
        return WeatherEntity.__list_of_weather_entities

    @staticmethod
    def clear():
        WeatherEntity.__list_of_weather_entities = []
