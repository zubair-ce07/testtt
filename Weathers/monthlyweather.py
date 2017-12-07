def mean(_list):
    return sum(_list) / len(_list)


class MonthlyWeather(object):

    def __init__(self, date):
        self._date = date
        self.daily_weathers = list()
        self._hottest_day = None
        self._coolest_day = None
        self._humid_day = None

    def add_daily_weather(self, weather):
        self.daily_weathers.append(weather)

    def month(self):
        return self._date.month

    def month_name(self):
            return self._date.strftime('%B')

    def highest_average_temperature(self):

        return mean([weather.highest_temperature()
                     for weather in self.daily_weathers
                     if weather.highest_temperature() is not None])

    def lowest_average_temperature(self):

        return mean([weather.lowest_temperature()
                     for weather in self.daily_weathers
                     if weather.lowest_temperature() is not None])

    def average_mean_humidity(self):

        return mean([weather.get_mean_humidity()
                     for weather in self.daily_weathers
                     if weather.get_mean_humidity() is not None])

    def highest_temperature(self):

        if self._hottest_day is None:
            self._hottest_day=self._find_hottest();

        return self._hottest_day.highest_temperature()

    def hottest_day(self):
        if self._hottest_day is None:
            self._hottest_day=self._find_hottest();

        return self._hottest_day.day()

    def lowest_temperature(self):
        if self._coolest_day is None:
            self._coolest_day=self._find_coolest();

        return self._coolest_day.lowest_temperature()

    def coolest_day(self):
        if self._coolest_day is None:
            self._coolest_day=self._find_coolest();

        return self._coolest_day.day()

    def most_humid_day(self):
        if self._humid_day is None:
            self._humid_day=self._find_humid();

        return self._humid_day.day()

    def max_humidity(self):
        if self._humid_day is None:
            self._humid_day=self._find_humid();

        return self._humid_day.max_humidity()

    def _find_hottest(self):
        hottest_day=None
        for weather in self.daily_weathers:
                if hottest_day is None:
                    hottest_day = weather
                else:
                    highest_temperature = hottest_day.highest_temperature()
                    new_temperature = weather.highest_temperature()

                    if new_temperature is not None and highest_temperature < new_temperature:
                        hottest_day = weather
        return hottest_day

    def _find_coolest(self):
        coolest_day=None
        for weather in self.daily_weathers:
                if coolest_day is None:
                    coolest_day = weather
                else:
                    lowest_temperature = coolest_day.lowest_temperature()
                    new_temperature = weather.lowest_temperature()

                    if new_temperature is not None and lowest_temperature > new_temperature:
                        coolest_day = weather
        return coolest_day

    def _find_humid(self):
        humid_day=None
        for weather in self.daily_weathers:
                if humid_day is None:
                    humid_day = weather
                else:
                    highest_humidity = humid_day.max_humidity()
                    new_humidity = weather.max_humidity()

                    if new_humidity is not None and highest_humidity < new_humidity:
                        humid_day = weather
        return humid_day
