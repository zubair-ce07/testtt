import datetime


class WeatherData:
    """This is a data structure for holding all the weather data
    it contains data from all the files present in directory.
    """

    def __init__(self, date, h_temperature, l_temperature, m_temperature,
                 max_humidity, mean_humidity):
        self.__date = date
        self.__highest_temperature = h_temperature
        self.__lowest_temperature = l_temperature
        self.__mean_temperature = m_temperature
        self.__max_humidity = max_humidity
        self.__mean_humidity = mean_humidity

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = date

    @property
    def highest_temperature(self):
        return self.__highest_temperature

    @highest_temperature.setter
    def highest_temperature(self, h_temperature):
        self.__highest_temperature = h_temperature

    @property
    def lowest_temperature(self):
        return self.__lowest_temperature

    @lowest_temperature.setter
    def lowest_temperature(self, l_temperature):
        self.__lowest_temperature = l_temperature

    @property
    def max_humidity(self):
        return self.__max_humidity

    @max_humidity.setter
    def max_humidity(self, max_humidity):
        self.__max_humidity = max_humidity

    @property
    def min_humidity(self):
        return self.__mean_humidity

    @min_humidity.setter
    def min_humidity(self, mean_humidity):
        self.__mean_humidity = mean_humidity

    @property
    def mean_temperature(self):
        return self.__mean_temperature

    @mean_temperature.setter
    def mean_temperature(self, mean_temperature):
        self.__mean_temperature = mean_temperature