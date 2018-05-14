import operator


class WeatherAnalyzer:

    def __init__(self, weather_record):
        self.weather_records = weather_record

    def calculate_weather_extremes(self):
        self.max_weather = max(self.weather_records, key=lambda index: index.max_temp)
        self.min_weather = min(self.weather_records, key=lambda index: index.min_temp)
        self.max_humidity = max(self.weather_records, key=lambda index: index.max_humidity)

    def calculate_weather_averages(self):
        self.max_temp_avrg = int(sum(temperature.max_temp for temperature in self.weather_records) \
                             / len(self.weather_records))
        self.min_temp_avrg = int(sum(temperature.min_temp for temperature in self.weather_records) \
                             / len(self.weather_records))
        self.max_humidity_avrg = int(sum(temperature.mean_humidity for temperature in self.weather_records) \
                                 / len(self.weather_records))
