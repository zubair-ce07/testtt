class DailyWeatherModel:
    def __init__(self, date, max_temperature, min_temperature, max_humidity, mean_humidity):
        self.date = date
        self.max_temperature = max_temperature
        self.min_temperature = min_temperature
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
