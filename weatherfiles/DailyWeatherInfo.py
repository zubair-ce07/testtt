

class DailyWeatherInfo:
    def __init__(self, weather_info_string):
        weather_info = weather_info_string.split(',')
        self.date = weather_info[0]
        self.max_temp = get_int(weather_info[1])
        self.mean_temp = get_int(weather_info[2])
        self.min_temp = get_int(weather_info[3])
        self.max_humidity = get_int(weather_info[7])
        self.mean_humidity = get_int(weather_info[8])
        self.min_humidity = get_int(weather_info[9])


def get_int(string):
    if (string):
        return int(string)
    return None
