from datetime import date
import operator
from utilities import value_exists


class WeatherReading:

    def __init__(self, reading_date: date, max_temperature, mean_temperature, min_temperature, max_humidity, mean_humidity, min_humidity):
        self.reading_date = reading_date
        self.max_temperature = max_temperature
        self.mean_temperature = mean_temperature
        self.min_temperature = min_temperature
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.min_humidity = min_humidity

    reading_date = property(operator.attrgetter('_reading_date'))

    @reading_date.setter
    def reading_date(self, value):
        if value_exists(value):
            self._reading_date = value
        else:
            raise Exception('Date is required')

    max_temperature = property(operator.attrgetter('_max_temperature'))

    @max_temperature.setter
    def max_temperature(self, value):
        if value_exists(value):
            self._max_temperature = int(value)
        else:
            self._max_temperature = 0

    min_temperature = property(operator.attrgetter('_min_temperature'))

    @min_temperature.setter
    def min_temperature(self, value):
        if value_exists(value):
            self._min_temperature = int(value)
        else:
            self._min_temperature = 0

    mean_temperature = property(operator.attrgetter('_mean_temperature'))

    @mean_temperature.setter
    def mean_temperature(self, value):
        if value_exists(value):
            self._mean_temperature = float(value)
        else:
            self._mean_temperature = 0

    max_humidity = property(operator.attrgetter('_max_humidity'))

    @max_humidity.setter
    def max_humidity(self, value):
        if value_exists(value):
            self._max_humidity = int(value)
        else:
            self._max_humidity = 0

    mean_humidity = property(operator.attrgetter('_mean_humidity'))

    @mean_humidity.setter
    def mean_humidity(self, value):
        if value_exists(value):
            self._mean_humidity = float(value)
        else:
            self._mean_humidity = 0

    min_humidity = property(operator.attrgetter('_min_humidity'))

    @min_humidity.setter
    def min_humidity(self, value):
        if value_exists(value):
            self._min_humidity = int(value)
        else:
            self._min_humidity = 0

        


