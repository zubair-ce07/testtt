class WeatherResult:
    def __init__(self, max_temperature_record="", min_temperature_record="",
                 max_humidity_record="", avg_max_temperature="",
                 avg_min_temperature="", mean_humidity_avg=""):
        self.max_temperature_record = max_temperature_record
        self.min_temperature_record = min_temperature_record
        self.max_humidity_record = max_humidity_record
        self.avg_max_temperature = avg_max_temperature
        self.avg_min_temperature = avg_min_temperature
        self.mean_humidity_avg = mean_humidity_avg
