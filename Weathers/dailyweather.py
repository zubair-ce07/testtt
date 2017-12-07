class DailyWeather:

    def __init__(self, date, max_temp, mean_temp, min_temp, max_humidity, mean_humidity, min_humidity):
        self._date = date
        self._highest_temperature = max_temp
        self._mean_temperature = mean_temp
        self._lowest_temperature = min_temp
        self._max_humidity = max_humidity
        self._mean_humidity = mean_humidity
        self._min_humidity = min_humidity

    def day(self):
        return self._date.day

    def month_name(self):
        return self._date.strftime('%B')

    def highest_temperature(self):
        return self._highest_temperature

    def lowest_temperature(self):
        return self._lowest_temperature

    def max_humidity(self):
        return self._max_humidity

    def mean_humidity(self):
        return self._mean_humidity
