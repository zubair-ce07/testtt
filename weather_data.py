class WeatherData:
    """
    weather_yearly_data
    Data Structure for saving
    { '2015':
              {
                'oct': [list of dictionaries of daily entries],
                'dec': [list of dictionaries daily entries]
              }
    }
    saves and maintain weather files data in above data structure
    """
    weather_yearly_data = {}
    years_added_so_far = set()
    single_month_weather_list = []

    def __init__(self, entry):
        WeatherData.add_weather_data(entry)

    @staticmethod
    def add_weather_data(entry):
        """
        :param entry: here entry is year from weather_files
        add year to weather_yearly_data and years_added_so_far
        ignores if already added
        :return:
        """
        if WeatherData.weather_yearly_data == {}:
            WeatherData.weather_yearly_data[entry] = {}
        elif entry not in WeatherData.weather_yearly_data.keys():
            WeatherData.weather_yearly_data[entry] = {}

        if entry not in WeatherData.years_added_so_far:
            WeatherData.years_added_so_far.add(entry)

    @staticmethod
    def append_single_list(string):
        """
        :param string: if given string is not empty, split it and add all
        entries to its respective key in dictionary
        and append in parent array
        :return:
        """
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
            daily_weather_entry = {'pkt': arr[0], 'max_temperature_c': max_temp,
                                   'mean_temperature_c': arr[2], 'min_temperature_c': min_temp,
                                   'dew_point_c': arr[4], 'mean_dev_point_c': arr[5],
                                   'min_dew_point_c': arr[6], 'max_humidity': max_humidity,
                                   'mean_humidity': arr[8], 'min_humidity': arr[9],
                                   'max_sea_level_pressure_hpa': arr[10],
                                   'mean_sea_level_pressure_hpa': arr[11],
                                   'min_sea_level_pressure_hpa': arr[12],
                                   'max_visibility_km': arr[13], 'mean_visibility_km': arr[14],
                                   'min_visibility_km': arr[15], 'max_wind_speed_kmh': arr[16],
                                   'mean_wind_speed_kmh': arr[17], 'max_gust_speed_kmh': arr[18],
                                   'precipitation_mm': arr[19], 'cloud_cover': arr[20],
                                   'events': arr[21], 'wind_dir_degree': arr[22]}
            WeatherData.single_month_weather_list.append(daily_weather_entry)

    @staticmethod
    def append_month_to_year(month, year, list_of_daily_weather_entry):
        """
        :param month:
        :param year: year from weather files
        :param list_of_daily_weather_entry: data structure
        to be appended in main WeatherData.weather_yearly_data
        if month is not added in year then add as dict
        :return:
        """
        if month not in WeatherData.weather_yearly_data[year].keys():
            WeatherData.weather_yearly_data[year] = dict(
                list(WeatherData.weather_yearly_data[year].items()) +
                list({month: list_of_daily_weather_entry}.items()))
