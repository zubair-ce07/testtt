from statistics import mean
from types import SimpleNamespace


class WeatherDataAnalyzer:
    def __init__(self, weather_readings, year=None, month=None):
        self.__weather_readings = weather_readings
        self.__year = year
        self.__month = month

    def calculate_extremes(self):
        result = SimpleNamespace()

        year_readings = self.fetch_records_of_year(self.__year)

        sorted_by_highest_temp = self.sort_by_property('max_temperature', year_readings)
        sorted_by_lowest_temp = self.sort_by_property('min_temperature', year_readings)
        sorted_by_highest_humid = self.sort_by_property('max_humidity', year_readings)

        result.max_temperature_reading = sorted_by_highest_temp[-1]
        result.min_temperature_reading = sorted_by_lowest_temp[0]
        result.max_humidity_reading = sorted_by_highest_humid[-1]

        return result

    def calculate_averages(self):
        result = SimpleNamespace()

        month_readings = self.fetch_records_of_month(self.__month, self.__year)

        result.average_max_temperature = self.get_average_of_field('max_temperature', month_readings)
        result.average_min_temperature = self.get_average_of_field('min_temperature', month_readings)
        result.average_mean_humidity = self.get_average_of_field('mean_humidity', month_readings)

        return result

    def fetch_records_of_month(self, month, year):
        records = []

        for record in self.__weather_readings:
            if record.reading_date.month == month and record.reading_date.year == year:
                records.append(record)

        return records

    def fetch_records_of_year(self, year):
        records = []

        for record in self.__weather_readings:
            if record.reading_date.year == year:
                records.append(record)

        return records

    def get_average_of_field(self, field, readings_data):
        return mean([getattr(item, field) for item in readings_data])

    def sort_by_property(self, field, readings_data):
        return sorted(readings_data, key=lambda k: getattr(k, field))
