from models.WeatherData import WeatherData
from models.MonthlyWeatherData import MonthlyWeatherData


class YearlyWeatherData(WeatherData):

    def __init__(self, year, month, weather_entity_data):
        # add year, month and date-wise month entries
        WeatherData.__init__(self, year)
        YearlyWeatherData.__add_month(month, year, weather_entity_data)

    @staticmethod
    def __add_month(month, year, weather_entity_data):
        MonthlyWeatherData(month, year, weather_entity_data)
