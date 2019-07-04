

class WeatherReading:

    def __init__(self, weather_reading):
        self.pkt = weather_reading.get('PKT')
        self.max_temperature = int(weather_reading.get("Max TemperatureC")) if weather_reading.get("Max TemperatureC") else None
        self.min_temperature = int(weather_reading.get("Min TemperatureC")) if weather_reading.get("Min TemperatureC") else None
        self.mean_temperature = int(weather_reading.get("Mean TemperatureC")) if weather_reading.get("Mean TemperatureC") else None
        self.max_humidity = int(weather_reading.get("Max Humidity")) if weather_reading.get("Max Humidity") else None
        self.min_humidity = int(weather_reading.get(" Min Humidity")) if weather_reading.get(" Min Humidity") else None
        self.mean_humidity = int(weather_reading.get(" Mean Humidity")) if weather_reading.get(" Mean Humidity") else None
