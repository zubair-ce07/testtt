""" This is class will receive the WeatherReading Obj of
    high, low and stores it as a Dictionary obj as highest, lowest, date for high and low WeatherReading obj
"""
import calendar
from _datetime import datetime


class ChartResult:
    def __init__(self, high, low):
        self.highest = {"highest": high.highest,
                        "lowest": high.lowest,
                        "date": high.date}
        self.lowest = {"highest": low.highest,
                       "lowest": low.lowest,
                       "date": low.date}

    def __str__(self):
        return \
            calendar.month_name[datetime.strptime(self.highest["date"], "%Y-%m-%d").month] + ' ' +\
            str(datetime.strptime(self.highest["date"], "%Y-%m-%d").year) + '\n' + "\033[95m" +\
            str(datetime.strptime(self.highest["date"], "%Y-%m-%d").day) +\
            ' \033[00m' +\
            '\033[94m+' * self.highest["lowest"] +\
            '\033[91m+\033[00m' * self.highest["highest"] +\
            "\033[95m " +\
            str(self.highest["lowest"]) + 'C - ' + str(self.highest["highest"]) + 'C' +\
            "\033[00m" +\
            "\033[95m" + '\n' +\
            str(datetime.strptime(self.lowest["date"], "%Y-%m-%d").day) +\
            " \033[00m" +\
            '\033[94m+' * self.lowest["lowest"] +\
            '\033[91m+\033[00m' * self.lowest["highest"] +\
            "\033[95m " +\
            str(self.lowest["lowest"]) + 'C - ' + str(self.lowest["highest"]) + 'C' +\
            "\033[00m"
