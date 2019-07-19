class HighLowResult:
    def __init__(self, max_temp_record, max_humidity_record, min_temp_record):
        self.max_temp_record = max_temp_record
        self.max_humidity_record = max_humidity_record
        self.min_temp_record = min_temp_record


class AvgTemperatureResult:
    def __init__(self, avg_max_temp, avg_mean_humidity, avg_min_temp):
        self.avg_max_temp = avg_max_temp
        self.avg_mean_humidity = avg_mean_humidity
        self.avg_min_temp = avg_min_temp
