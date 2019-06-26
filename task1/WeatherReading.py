

class WeatherReading:

    def __init__(self, weather_reading):
        self.pkt = weather_reading['PKT']
        self.max_temperature = weather_reading.get("Max TemperatureC")
        self.min_temperature = weather_reading.get("Min TemperatureC")
        self.mean_temperature = weather_reading.get("Mean TemperatureC")
        self.max_humidity = weather_reading.get("Max Humidity")
        self.min_humidity = weather_reading.get(" Min Humidity")
        self.mean_humidity = weather_reading.get(" Mean Humidity")
