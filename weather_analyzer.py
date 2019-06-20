from weather_results import WeatherResult
from weather_record_parser import WeatherDataParser


class WeatherAnalyzer:
    def __init__(self):
        self.weather_records = []

    def collect_weather_data_set(self, files_path):
        weather_data_parser = WeatherDataParser()
        self.weather_records = weather_data_parser.parse(files_path)

    def get_filtered_records(self, year, month):
        return [day_weather_record for day_weather_record in self.weather_records
                if (day_weather_record.pkt.month == month if month else True)
                and day_weather_record.pkt.year == year]

    def get_weather_results(self, dir_path, year, month=None):
        weather_results = WeatherResult()
        self.collect_weather_data_set(dir_path)
        filtered_records = self.get_filtered_records(year, month)
        weather_results.max_temp_record = WeatherAnalyzer.get_max_temperature(filtered_records)
        weather_results.min_temp_record = WeatherAnalyzer.get_min_temperature(filtered_records)
        weather_results.max_humidity_record = WeatherAnalyzer.get_max_humidity(filtered_records)
        weather_results.mean_humidity_avg = WeatherAnalyzer.get_mean_humidity(filtered_records)
        weather_results.avg_min_temp = WeatherAnalyzer.get_avg_min_temp(filtered_records)
        weather_results.avg_max_temp = WeatherAnalyzer.get_avg_max_temp(filtered_records)
        weather_results.daily_reading = filtered_records
        return weather_results

    @staticmethod
    def get_max_temperature(weather_records):
        return max(weather_records, key=lambda daily_reading: daily_reading.max_temperature)

    @staticmethod
    def get_min_temperature(weather_records):
        return min(weather_records, key=lambda daily_reading: daily_reading.min_temperature)

    @staticmethod
    def get_max_humidity(weather_records):
        return max(weather_records, key=lambda daily_reading: daily_reading.max_humidity)

    @staticmethod
    def get_mean_humidity(weather_records):
        mean_humidity_sum = sum(daily_reading.mean_humidity for daily_reading in weather_records)
        return mean_humidity_sum/ len(weather_records)

    @staticmethod
    def get_avg_min_temp(weather_records):
        min_temp_sum = sum(daily_reading.min_temperature for daily_reading in weather_records)
        return min_temp_sum / len(weather_records)

    @staticmethod
    def get_avg_max_temp(weather_records):
        max_temp_sum = sum(daily_reading.max_temperature for daily_reading in weather_records)
        return max_temp_sum / len(weather_records)
