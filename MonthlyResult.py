"""This class hold Yearly Report obj with these fields required for Task1:
        high, low, mean_humidity
"""


class MonthlyResult:
    def __init__(self, high, low, humidity):
        self.highest_avg = high
        self.lowest_avg = low
        self.mean_humidity_avg = humidity

    def __str__(self):
        return 'Highest Average: ' + str(int(self.highest_avg)) + 'C' + '\nLowest Average: ' + \
               str(int(self.lowest_avg)) + 'C' + '\nAverage Mean Humidity: ' + str(int(self.mean_humidity_avg)) + 'C'
