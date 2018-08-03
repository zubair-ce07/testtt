import calendar


class MinTempDayWeather:
    """ contains data for Max Temp Day Weather ."""
    def __init__(self):
        self.min_temp = 100
        self.avg_min_temp = 0
        self.min_temp_date = ""

    def set_min_temp(self, min_temp):
        self.min_temp = min_temp

    def get_min_temp(self):
        return self.min_temp

    def set_avg_min_temp(self, avg_min_temp):
        self.avg_min_temp = avg_min_temp

    def get_avg_min_temp(self):
        return self.avg_min_temp

    def set_min_temp_date(self, min_temp_date):
        self.min_temp_date = min_temp_date

    def get_min_temp_date(self):
        return self.min_temp_date

    def print_min_temp_data(self):
        min_temp_date = self.get_min_temp_date().split("-")
        print("Highest: " + str(self.get_min_temp()) +
              "C on " + calendar.month_name[int(min_temp_date[1])] +
              " " + str(min_temp_date[2]))

    def print_avg_min_temp(self):
        print ("Lowest Average: " +
                str(self.get_avg_min_temp()) +
                "C")
