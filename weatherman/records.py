class Records:
    """class for holding the required data"""

    def __init__(self, d, max_t, mean_t, min_t, max_h, mean_h, min_h):
        self.date = d
        self.max_temperature = int(max_t) if max_t else None
        self.mean_temperature = int(mean_t) if mean_t else None
        self.min_temperature = int(min_t) if min_t else None
        self.max_humidity = int(max_h) if max_h else None
        self.mean_humdity = int(mean_h) if mean_h else None
        self.min_humidity = int(min_h) if min_h else None
