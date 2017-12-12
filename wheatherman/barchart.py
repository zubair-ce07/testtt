class Barchart:
    def __init__(self, bar_min, bar_max, max_temp, min_temp, date):
        self.bar_min = bar_min
        self.bar_max = bar_max
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.chart_date = date

    def bar_min(self):
        return self.bar_min

    def bar_max(self):
        return self.bar_max()

    def max_temp(self):
        return self.max_temp

    def min_temp(self):
        return self.min_temp

    def chart_date(self):
        return self.chart_date
