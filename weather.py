
class WeatherRecord(object):
    def __init__(self, date, max_temp, low_temp, max_humid, mean_humid):
        self.date = date
        self.max_temp = int(max_temp)
        self.low_temp = int(low_temp)
        self.max_humid = int(max_humid)
        self.mean_humid = int(mean_humid)
