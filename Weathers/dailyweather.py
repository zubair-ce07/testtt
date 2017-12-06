class DailyWeather:

    def __init__(self):
        self.day = ''
        self.highest_temperature = 0
        self.mean_temperature = 0
        self.lowest_temperature = 0
        self.max_humidity = 1
        self.mean_humidity = 1
        self.min_humidity = 1

    def get_day(self):
        return self.day

    def get_highest_temperature(self):
        return self.highest_temperature

    def get_lowest_temperature(self):
        return self.lowest_temperature

    def get_max_humidity(self):
        return self.max_humidity

    def get_mean_humidity(self):
        return self.mean_humidity
