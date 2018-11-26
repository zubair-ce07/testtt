from datetime import datetime
from termcolor import colored, cprint


class Reports:
    """Class for generating reports and printing on to the console"""

    def yearly_weather(self, result):

            """reads the temperature results for the year and displays on the console"""

            print("Highest {0}C on {1} {2}" .format(result[0].max_temperature, \
                    result[0].date.strftime('%B'), result[0].date.day))
            print("Lowest: {0}C on {1} {2}" .format(result[1].min_temperature, \
                    result[1].date.strftime('%B'), result[1].date.day ))
            print("Humidity: {0}% on {1} {2} ".format(result[2].max_humidity, \
                    result[2].date.strftime('%B'), result[2].date.day))

    def monthly_weather(self, result):

            """reads temperature results for month and displays output on the console"""

            print("Highest Average: {0}C ".format(result[0]))
            print("Lowest Average: {0}C ".format(result[1]))
            print("Average Mean Humidity: {0}% ".format(result[2]))

    def max_min_bar(self, month, year, result):

        """reads the result and displays graphs """

        s = datetime.strptime(month, '%b')
        m = s.strftime('%B')
        print("{0} {1}".format(m, year))
        highest_temp = result[0].max_temperature
        lowest_temp = result[0].min_temperature

        for i in range(int(highest_temp)):
            cprint('+', 'red', end=' ')
        print('{0}C'.format(str(highest_temp)))

        for j in range(int(lowest_temp)):
            cprint('+', 'blue', end=' ')
        print('{0}C'.format(str(lowest_temp)))

        # print one bar graph
        for i in range(int(highest_temp)):
            cprint('+', 'red', end=' ')
        for j in range(int(lowest_temp)):
            cprint('+', 'blue', end=' ')
        print('{0}C-{1}C'.format(str(highest_temp), str(lowest_temp)))
