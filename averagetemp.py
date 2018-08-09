import constants


class AverageTemperatue:
    """ Class for storing Average Temperatures """
    def __init__(self, high=constants.ZERO,
                 low=constants.ZERO, hum=constants.ZERO):
        self.avg_high = high
        self.avg_low = low
        self.avg_humidity = hum


