"""
This class hold weather obj with these fields required for Task1
        date,
        highest,
        lowest,
        max_humidity,
        mean_humidity
"""


class WeatherDS:
    def __init__(self, date, highest, lowest, humidity, mean_humidity):
        self.date = date
        self.highest = highest
        self.lowest = lowest
        self.max_humidity = humidity
        self.mean_humidity = mean_humidity
