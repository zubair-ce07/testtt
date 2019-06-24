"""
This class hold Yearly Report obj with these fields required for Task1:
    high,
    low,
    max_humidity

"""
import calendar
from _datetime import datetime


class YearlyResult:
    def __init__(self, high, low, humidity):
        self.highest = {"highest": high.highest,
                        "date": high.date}
        self.lowest = {"lowest": low.lowest,
                       "date": low.date}
        self.max_humidity = {"max_humidity": humidity.max_humidity,
                             "date": humidity.date}

    def __str__(self):
        return f'Highest:' \
            f' {self.highest["highest"]} on' \
            f' {calendar.month_name[datetime.strptime(self.highest["date"], "%Y-%m-%d").month]}' \
            f' {datetime.strptime(self.highest["date"], "%Y-%m-%d").day}' + \
            f'\nLowest:'\
            f' {self.lowest["lowest"]} on' \
            f' {calendar.month_name[datetime.strptime(self.lowest["date"], "%Y-%m-%d").month]}' \
            f' {datetime.strptime(self.lowest["date"], "%Y-%m-%d").day}' + \
            f'\nHumidity:'\
            f' {self.max_humidity["max_humidity"]} on' \
            f' {calendar.month_name[datetime.strptime(self.max_humidity["date"], "%Y-%m-%d").month]}' \
            f' {datetime.strptime(self.max_humidity["date"], "%Y-%m-%d").day}\n'
