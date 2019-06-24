
class WeatherReadings: # Class to store data

    def __init__(self, weather_reading):
        self.pkt = weather_reading['PKT']
        try:
            self.maxTemperature = weather_reading["Max TemperatureC"]
        except:
            self.maxTemperature = None
        try:
            self.minTemperature = weather_reading["Min TemperatureC"]
        except:
            self.minTemperature = None
        try:
            self.meanTemperature = weather_reading["Mean TemperatureC"]
        except:
            self.meanTemperature = None
        try:
            self.maxHumidity = weather_reading["Max Humidity"]
        except:
            self.maxHumidity = None
        try:
            self.minHumidity = weather_reading[" Min Humidity"]
        except:
            self.minHumidity = None
        try:
            self.meanHumidity = weather_reading[" Mean Humidity"]
        except:
            self.meanHumidity = None


