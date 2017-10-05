from DailyWeatherInfo import DailyWeatherInfo


class MonthlyWeatherInfo:
    def __init__(self, weather_info_list):
        del (weather_info_list[0])
        self.month = weather_info_list[0].split(',')[0]
        self.daily_weathers_info = [DailyWeatherInfo(weather_info) for weather_info in weather_info_list]