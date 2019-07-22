class WeatherAnalyzer():
    """Extracts aggregate information from WeatherReading objects"""

    def __filter(self, readings, year, month=None):
        """Filters readings based on the year and optionally on month"""
        if month == None:
            filtered = [w for w in readings if w["PKT"].year == year]
        else:
            filtered = [w for w in readings
                        if w["PKT"].year == year and w["PKT"].month == month]
        return filtered

    def __average(self, values):
        """Returns average of values in an array"""
        total = sum(values)
        count = len(values)
        try:
            return round(total/count)
        except ZeroDivisionError:
            return 0

    def get_maximum_temperature_day(self, readings, year):
        """Returns WeatherReading object with the maximum temperature"""
        readings = self.__filter(readings, year)
        readings = [w for w in readings if w["Max TemperatureC"] != None]
        day_with_max_temperature = max(readings, key=lambda w: w["Min TemperatureC"])
        return day_with_max_temperature

    def get_minimum_temperature_day(self, readings, year):
        """Returns WeatherReading object with the minimum temperature"""
        readings = self.__filter(readings, year)
        readings = [w for w in readings if w["Min TemperatureC"] != None]
        day_with_min_temperature = min(readings, key=lambda w: w["Min TemperatureC"])
        return day_with_min_temperature

    def get_most_humidity_day(self, readings, year):
        """Returns WeatherReading object with the highest humidity"""
        readings = self.__filter(readings, year)
        readings = [w for w in readings if w["Max Humidity"] != None]
        day_with_max_humidity = max(readings, key=lambda w: w["Max Humidity"])
        return day_with_max_humidity

    def get_avg_maximum_temperature(self, readings, year, month):
        """Returns average maximum temperature for a month"""
        readings = self.__filter(readings, year, month)
        readings = [w for w in readings if w["Max TemperatureC"] != None]
        average_max_temperature = self.__average([w["Max TemperatureC"] for w in readings])
        return average_max_temperature

    def get_avg_minimum_temperature(self, readings, year, month):
        """Returns average minimum temperature for a month"""
        readings = self.__filter(readings, year, month)
        readings = [w for w in readings if w["Min TemperatureC"] != None]
        average_min_temperature = self.__average([w["Min TemperatureC"] for w in readings])
        return average_min_temperature

    def get_avg_mean_humidity(self, readings, year, month):
        """Returns average mean humidity for a month"""
        readings = self.__filter(readings, year, month)
        readings = [w for w in readings if w["Min TemperatureC"] != None]
        avg_mean_humidity = self.__average([w[" Mean Humidity"] for w in readings])
        return avg_mean_humidity

    def get_maximum_temperatures(self, readings, year, month):
        """Returns a list of maximum temperature in a month ordered by date"""
        readings = self.__filter(readings, year, month)
        readings = sorted(readings, key=lambda w: w["PKT"].day)
        return [w["Max TemperatureC"] for w in readings]

    def get_minimum_temperatures(self, readings, year, month):
        """Returns a list of minimum temperature in a month ordered by date"""
        readings = self.__filter(readings, year, month)
        readings = sorted(readings, key=lambda w: w["PKT"].day)
        return [w["Min TemperatureC"] for w in readings]
