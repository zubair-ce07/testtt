from datetime import datetime


class WeatherData:

    def __init__(self, data):

        self.date = datetime.strptime(data.get('PKT'), '%Y-%m-%d')
        self.highest_temp = int(data["Max TemperatureC"]) if data["Max TemperatureC"] else None
        self.lowest_temp = int(data["Min TemperatureC"]) if data["Min TemperatureC"] else None
        self.highest_humidity = int(data["Max Humidity"]) if data["Max Humidity"] else None
        self.avg_humidity = int(data[" Mean Humidity"]) if data[" Mean Humidity"] else None

