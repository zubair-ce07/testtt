from datetime import datetime


class DataSetRow:
    """DataSetRow represent the record in data-set"""
    def __init__(self, date, max_temp, min_temp, max_humidity, mean_humidity):
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.max_temp = int(max_temp)
        self.min_temp = int(min_temp)
        self.max_humidity = int(max_humidity)
        self.mean_humidity = int(mean_humidity)

