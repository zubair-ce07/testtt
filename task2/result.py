class Result:
    def __init__(self, month, year):
        self.month = month
        self.year = year
        self.min_temp = 0
        self.avg_temp = 0
        self.max_temp = 0

    def set_report(self, min_temp, avg_temp, max_temp):
        self.min_temp = min_temp
        self.avg_temp = avg_temp
        self.max_temp = max_temp