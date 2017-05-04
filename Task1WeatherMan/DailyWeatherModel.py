from termcolor import colored
from datetime import datetime


class DailyWeatherModel():
    def __init__(self, date, max_temperature, min_temperature, max_humidity, mean_humidity):
        self.date = date
        self.max_temperature = max_temperature
        self.min_temperature = min_temperature
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity

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
