from weather_results import WeatherResult
from weather_record_parser import WeatherDataParser


class WeatherAnalyzer:
    def __init__(self):
        self.weather_records = []

    def collect_weather_data_set(self, files_path):
        weather_data_parser = WeatherDataParser()
        self.weather_records = weather_data_parser.parse(files_path)

    def get_filtered_records(self, year, month=None):
        return [day_weather_record for day_weather_record in
                self.weather_records if (day_weather_record.pkt.month == month if month else
                                         True) and day_weather_record.pkt.year == year]

    def get_weather_results(self, weather_records):
        computed_weather_results = WeatherResult()
        computed_weather_results.max_temperature_record = max(weather_records,
                                                              key=lambda day_data: int(
                                                                  day_data.max_temperature))
        computed_weather_results.min_temperature_record = min(weather_records,
                                                              key=lambda day_data: int(
                                                                  day_data.min_temperature))
        computed_weather_results.max_humidity_record = max(weather_records,
                                                           key=lambda day_data: int(
                                                               day_data.max_humidity))
        computed_weather_results.mean_humidity_avg = sum(
            int(day_record.mean_humidity) for day_record in weather_records) / len(weather_records)
        computed_weather_results.avg_min_temperature = sum(
            int(day_record.min_temperature) for day_record in weather_records) / len(
            weather_records)
        computed_weather_results.avg_max_temperature = sum(
            int(day_record.max_temperature) for day_record in weather_records) / len(
            weather_records)
        return computed_weather_results
