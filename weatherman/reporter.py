from datetime import datetime
import math


class Reporter:

    CRED = '\033[91m'
    CEND = '\033[0m'
    CBLUE = '\33[34m'

    def yearly_report(self, yearly_calculations):
        """This function will print max temperature, max humidity
        and minimum temperature in
        in the year details.
        """
        date = yearly_calculations['Max Temp Day']
        date = datetime.strptime(date, '%Y-%m-%d')
        month = date.strftime("%b")
        day = date.strftime("%d")
        max_temp = yearly_calculations['Max Temperature']

        print(f'Highest: {max_temp}C on {month} {day}')

        date = yearly_calculations['Min Temp Day']
        date = datetime.strptime(date, '%Y-%m-%d')
        month = date.strftime("%b")
        day = date.strftime("%d")
        min_temp = yearly_calculations['Min Temperature']

        print(f'Lowest: {min_temp}C on {month} {day}')

        date = yearly_calculations['Max Humidity Day']
        date = datetime.strptime(date, '%Y-%m-%d')
        month = date.strftime("%b")
        day = date.strftime("%d")
        max_humid = yearly_calculations['Max Humidity']

        print(f'Humidity: {max_humid}% on {month} {day}')

    def monthly_report(self, monthly_calculations):
        """This will report highest average temperature, lowest average
        temperature and average mean humidity.
        """

        avg_max_temp = monthly_calculations['Avg Max Temp']
        print(f'Highest Average: {int(avg_max_temp)}C')

        avg_min_temp = monthly_calculations['Avg Min Temp']
        print(f'Lowest Average: {int(avg_min_temp)}C')

        avg_mean_humid = monthly_calculations['Avg Mean Humidity']
        print(f'Average Mean Humidity: {int(avg_mean_humid)}%')

    def monthly_bar_chart(self, data):
        """This will print the bar chart."""

        for reading in data:
            if reading['Max TemperatureC'] != -math.inf and reading['Min TemperatureC'] != math.inf:
                high_str = reading['Max TemperatureC'] * '+'
                low_str = reading['Min TemperatureC'] * '+'
                high_temp = reading['Max TemperatureC']
                low_temp = reading['Min TemperatureC']
                day = reading['PKT'].split('-')[2] if 'PKT' in reading.keys() else reading['PKST'].split('-')[2]

                print(f'{day} {self.CRED}{high_str}{self.CEND} {high_temp}C')
                print(f'{day} {self.CBLUE}{low_str}{self.CEND} {low_temp}C')

    def horizontal_barchart(self, data):
        """This will print horizontal bar chart."""
        for reading in data:
            if reading['Max TemperatureC'] != -math.inf and reading['Min TemperatureC'] != math.inf:
                high_str = reading['Max TemperatureC'] * '+'
                low_str = reading['Min TemperatureC'] * '+'
                high_temp = reading['Max TemperatureC']
                low_temp = reading['Min TemperatureC']
                day = reading['PKT'].split('-')[2] if 'PKT' in reading.keys() else reading['PKST'].split('-')[2]

                print(
                    f'{day} {self.CBLUE}{low_str}{self.CEND}{self.CRED}{high_str}{self.CEND} {low_temp}C-{high_temp}C'
                    )
