import constants


class TemperatureOfYear:
    """ This is a class for storing Yearly Temperature """
    def __init__(self, high=constants.MIN_VALUE,
                 low=constants.MAX_VALUE, hum=constants.ZERO):
        self.highest = high
        self.highest_temp_day = ""
        self.lowest = low
        self.lowest_temp_day = ""
        self.humidity = hum
        self.humid_day = ""


