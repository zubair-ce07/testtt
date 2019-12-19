from statistics import mean
from types import SimpleNamespace


class WeatherDataAnalyzer:
    def __init__(self, weather_records, date=None):
        self.__weather_records = weather_records
        self.__date = date

    def calculate_extremes(self):
        result = SimpleNamespace()

        year_records = self.fetch_records_of_year(self.__date)

        sorted_by_highest_temp = self.sort_by_property('max_temperature', year_records)
        sorted_by_lowest_temp = self.sort_by_property('min_temperature', year_records)
        sorted_by_highest_humid = self.sort_by_property('max_humidity', year_records)

        result.max_temperature_record = sorted_by_highest_temp[-1]
        result.min_temperature_record = sorted_by_lowest_temp[0]
        result.max_humidity_record = sorted_by_highest_humid[-1]

        return result

    def calculate_averages(self):
        result = SimpleNamespace()

        month_records = self.fetch_records_of_month(self.__date)

        result.average_max_temperature = self.get_average_of_field('max_temperature', month_records)
        result.average_min_temperature = self.get_average_of_field('min_temperature', month_records)
        result.average_mean_humidity = self.get_average_of_field('mean_humidity', month_records)

        return result

    def fetch_records_of_month(self, date_to_search):
        return [record for record in self.__weather_records if
                record.record_date.month == date_to_search.month and record.record_date.year == date_to_search.year]

    def fetch_records_of_year(self, date_to_search):
        return [record for record in self.__weather_records if record.record_date.year == date_to_search.year]

    def get_average_of_field(self, field, weather_records):
        return mean([getattr(item, field) for item in weather_records])

    def sort_by_property(self, field, weather_records):
        return sorted(weather_records, key=lambda k: getattr(k, field))
