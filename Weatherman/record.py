from datetime import datetime


class Record:
    '''represents a row in the dataset'''

    def __init__(self, date, max_temp, min_temp, max_humidity, mean_humidity):

        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.max_temp = int(max_temp) if max_temp.isdigit() else max_temp
        self.min_temp = int(min_temp) if min_temp.isdigit() else min_temp
        self.max_humidity = int(
            max_humidity) if max_humidity.isdigit() else max_humidity
        self.mean_humidity = int(
            mean_humidity) if mean_humidity.isdigit() else mean_humidity
