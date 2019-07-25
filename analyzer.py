class WeatherAnalyzer():
    """Extracts aggregate information from WeatherReading objects"""

    def __average(self, values):
        """Returns average of values in an array"""
        total = sum(values)
        count = len(values)
        if count == 0:
            return 0
        else:
            return round(total/count)

    def get_maximum_temperature_day(self, readings):
        """Returns WeatherReading object with the maximum temperature"""
        readings = [w for w in readings if w.max_temperature != None]
        day_with_max_temperature = max(readings, key=lambda w: w.min_temperature)
        return day_with_max_temperature

    def get_minimum_temperature_day(self, readings):
        """Returns WeatherReading object with the minimum temperature"""
        readings = [w for w in readings if w.min_temperature != None]
        day_with_min_temperature = min(readings, key=lambda w: w.min_temperature)
        return day_with_min_temperature

    def get_most_humidity_day(self, readings):
        """Returns WeatherReading object with the highest humidity"""
        readings = [w for w in readings if w.max_humidity != None]
        day_with_max_humidity = max(readings, key=lambda w: w.max_humidity)
        return day_with_max_humidity

    def get_avg_maximum_temperature(self, readings):
        """Returns average maximum temperature for a month"""
        readings = [w for w in readings if w.max_temperature != None]
        average_max_temperature = self.__average([w.max_temperature for w in readings])
        return average_max_temperature

    def get_avg_minimum_temperature(self, readings):
        """Returns average minimum temperature for a month"""
        readings = [w for w in readings if w.min_temperature != None]
        average_min_temperature = self.__average([w.min_temperature for w in readings])
        return average_min_temperature

    def get_avg_mean_humidity(self, readings):
        """Returns average mean humidity for a month"""
        readings = [w for w in readings if w.min_temperature != None]
        avg_mean_humidity = self.__average([w.mean_humidity for w in readings])
        return avg_mean_humidity

    def get_maximum_temperatures(self, readings):
        """Returns a list of maximum temperature in a month ordered by date"""
        readings = sorted(readings, key=lambda w: w.date.day)
        return [w.max_temperature for w in readings]

    def get_minimum_temperatures(self, readings):
        """Returns a list of minimum temperature in a month ordered by date"""
        readings = sorted(readings, key=lambda w: w.date.day)
        return [w.min_temperature for w in readings]
