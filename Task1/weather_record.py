import datetime


class WeatherRecord:
    def __init__(self, weather_date, highest_temperature, lowest_temperature, mean_temperature,
                 max_humidity, mean_humidity):
        self.weather_record_date = datetime.datetime.strptime(weather_date, "%Y-%m-%d").date()
        self.highest_temperature = int(highest_temperature)
        self.lowest_temperature = int(lowest_temperature)
        self.mean_temperature = float(mean_temperature)
        self.max_humidity = float(max_humidity)
        self.mean_humidity = float(mean_humidity)
