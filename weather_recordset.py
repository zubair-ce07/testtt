class WeatherRecord:
    def __init__(self, weather_date, h_temperature, l_temperature, mean_temperature, max_humidity, mean_humidity):
        self.weather_record_date = weather_date
        self.highest_temperature = h_temperature
        self.lowest_temperature = l_temperature
        self.mean_temperature = mean_temperature
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
