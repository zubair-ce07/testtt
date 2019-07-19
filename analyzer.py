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

    def get_day_with_max_temperature_from_year(self, readings, year):
        """Returns WeatherReading object with the maximum temperature"""
        readings = self.__filter(readings, year)
        readings = [w for w in readings if w.max_temperature != None]
        day_with_max_temperature = max(readings, key=lambda w: w.min_temperature)
        return day_with_max_temperature

    def get_day_with_min_temperature_from_year(self, readings, year):
        """Returns WeatherReading object with the minimum temperature"""
        readings = self.__filter(readings, year)
        readings = [w for w in readings if w.min_temperature != None]
        day_with_min_temperature = min(readings, key=lambda w: w.min_temperature)
        return day_with_min_temperature

    def get_day_with_max_humidity_from_year(self, readings, year):
        """Returns WeatherReading object with the highest humidity"""
        readings = self.__filter(readings, year)
        readings = [w for w in readings if w.max_humidity != None]
        day_with_max_humidity = max(readings, key=lambda w: w.max_humidity)
        return day_with_max_humidity

    def get_avg_max_temperature_from_month(self, readings, year, month):
        """Returns average maximum temperature for a month"""
        readings = self.__filter(readings, year, month)
        readings = [w for w in readings if w.max_temperature != None]
        average_max_temperature = self.__average([w.max_temperature for w in readings])
        return average_max_temperature

    def get_avg_min_temperature_from_month(self, readings, year, month):
        """Returns average minimum temperature for a month"""
        readings = self.__filter(readings, year, month)
        readings = [w for w in readings if w.min_temperature != None]
        average_min_temperature = self.__average([w.min_temperature for w in readings])
        return average_min_temperature

    def get_avg_mean_humidity_from_month(self, readings, year, month):
        """Returns average mean humidity for a month"""
        readings = self.__filter(readings, year, month)
        readings = [w for w in readings if w.min_temperature != None]
        avg_mean_humidity = self.__average([w.mean_humidity for w in readings])
        return avg_mean_humidity

    def get_list_of_max_temperatures_from_month(self, readings, year, month):
        """Returns a list of maximum temperature in a month ordered by date"""
        readings = self.__filter(readings, year, month)
        readings = sorted(readings, key=lambda w: w.date.day)
        return [w.max_temperature for w in readings]

    def get_list_of_min_temperatures_from_month(self, readings, year, month):
        """Returns a list of minimum temperature in a month ordered by date"""
        readings = self.__filter(readings, year, month)
        readings = sorted(readings, key=lambda w: w.date.day)
        return [w.min_temperature for w in readings]
