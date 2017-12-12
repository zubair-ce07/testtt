class Forecast:
    def __init__(self, date, maximum_temp, minimum_temp, maximum_humidity, average_humidity):
        self.tempetaure_date = date
        self.maximum_temperature = maximum_temp
        self.minimum_temperature = minimum_temp
        self.maximum_humidity = maximum_humidity
        self.average_humidity = average_humidity

    def tempetaure_date(self):
        return self.tempetaure_date

    def maximum_temperature(self):
        return self.maximum_temperature

    def minimum_temperature(self):
        return self.minimum_temperature

    def maximum_humidity(self):
        return self.maximum_humidity

    def average_humidity(self):
        return self.average_humidity