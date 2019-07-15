from datetime import datetime


class Reporter:

    CRED = '\033[91m'
    CEND = '\033[0m'
    CBLUE = '\33[34m'

    def yearly_report(self, yearly_calculations):
        """This function will print max temperature, max humidity
        and minimum temperature in
        in the year details.
        """

        try:
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
        except KeyError:
            print("Invalid Input....")
        return

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

        return

    def monthly_bar_chart(self, data):
        """This will print the bar chart."""

        for i in range(len(data[1])):
            if data[1][i] is not None and data[2][i] is not None:
                high = data[1][i] * '+'
                low = data[2][i] * '+'
                print(f'{i} {self.CRED}{high}{self.CEND} {data[1][i]}C')
                print(f'{i} {self.CBLUE}{low}{self.CEND} {data[2][i]}C')
        return

    def horizontal_barchart(self, data):
        """This will print horizontal bar chart."""

        for i in range(len(data[1])):
            if data[1][i] is not None and data[2][i] is not None:
                high = data[1][i] * '+'
                low = data[2][i] * '+'
                print(f'{i} {self.CRED}{high}{self.CEND}{self.CBLUE}{low}{self.CEND} {data[1][i]}C-{data[2][i]}C')
        return
