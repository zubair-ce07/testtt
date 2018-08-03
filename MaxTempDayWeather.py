import calendar


class MaxTempDayWeather:
    """ contains data for Min Temp Day Weather ."""
    def __init__(self):
        self.max_temp = 0
        self.avg_max_temp = 0
        self.max_temp_date = ""

    def set_max_temp(self, max_temp):
        self.max_temp = max_temp

    def get_max_temp(self):
        return self.max_temp

    def set_avg_max_temp(self, avg_max_temp):
        self.avg_max_temp = avg_max_temp

    def get_avg_max_temp(self):
        return self.avg_max_temp

    def set_max_temp_date(self, max_temp_date):
        self.max_temp_date = max_temp_date

    def get_max_temp_date(self):
        return self.max_temp_date

    def print_max_temp_data(self):
        max_temp_date = self.get_max_temp_date().split("-")
        print("Highest: " + str(self.get_max_temp()) +
              "C on " + calendar.month_name[int(max_temp_date[1])] +
              " " + str(max_temp_date[2]))

    def print_avg_max_temp(self):
        print ("Highest Average: " +
                str(self.get_avg_max_temp()) +
                "C")
