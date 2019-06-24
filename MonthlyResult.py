"""
    This class hold Yearly Report obj with these fields required for Task1:
        high,
        low,
        mean_humidity

"""


class MonthlyResult:
    def __init__(self, high, low, humidity):
        self.highest_avg = high
        self.lowest_avg = low
        self.mean_humidity_avg = humidity

    def __str__(self):
        return 'Highest Average: ' + str(self.highest_avg) + '\nLowest Average: ' + str(self.lowest_avg) +\
               '\nAverage Mean Humidity: ' + str(self.mean_humidity_avg)
