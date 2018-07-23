import time


class WeatherReading:
    def __init__(self, day):
        self.date = time.strptime(day.get('PKT') or day.get('PKST'), "%Y-%m-%d")
        self.highest_temp = int(day["Max TemperatureC"])
        self.lowest_temp = int(day["Min TemperatureC"])
        self.mean_temp = int(day["Mean TemperatureC"])
        self.highest_hum = int(day["Max Humidity"])
        self.lowest_hum = int(day[" Min Humidity"])
        self.mean_hum = int(day[" Mean Humidity"])
