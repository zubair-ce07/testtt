from termcolor import colored
from datetime import datetime


class DailyWeatherModel():
    def __init__(self, row_data):
        self.date = row_data[0]
        self.max_temperature = row_data[1]
        self.min_temperature = row_data[2]
        self.max_humidity = row_data[7]
        self.mean_humidity = row_data[8]

    def print_chart_string(self):
        components = datetime.strptime(self.date, "%Y-%m-%d")
        try:
            print(str(components.day), colored('+', 'red') * int(self.max_temperature), self.max_temperature + 'C')
        except:
            print(str(components.day), colored('Data N/A', 'red'))

        try:
            print(str(components.day), colored('+', 'blue') * int(self.min_temperature), self.min_temperature + 'C')
        except:
            print(str(components.day), colored('Data N/A', 'blue'))
