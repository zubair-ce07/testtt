import math
from datetime import datetime


class Reports:

    CRED = '\033[91m'
    CEND = '\033[0m'
    CBLUE = '\33[34m'

    def report_year(self, calculations):

        date = (datetime.strptime(calculations['Max Temp Day'], '%Y-%m-%d')
                if calculations['Max Temp Day'] else None)
        print(f"Highest: {calculations['Max Temperature']}C on {date.strftime('%b')} {date.strftime('%d')}"
              if date else f"Highest: None")

        date = (datetime.strptime(calculations['Min Temp Day'], '%Y-%m-%d')
                if calculations['Min Temp Day'] else None)
        print(f"Lowest: {calculations['Min Temperature']}C on {date.strftime('%b')} {date.strftime('%d')}"
              if date else f"Lowest: None")

        date = (datetime.strptime(calculations['Max Humidity Day'], '%Y-%m-%d')
                if calculations['Max Humidity Day'] else None)
        print(f"Humidity: {calculations['Max Humidity']}% on {date.strftime('%b')} {date.strftime('%d')}"
              if date else f"Humidity: None")

    def report_month(self, calculations):
        print(f"Highest Average: {int(calculations['Avg Max Temp'])}C"
              if calculations['Avg Max Temp'] else f"Highest Average: None")
        print(f"Lowest Average: {int(calculations['Avg Min Temp'])}C"
              if calculations['Avg Min Temp'] else f"Lowest Average: None")
        print(f"Average Mean Humidity: {int(calculations['Avg Mean Humidity'])}%"
              if calculations['Avg Mean Humidity'] else f"Average Mean Humidity: None")

    def plot_month(self, records):
        for reading in records:
            if reading['Max TemperatureC'] and reading['Min TemperatureC']:
                date = (datetime.strptime(reading.get('PKT', reading.get('PKST')), '%Y-%m-%d'))

                print(
                    f"{date.strftime('%d')}"
                    f" {self.CRED}{reading['Max TemperatureC'] * '+'}{self.CEND}"
                    f" {reading['Max TemperatureC']}C"
                    )
                print(
                    f"{date.strftime('%d')}"
                    f" {self.CBLUE}{reading['Min TemperatureC'] * '+'}{self.CEND}"
                    f" {reading['Min TemperatureC']}C"
                    )

    def plot_month_horizontal(self, records):
        for reading in records:
            if reading['Max TemperatureC'] and reading['Min TemperatureC']:
                date = (datetime.strptime(reading.get('PKT', reading.get('PKST')), '%Y-%m-%d'))
                print(
                    f"{date.strftime('%d')} "
                    f"{self.CBLUE}{reading['Min TemperatureC'] * '+'}{self.CEND}"
                    f"{self.CRED}{reading['Max TemperatureC'] * '+'}{self.CEND} "
                    f"{reading['Min TemperatureC']}C-{reading['Max TemperatureC']}C"
                    )
