from computer import *


class Reporter:
    def __init__(self, data):
        self.__data = data

    def report_for_e(self):
        max_temperature = max_value(self.__data.readings, lambda wr: wr.max_temperature)
        min_temperature = min_value(self.__data.readings, lambda wr: wr.min_temperature)
        max_humidity = max_value(self.__data.readings, lambda wr: wr.max_humidity)
        print("Highest: {}C on {}".format(
            max_temperature.max_temperature,
            max_temperature.date.strftime("%B %d")))
        print("Lowest: {}C on {}".format(
            min_temperature.min_temperature,
            min_temperature.date.strftime("%B %d")))
        print("Humidity: {}% on {}".format(
            max_humidity.max_humidity,
            max_humidity.date.strftime("%B %d")))

    def report_for_a(self):
        max_mean_temperature = max_value(self.__data.readings, lambda wr: wr.mean_temperature)
        min_mean_temperature = min_value(self.__data.readings, lambda wr: wr.mean_temperature)
        avg_mean_humidity = mean_value(self.__data.readings, lambda wr: wr.mean_humidity)
        print("Highest Average: {}C".format(max_mean_temperature.mean_temperature))
        print("Lowest Average: {}C".format(min_mean_temperature.mean_temperature))
        print("Average Mean Humidity: {}%".format(avg_mean_humidity.mean_humidity))

    def report_for_c(self):
        print(self.__data.month, self.__data.year)
        red = "\033[1;31m"
        blue = "\033[1;34m"
        normal = "\033[0;0m"
        for day in self.__data.readings:
            print("%02d" % day.date.day,
                  f"{blue}{'+' * day.min_temperature}{red}{'+' * day.max_temperature}",
                  f"{normal}{'%02dC - %02dC' % (day.min_temperature, day.max_temperature)}")
