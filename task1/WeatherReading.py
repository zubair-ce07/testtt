
class WeatherReadings: # Class to store data

    def __init__(self, weather_reading):
        self.pkt = weather_reading['PKT']
        self.max_temperature = weather_reading.get("Max TemperatureC")
        try:
            self.min_temperature = weather_reading["Min TemperatureC"]
        except:
            self.min_temperature = None
        try:
            self.mean_temperature = weather_reading["Mean TemperatureC"]
        except:
            self.mean_temperature = None
        try:
            self.max_humidity = weather_reading["Max Humidity"]
        except:
            self.max_humidity = None
        try:
            self.min_humidity = weather_reading[" Min Humidity"]
        except:
            self.min_humidity = None
        try:
            self.mean_humidity = weather_reading[" Mean Humidity"]
        except:
            self.mean_humidity = None
