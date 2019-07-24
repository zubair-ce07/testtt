"""
This class hold weather obj with these fields required for Task1
        date, highest, lowest, max_humidity, mean_humidity
"""


class WeatherReading:
    def __init__(self, date, highest, lowest, humidity, mean_humidity):
        self.date = date
        self.highest = int(highest) if highest else 0
        self.lowest = int(lowest) if lowest else 0
        self.max_humidity = int(humidity) if humidity else 0
        self.mean_humidity = int(mean_humidity) if mean_humidity else 0
