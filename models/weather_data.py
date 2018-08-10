class WeatherData:
    __data = {}
    __years_added = set()
    single_list = []

    # Data Structure for saving
    # { '2015':
    #           {
    #             'oct': [list of dictionaries of daily entries],
    #             'dec': [list of dictionaries daily entries]
    #           }
    # }

    def __init__(self, entry):
        WeatherData.__add_weather_data(entry)

    @staticmethod
    def __add_weather_data(entry):
        # add year in master data structure and if already added do nothing
        if WeatherData.__data == {}:
            WeatherData.__data[entry] = {}
        elif entry not in WeatherData.__data.keys():
            WeatherData.__data[entry] = {}
        if entry not in WeatherData.__years_added:
            WeatherData.__years_added.add(entry)

    @staticmethod
    def append_single_list(string):
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
            WeatherData.single_list.append(obj)


    @staticmethod
    def get_data(key=None):
        if key is None:
            return WeatherData.__data
        else:
            if key in WeatherData.__data:
                return WeatherData.__data[key]
        return None

    @staticmethod
    def get_years():
        return list(WeatherData.__years_added)

    @staticmethod
    def add_array_to_key(arr, key, entry, weather_entity_data):
        # add data in month of year
        if key not in WeatherData.__data[entry].keys():
            arr[list(arr.keys())[0]] = weather_entity_data
            WeatherData.__data[entry] = dict(list(WeatherData.__data[entry].items()) + list(arr.items()))

    @staticmethod
    def print_specific_key(key):
        if key in WeatherData.__data:
            print(WeatherData.__data[key])

    @staticmethod
    def print_():
        print(WeatherData.__data)
        for k, v in sorted(WeatherData.__data.items()):
            print(k)
            for month_k, month_v in v.items():
                print("\t", end='')
                print(month_k, month_v)
