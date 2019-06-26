"""
This class hold weather obj with these fields required for Task1
        date, highest, lowest, max_humidity, mean_humidity
"""


class WeatherReading:
    def __init__(self, date, highest, lowest, humidity, mean_humidity):
        self.date = date
        self.highest = 0 if not highest else int(highest)
        self.lowest = 0 if not lowest else int(lowest)
        self.max_humidity = 0 if not humidity else int(humidity)
        self.mean_humidity = 0 if not mean_humidity else int(mean_humidity)
