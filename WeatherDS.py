class WeatherDS:
    date = None
    highest = None
    lowest = None
    max_humidity = None
    mean_humidity = None

    def __init__(self, date, highest, lowest, humidity, mean_humidity):
        self.date = date
        self.highest = highest
        self.lowest = lowest
        self.max_humidity = humidity
        self.mean_humidity = mean_humidity


