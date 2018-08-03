import datetime


class Record:
    def __init__(self, date, max_temp, min_temp, max_humid, mean_humid):
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d')
        self.max_temp = int(max_temp)
        self.min_temp = int(min_temp)
        self.max_humid = int(max_humid)
        self.mean_humid = int(mean_humid)
