"""
class WeatherData
saves and maintain weather files data in weather_yearly_data data structure
"""


class WeatherData:
    """
    Data Structure for saving
    { '2015':
              {
                'oct': [list of dictionaries of daily entries],
                'dec': [list of dictionaries daily entries]
              }
    }
    """
    yearly = {}
    years_added_so_far = set()

    def __init__(self, year):
        """
        add weather data by year on Initializing
        :param year:
        """

        if not WeatherData.yearly.get(year):
            WeatherData.yearly[year] = {}

        if year not in WeatherData.years_added_so_far:
            WeatherData.years_added_so_far.add(year)

    @staticmethod
    def daily_weather_entry(weather_entry_string):
        """
        :param weather_entry_string: if given string is not empty, split it and add all
        entries to its respective key in dictionary
        and append in parent array
        :return:
        """
        if weather_entry_string.strip():
            arr = weather_entry_string.split(',')
            if arr:
                # defining variables to increase code readability
                date = arr[0]
                max_temp = 0.0
                min_temp = 0.0
                max_humidity = 0.0
                mean_temp = arr[2]
                dew_point = arr[4]
                mean_dew_point = arr[5]
                min_dew_point = arr[6]
                mean_humidity = arr[8]
                min_humidity = arr[9]
                max_sealevel_pressure = arr[10]
                mean_sealevel_pressure = arr[11]
                min_sealevel_pressure = arr[12]
                max_visibility_km = arr[13]
                mean_visibility_km = arr[14]
                min_visibility_km = arr[15]
                max_wind_speed_kmh = arr[16]
                mean_wind_speed_kmh = arr[17]
                max_gust_speed_kmh = arr[18]
                precipitation_mm = arr[19]
                cloud_cover = arr[20]
                events = arr[21]
                wind_dir_degree = arr[22]

                arr[-1] = arr[-1].split('\n')[0]

                if arr[1]:
                    max_temp = float(arr[1])

                if arr[3]:
                    min_temp = float(arr[3])

                if arr[7]:
                    max_humidity = float(arr[7])

                daily_weather_entry = {'pkt': date, 'max_temperature_c': max_temp,
                                       'mean_temperature_c': mean_temp,
                                       'min_temperature_c': min_temp, 'dew_point_c': dew_point,
                                       'mean_dev_point_c': mean_dew_point,
                                       'min_dew_point_c': min_dew_point,
                                       'max_humidity': max_humidity,
                                       'mean_humidity': mean_humidity, 'min_humidity': min_humidity,
                                       'max_sea_level_pressure_hpa': max_sealevel_pressure,
                                       'mean_sea_level_pressure_hpa': mean_sealevel_pressure,
                                       'min_sea_level_pressure_hpa': min_sealevel_pressure,
                                       'max_visibility_km': max_visibility_km,
                                       'mean_visibility_km': mean_visibility_km,
                                       'min_visibility_km': min_visibility_km,
                                       'max_wind_speed_kmh': max_wind_speed_kmh,
                                       'mean_wind_speed_kmh': mean_wind_speed_kmh,
                                       'max_gust_speed_kmh': max_gust_speed_kmh,
                                       'precipitation_mm': precipitation_mm,
                                       'cloud_cover': cloud_cover, 'events': events,
                                       'wind_dir_degree': wind_dir_degree}
                return daily_weather_entry

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
        if not WeatherData.yearly.get(year).get(month):
            WeatherData.yearly[year].update({month: list_of_daily_weather_entry})
