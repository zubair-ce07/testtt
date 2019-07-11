from datetime import datetime
import os
import re

class WeatherReading:
    def __init__(self, data):
        date = data.get("PKT", data.get("PKST"))
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.highest_temp = int(data["Max TemperatureC"])
        self.lowest_temp = int(data["Min TemperatureC"])
        self.avg_humidity = int(data[" Mean Humidity"])
        self.highest_humidity = int(data["Max Humidity"])