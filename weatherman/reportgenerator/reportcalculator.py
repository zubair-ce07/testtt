from statistics import mean

from reportgenerator import HighLowResult, AvgTemperatureResult


class ReportCalculator:
    def __init__(self, weather_records):
        self.weather_parser = weather_records

    def high_low_temperature(self, weather_records):
        max_temp_record = max(weather_records, key=lambda x: x.max_temp)
        max_humidity_record = max(weather_records, key=lambda x: x.max_humidity)
        min_temp_record = min(weather_records, key=lambda x: x.min_temp)

        return HighLowResult(max_temp_record, max_humidity_record, min_temp_record)

    def avg_temperature(self, weather_records):
        max_temps = [d.max_temp for d in weather_records if d.max_temp]
        min_temps = [d.min_temp for d in weather_records if d.min_temp]
        mean_humidities = [d.mean_humidity for d in weather_records if d.mean_humidity]

        avg_max_temp = int(mean(max_temps))
        avg_min_temp = int(mean(min_temps))
        avg_mean_humidity = int(mean(mean_humidities))

        return AvgTemperatureResult(avg_max_temp, avg_mean_humidity, avg_min_temp)
