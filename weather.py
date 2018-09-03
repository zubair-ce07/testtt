"""
this class contains all weather attributes
"""
import constants


class Weather:
    """
    this class is the definition of weather class
    """
    def __init__(self, max_temp=constants.EMPTY_STRING, min_temp=constants.EMPTY_STRING,
                 max_humid=constants.EMPTY_STRING, mean_humid=constants.EMPTY_STRING,
                 date=constants.EMPTY_STRING):
        self.max_temperature = max_temp
        self.min_temperature = min_temp
        self.max_humidity = max_humid
        self.mean_humidity = mean_humid
        self.date = date
