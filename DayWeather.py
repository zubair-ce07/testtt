import calendar


class DayWeather(object):
    """ contains data for Min Temp Day Weather ."""
    def __init__(self):
        self.__max_temp = 0
        self.__avg_max_temp = 0
        self.__max_temp_date = ""
        self.__max_humidity = 0
        self.__avg_max_humidity = 0
        self.__max_humidity_date = ""
        self.__min_temp = 100
        self.__avg_min_temp = 0
        self.__min_temp_date = ""

    def set_max_temp(self, max_temp):
        self.__max_temp = max_temp

    def get_max_temp(self):
        return self.__max_temp

    def set_avg_max_temp(self, avg_max_temp):
        self.__avg_max_temp = avg_max_temp

    def get_avg_max_temp(self):
        return self.__avg_max_temp

    def set_max_temp_date(self, max_temp_date):
        self.__max_temp_date = max_temp_date

    def get_max_temp_date(self):
        return self.__max_temp_date

    def print_max_temp_data(self):
        max_temp_date = self.get_max_temp_date().split("-")
        print("Highest: " + str(self.get_max_temp()) +
              "C on " + calendar.month_name[int(max_temp_date[1])] +
              " " + str(max_temp_date[2]))

    def print_avg_max_temp(self):
        print ("Highest Average: " +
                str(self.get_avg_max_temp()) +
                "C")

    def set_max_humidity(self, max_humidity):
        self.__max_humidity = max_humidity

    def get_max_humidity(self):
        return self.__max_humidity

    def set_avg_max_humidity(self, avg_max_humidity):
        self.__avg_max_humidity = avg_max_humidity

    def get_avg_max_humidity(self):
        return self.__avg_max_humidity

    def set_max_humidity_date(self, max_humidity_date):
        self.__max_humidity_date = max_humidity_date

    def get_max_humidity_date(self):
        return self.__max_humidity_date

    def print_max_humid_data(self):
        max_humidity_date = self.__max_humidity_date.split("-")
        print("Humid: " + str(self.__max_humidity) +
              "% on " + calendar.month_name[int(max_humidity_date[1])] +
              " " + str(max_humidity_date[2]))

    def print_avg_max_humidity(self):
        print ("Average Humidity: " +
                str(self.get_avg_max_humidity()) +
                "%")

    def set_min_temp(self, min_temp):
        self.__min_temp = min_temp

    def get_min_temp(self):
        return self.__min_temp

    def set_avg_min_temp(self, avg_min_temp):
        self.__avg_min_temp = avg_min_temp

    def get_avg_min_temp(self):
        return self.__avg_min_temp

    def set_min_temp_date(self, min_temp_date):
        self.__min_temp_date = min_temp_date

    def get_min_temp_date(self):
        return self.__min_temp_date

    def print_min_temp_data(self):
        min_temp_date = self.get_min_temp_date().split("-")
        print("Highest: " + str(self.get_min_temp()) +
              "C on " + calendar.month_name[int(min_temp_date[1])] +
              " " + str(min_temp_date[2]))

    def print_avg_min_temp(self):
        print ("Lowest Average: " +
                str(self.get_avg_min_temp()) +
                "C")
