class ResultSet:

    def __init__(self,
                 date=None,
                 max_temperature_reading=None,
                 average_max_temperature=None,
                 min_temperature_reading=None,
                 average_min_temperature=None,
                 max_humidity_reading=None,
                 average_mean_humidity=None):
        self.date = date
        self.max_temperature_reading = max_temperature_reading
        self.min_temperature_reading = min_temperature_reading
        self.max_humidity_reading = max_humidity_reading
        self.average_mean_humidity = average_mean_humidity
        self.average_max_temperature = average_max_temperature
        self.average_min_temperature = average_min_temperature
