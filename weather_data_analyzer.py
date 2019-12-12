from statistics import mean
from types import SimpleNamespace


class WeatherDataAnalyzer:
    def __init__(self, weather_readings):
        self.__weather_readings = weather_readings

    def calculate_extremes(self):
        result = SimpleNamespace()

        if len(self.__weather_readings) == 0:
            print('No data found for calculating extremes')
            return False

        sorted_by_highest_temp = self.sort_by_property('max_temperature')
        sorted_by_lowest_temp = self.sort_by_property('min_temperature')
        sorted_by_highest_humid = self.sort_by_property('max_humidity')

        result.max_temperature_reading = sorted_by_highest_temp[-1]
        result.min_temperature_reading = sorted_by_lowest_temp[0]
        result.max_humidity_reading = sorted_by_highest_humid[-1]

        return result

    def calculate_averages(self):
        result = SimpleNamespace()

        if len(self.__weather_readings) == 0:
            print('No data found for calculating averages')
            return False

        result.average_max_temperature = self.get_average_of_field('max_temperature')
        result.average_min_temperature = self.get_average_of_field('min_temperature')
        result.average_mean_humidity = self.get_average_of_field('mean_humidity')

        return result

    def get_average_of_field(self, field):
        return mean([getattr(item, field) for item in self.__weather_readings])

    def sort_by_property(self, field):
        return sorted(self.__weather_readings, key=lambda k: getattr(k, field))
