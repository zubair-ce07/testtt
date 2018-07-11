from computer import Computer


class Reporter:
    def __init__(self, data):
        self.__data = data
        self.__computer = Computer()

    def report_e(self):
        result_e = self.__computer.result_e(self.__data.readings)
        print("Highest: {}C on {}".format(
            result_e[0].max_temperature,
            result_e[0].date.strftime("%B %d")))
        print("Lowest: {}C on {}".format(
            result_e[1].min_temperature,
            result_e[1].date.strftime("%B %d")))
        print("Humidity: {}% on {}".format(
            result_e[2].max_humidity,
            result_e[2].date.strftime("%B %d")))

    def report_a(self):
        result_a = self.__computer.result_a(self.__data.readings)
        print("Highest Average: {}C".format(result_a[0].mean_temperature))
        print("Lowest Average: {}C".format(result_a[1].mean_temperature))
        print("Average Mean Humidity: {}%".format(result_a[2].mean_humidity))

    def report_c(self):
        print(self.__data.month, self.__data.year)
        result_c = self.__computer.result_c(self.__data.readings)
        red = "\033[1;31m"
        blue = "\033[1;34m"
        normal = "\033[0;0m"
        for day in result_c:
            print("%02d" % day.date.day,
                  f"{blue}{'+' * day.min_temperature}{red}{'+' * day.max_temperature}",
                  f"{normal}{'%02dC - %02dC' % (day.min_temperature, day.max_temperature)}")
