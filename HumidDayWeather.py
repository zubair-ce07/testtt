import calendar


class HumidDayWeather:
    """ contains data for Humid Day Weather ."""
    def __init__(self):
        self.max_humidity = 0
        self.avg_max_humidity = 0
        self.max_humidity_date = ""

    def set_max_humidity(self, max_humidity):
        self.max_humidity = max_humidity

    def get_max_humidity(self):
        return self.max_humidity

    def set_avg_max_humidity(self, avg_max_humidity):
        self.avg_max_humidity = avg_max_humidity

    def get_avg_max_humidity(self):
        return self.avg_max_humidity

    def set_max_humidity_date(self, max_humidity_date):
        self.max_humidity_date = max_humidity_date

    def get_max_humidity_date(self):
        return self.max_humidity_date

    def print_max_humid_data(self):
        max_humidity_date = self.max_humidity_date.split("-")
        print("Humid: " + str(self.max_humidity) +
              "% on " + calendar.month_name[int(max_humidity_date[1])] +
              " " + str(max_humidity_date[2]))

    def print_avg_max_humidity(self):
        print ("Average Humidity: " +
                str(self.get_avg_max_humidity()) +
                "%")
