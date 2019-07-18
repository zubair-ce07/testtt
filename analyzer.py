class WeatherAnalyzer():
    """Extracts aggregate information from WeatherReading objects"""

    def __filter(self, readings, year, month=None):
        """Filters readings based on the year and optionally on month"""
        if month == None:
            filtered = [w for w in readings if w.date.year == year]
        else:
            filtered = [w for w in readings
                        if w.date.year == year and w.date.month == month]
        return filtered

    def __average(self, values):
        """Returns average of values in an array"""
        total = sum(values)
        count = len(values)
        try:
            return round(total/count)
        except ZeroDivisionError:
            return 0

    def get_max_temperature_year(self, readings, year):
        """Returns WeatherReading object with the maximum temperature"""
        readings = self.__filter(readings, year)
        readings = [w for w in readings if w.max_temperature != None]
        max_temperature = max(readings, key=lambda w: w.min_temperature)
        return max_temperature

    def get_min_temperature_year(self, readings, year):
        """Returns WeatherReading object with the minimum temperature"""
        readings = self.__filter(readings, year)
        readings = [w for w in readings if w.min_temperature != None]
        min_temperature = min(readings, key=lambda w: w.min_temperature)
        return min_temperature

    def get_max_humidity_year(self, readings, year):
        """Returns WeatherReading object with the highest humidity"""
        readings = self.__filter(readings, year)
        readings = [w for w in readings if w.max_humidity != None]
        max_humidity = max(readings, key=lambda w: w.max_humidity)
        return max_humidity

    def get_avg_max_temperature_month(self, readings, year, month):
        """Returns average maximum temperature for a month"""
        readings = self.__filter(readings, year, month)
        readings = [w for w in readings if w.max_temperature != None]
        average_max = self.__average([w.max_temperature for w in readings])
        return average_max

    def get_avg_min_temperature_month(self, readings, year, month):
        """Returns average minimum temperature for a month"""
        readings = self.__filter(readings, year, month)
        readings = [w for w in readings if w.min_temperature != None]
        average_min = self.__average([w.min_temperature for w in readings])
        return average_min

    def get_avg_mean_humidity_month(self, readings, year, month):
        """Returns average mean humidity for a month"""
        readings = self.__filter(readings, year, month)
        readings = [w for w in readings if w.min_temperature != None]
        avg_mean_humidity = self.__average([w.mean_humidity for w in readings])
        return avg_mean_humidity

    def get_max_temperatures_month(self, readings, year, month):
        """Returns a list of maximum temperature in a month ordered by date"""
        readings = self.__filter(readings, year, month)
        readings = sorted(readings, key=lambda w: w.date.day)
        return [w.max_temperature for w in readings]

    def get_min_temperatures_month(self, readings, year, month):
        """Returns a list of minimum temperature in a month ordered by date"""
        readings = self.__filter(readings, year, month)
        readings = sorted(readings, key=lambda w: w.date.day)
        return [w.min_temperature for w in readings]
