from datetime import datetime


class WeatherData:
    def __init__(self, data):
        date = data.get("PKT", data.get('PKST'))
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.max_temp = int(data["Max TemperatureC"])
        self.min_temp = int(data["Min TemperatureC"])
        self.mean_temp = int(data["Mean TemperatureC"])
        self.max_humidity = float(data["Max Humidity"])
        self.mean_humidity = float(data[" Min Humidity"])
