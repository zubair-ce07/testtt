from statistics import mean

from result_set import ResultSet


class WeatherDataAnalyzer:
    def __init__(self, data):
        self.__data = data

    def calculate_extremes(self):
        result = ResultSet()

        if len(self.__data) == 0:
            print("No data found for calculating extremes")
            return False

        sorted_by_highest_temp = self.sort_by_property('max_temperature')
        sorted_by_lowest_temp = self.sort_by_property('min_temperature')
        sorted_by_highest_humid = self.sort_by_property('max_humidity')

        result.max_temperature_reading = sorted_by_highest_temp[-1]
        result.min_temperature_reading = sorted_by_lowest_temp[0]
        result.max_humidity_reading = sorted_by_highest_humid[-1]

        return result

    def find_date_with_max_field_value(self, field):
        result = ResultSet()

        setattr(result, field, getattr(self.sort_by_property(field)[-1], field))

        return result

    def find_date_with_min_field_value(self, field):
        result = ResultSet()

        setattr(result, field, getattr(self.sort_by_property(field)[0], field))

        return result

    def calculate_averages(self):
        result = ResultSet()

        if len(self.__data) == 0:
            print("No data found for calculating averages")
            return False

        result.average_max_temperature = self.get_average_of_field('max_temperature')
        result.average_min_temperature = self.get_average_of_field('min_temperature')
        result.average_mean_humidity = self.get_average_of_field('mean_humidity')

        return result

    def get_average_of_field(self, field):
        return mean([getattr(item, field) for item in self.__data])

    def sort_by_property(self, field):
        return sorted(self.__data, key=lambda k: getattr(k, field))
