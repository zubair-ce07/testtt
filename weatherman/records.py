class Records:
    """class for holding the required data"""

    def __init__(self, d, max_t, mean_t, min_t, max_h, mean_h, min_h):
        self.date = d
        self.max_temperature = max_t
        self.mean_temperature = mean_t
        self.min_temperature = min_t
        self.max_humidity = max_h
        self.mean_humdity = mean_h
        self.min_humidity = min_h
