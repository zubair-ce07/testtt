
class WeatherInformation(object):
    def __init__(self, date='', max_temp='', low_temp='', max_humid='', mean_humid=''):
        self.date = date
        self.max_temp = max_temp
        self.low_temp = low_temp
        self.max_humid = max_humid
        self.mean_humid = mean_humid


class CalculationResults(object):
    def __init__(
            self, max_temp='', max_temp_day='', low_temp='',
            low_temp_day='',max_humid='',max_humid_day='',
            average_max_temp='', average_low_temp='',
            average_mean_humid='', date=''):
        self.max_temp = max_temp
        self.max_temp_day = max_temp_day
        self.low_temp = low_temp
        self.low_temp_day = low_temp_day
        self.max_humid = max_humid
        self.max_humid_day = max_humid_day
        self.average_max_temp = average_max_temp
        self.average_low_temp = average_low_temp
        self.average_mean_humid = average_mean_humid
        self.date = date
