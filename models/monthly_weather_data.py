from models.weather_data import WeatherData


class MonthlyWeatherData:

    def __init__(self, month, year, weather_entity_data):
        self.data = {month: []}
        # adding year, month and date-wise entries in month dict
        WeatherData.add_array_to_key(self.data, month, year, weather_entity_data)
