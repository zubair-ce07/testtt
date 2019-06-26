from datetime import datetime


class MonthlyResult:
    def __init__(self, high, low, humidity):
        self.highest_avg = high
        self.lowest_avg = low
        self.mean_humidity_avg = humidity

    def __str__(self):
        return 'Highest Average: ' + str(int(self.highest_avg)) + 'C' + '\nLowest Average: ' + \
               str(int(self.lowest_avg)) + 'C' + '\nAverage Mean Humidity: ' + str(int(self.mean_humidity_avg)) + 'C'


class ChartResult:
    def __init__(self, high, low):
        self.highest = {"highest": high.highest,
                        "lowest": high.lowest,
                        "date": datetime.strptime(high.date, "%Y-%m-%d").date()}
        self.lowest = {"highest": low.highest,
                       "lowest": low.lowest,
                       "date": datetime.strptime(low.date, "%Y-%m-%d").date()}

    @staticmethod
    def print_chart(model):
        return '\033[00m' + '\033[95m' + str(model["date"].day) + ' \033[00m' +\
               '\033[94m' '+' * abs(model["lowest"]) + '\033[00m' + '\033[91m' '+' * model["highest"] + '\033[00m ' + \
               '\033[95m' + str(model["lowest"]) + 'C - ' + str(model["highest"]) + 'C\033[00m\n'

    def __str__(self):
        return \
            self.print_chart(self.lowest) +\
            self.print_chart(self.highest)


class YearlyResult:
    def __init__(self, high, low, humidity):
        self.highest = {"highest": high.highest,
                        "date": datetime.strptime(high.date, "%Y-%m-%d").date()}
        self.lowest = {"lowest": low.lowest,
                       "date": datetime.strptime(low.date, "%Y-%m-%d").date()}
        self.max_humidity = {"max_humidity": humidity.max_humidity,
                             "date": datetime.strptime(humidity.date, "%Y-%m-%d").date()}

    def __str__(self):
        return f'Highest:' \
            f' {self.highest["highest"]} on' \
            f' {self.highest["date"].strftime("%B")}' \
            f' {self.highest["date"].day}' + \
            f'\nLowest:'\
            f' {self.lowest["lowest"]} on' \
            f' {self.lowest["date"].strftime("%B")}' \
            f' {self.lowest["date"].day}' + \
            f'\nHumidity:'\
            f' {self.max_humidity["max_humidity"]} on' \
            f' {self.max_humidity["date"].strftime("%B")}' \
            f' {self.max_humidity["date"].day}\n'
