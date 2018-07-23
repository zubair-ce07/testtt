class WeatherResult:
    def __init__(self, highest_temperature_record="", max_avg_temperature_record="",
                 lowest_temperature_record="", min_avg_temperature_record="",
                 max_humidity_record_record="", mean_humidity=""):
        self.max_temperature_record = highest_temperature_record
        self.min_temperature_record = lowest_temperature_record
        self.max_humidity_record = max_humidity_record_record
        self.max_avg_temperature_record = max_avg_temperature_record
        self.min_avg_temperature_record = min_avg_temperature_record
        self.mean_humidity = mean_humidity
        self.daily_temperatures = []
