""" This is class will receive the WeatherReading Obj of
    high, low and stores it as a Dictionary obj as highest, lowest, date for high and low WeatherReading obj
"""
import calendar
from _datetime import datetime


class ChartResult:
    def __init__(self, high, low):
        self.highest = {"highest": high.highest,
                        "lowest": high.lowest,
                        "date": datetime.strptime(high.date, "%Y-%m-%d").date()}
        self.lowest = {"highest": low.highest,
                       "lowest": low.lowest,
                       "date": datetime.strptime(low.date, "%Y-%m-%d").date()}

    def print_chart(self, count, color_code, string):
        return '\033[00m' + color_code + string * count + '\033[00m'

    def __str__(self):
        return \
            self.highest["date"].strftime("%B") + ' ' + \
            str(self.highest["date"].strftime("%Y")) + '\n' + "\033[95m" +\
            self.print_chart(1, "\033[95m", str(self.highest["date"].day) + ' ') + \
            self.print_chart(self.highest["lowest"], '\033[94m', '+') + \
            self.print_chart(self.highest["highest"], '\033[91m', '+') + \
            self.print_chart(1, "\033[95m ", str(self.highest["lowest"]) + 'C - ' + str(self.highest["highest"]) + 'C') +\
            self.print_chart(1,  "\033[95m", '\n' + str(self.lowest["date"].day) + ' ') +\
            self.print_chart(self.lowest["lowest"], '\033[94m', '+') + \
            self.print_chart(self.lowest["highest"], '\033[91m', '+') + \
            self.print_chart(1, "\033[95m ", str(self.lowest["lowest"]) + 'C - ' + str(self.lowest["highest"]) + 'C')
