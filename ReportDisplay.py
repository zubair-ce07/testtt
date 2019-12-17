from termcolor import colored, cprint


class Results:
    def __init__(self):
        self.highest_temperature_monthly = []
        self.lowest_temperature_monthly = []
        self.highest_temperature = 0
        self.lowest_temperature = 0
        self.highest_humidity = 0

        self.average_highest_temperature = 0
        self.average_lowest_temperature = 0
        self.average_humidity = 0

    def display_report_A(self):
        print(f"Highest Average: {self.average_highest_temperature:.1f}C")
        print(f"Lowest Average: {self.average_lowest_temperature:.1f}C")
        print(f"Average Mean Humidity: {self.average_humidity:.1f}%")

    def display_report_C(self):
        for index in range(len(self.highest_temperature_monthly)):
            print(f"{index+1} ", end='')

            for value in range(0, self.lowest_temperature_monthly[index]):
                cprint('+', 'blue', end='')

            for value in range(0, self.highest_temperature_monthly[index]):
                cprint('+', 'red', end='')

            print(
                f" {self.lowest_temperature_monthly[index]}C-", end='', sep='')
            print(
                f"{self.highest_temperature_monthly[index]}C", sep='')

    def display_report_E(self):
        print(f"Highest: {self.highest_temperature}C")
        print(f"Lowest: {self.lowest_temperature}C")
        print(f"Humidity: {self.highest_humidity}%")
