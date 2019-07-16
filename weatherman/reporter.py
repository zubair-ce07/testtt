from datetime import datetime
import math


class Reporter:

    CRED = '\033[91m'
    CEND = '\033[0m'
    CBLUE = '\33[34m'

    def yearly_report(self, yearly_calculations):
        date = datetime.strptime(yearly_calculations['Max Temp Day'], '%Y-%m-%d')
        print(f"Highest: {yearly_calculations['Max Temperature']}C on {date.strftime('%b')} {date.strftime('%d')}")

        date = datetime.strptime(yearly_calculations['Min Temp Day'], '%Y-%m-%d')
        print(f"Lowest: {yearly_calculations['Min Temperature']}C on {date.strftime('%b')} {date.strftime('%d')}")

        date = datetime.strptime(yearly_calculations['Max Humidity Day'], '%Y-%m-%d')
        print(f"Humidity: {yearly_calculations['Max Humidity']}% on {date.strftime('%b')} {date.strftime('%d')}")

    def monthly_report(self, monthly_calculations):
        print(f"Highest Average: {int(monthly_calculations['Avg Max Temp'])}C")
        print(f"Lowest Average: {int(monthly_calculations['Avg Min Temp'])}C")
        print(f"Average Mean Humidity: {int(monthly_calculations['Avg Mean Humidity'])}%")

    def monthly_bar_chart(self, data):
        for reading in data:
            if reading['Max TemperatureC'] is not None and reading['Min TemperatureC'] is not None:
                date = (datetime.strptime(reading['PKT'], '%Y-%m-%d')
                        if 'PKT' in reading.keys() else datetime.strptime(reading['PKST'], '%Y-%m-%d'))

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

    def horizontal_barchart(self, data):
        for reading in data:
            if reading['Max TemperatureC'] is not None and reading['Min TemperatureC'] is not None:
                date = (datetime.strptime(reading['PKT'], '%Y-%m-%d') 
                        if 'PKT' in reading.keys() else datetime.strptime(reading['PKST'], '%Y-%m-%d'))
                print(
                    f"{date.strftime('%d')} "
                    f"{self.CBLUE}{reading['Min TemperatureC'] * '+'}{self.CEND}"
                    f"{self.CRED}{reading['Max TemperatureC'] * '+'}{self.CEND} "
                    f"{reading['Min TemperatureC']}C-{reading['Max TemperatureC']}C"
                    )
