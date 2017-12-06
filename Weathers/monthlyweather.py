def mean(_list):
    return sum(_list) / len(_list)


class MonthlyWeather(object):

    def __init__(self, month):
        self.month = month
        self.daily_weathers = list()
        self.hottest_day = None
        self.coolest_day = None
        self.most_humid_day = None

    def add_daily_weather(self, weather):

        if self.hottest_day is None:
            self.hottest_day = weather
        else:
            highest_temperature = self.hottest_day.get_highest_temperature()
            new_temperature = weather.get_highest_temperature()

            if highest_temperature < new_temperature:
                self.hottest_day = weather

        if self.coolest_day is None:
            self.coolest_day = weather
        else:
            lowest_temperature = self.coolest_day.get_lowest_temperature()
            new_temperature = weather.get_lowest_temperature()

            if lowest_temperature > new_temperature:
                self.coolest_day = weather

        if self.most_humid_day is None:
            self.most_humid_day = weather
        else:
            highest_humidity = self.most_humid_day.get_max_humidity()
            new_humidity = weather.get_max_humidity()

            if highest_humidity < new_humidity:
                self.most_humid_day = weather

        self.daily_weathers.append(weather)

    def get_month_name(self):
        month_names = ["January", "February", "March", "April",
                       "May", "June", "July",
                       "August", "September", "October",
                       "November", "December"]
        return month_names[self.month]

    def get_highest_average_temperature(self):

        return mean([weather.get_highest_temperature()
                     for weather in self.daily_weathers])

    def get_lowest_average_temperature(self):

        return mean([weather.get_lowest_temperature()
                     for weather in self.daily_weathers])

    def get_average_mean_humidity(self):

        return mean([weather.get_mean_humidity()
                     for weather in self.daily_weathers])

    def get_highest_temperature(self):
        return self.hottest_day.get_highest_temperature()

    def get_hottest_day(self):
        return self.hottest_day.get_day()

    def get_lowest_temperature(self):
        return self.coolest_day.get_lowest_temperature()

    def get_coolest_day(self):
        return self.coolest_day.get_day()

    def get_most_humid_day(self):
        return self.most_humid_day.get_day()

    def get_max_humidity(self):
        return self.most_humid_day.get_max_humidity()
