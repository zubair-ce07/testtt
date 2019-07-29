
class WeatherResult:
    def __init__(self, max_temp="", max_avg_temp="", min_temp="", min_avg_temp="",
                 max_humidity="", mean_humidity=""):
        self.all_temp = []
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.max_avg_temp = max_avg_temp
        self.min_avg_temp = min_avg_temp
        self.mean_humidity = mean_humidity
