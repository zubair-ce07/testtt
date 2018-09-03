class WeatherData:

    def __init__(self, date, max_temperature, min_temperature, humidity):
        self.__date = date
        self.__max_temperature = max_temperature
        self.__min_temperature = min_temperature
        self.__humidity = humidity

    def get_date(self):
        return self.__date

    def get_max_temperature(self):
        return self.__max_temperature

    def get_min_temperature(self):
        return self.__min_temperature

    def get_humidity(self):
        return self.__humidity
