from datetime import datetime


class WeatherReading:

    def __init__(self, weather_reading):
        self.pkt = datetime.strptime(weather_reading.get('PKT') or weather_reading['PKST'], '%Y-%m-%d')
        self.max_temperature = int(weather_reading["Max TemperatureC"]) if weather_reading["Max TemperatureC"] else None
        self.min_temperature = int(weather_reading["Min TemperatureC"]) if weather_reading["Min TemperatureC"] else None
        self.mean_temperature = int(weather_reading["Mean TemperatureC"]) if weather_reading["Mean TemperatureC"] else None
        self.max_humidity = int(weather_reading["Max Humidity"]) if weather_reading["Max Humidity"] else None
        self.min_humidity = int(weather_reading[" Min Humidity"]) if weather_reading[" Min Humidity"] else None
        self.mean_humidity = int(weather_reading[" Mean Humidity"]) if weather_reading[" Mean Humidity"] else None
