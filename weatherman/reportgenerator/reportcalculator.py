from statistics import mean

from reportgenerator import HighLowResult, AvgTemperatureResult


class ReportCalculator:
    def high_low_temperature(self, weather_records):
        max_temp_record = max(weather_records, key=lambda r: r.max_temp)
        max_humidity_record = max(weather_records, key=lambda r: r.max_humidity)
        min_temp_record = min(weather_records, key=lambda r: r.min_temp)

        return HighLowResult(max_temp_record, max_humidity_record, min_temp_record)

    def avg_temperature(self, weather_records):
        avg_max_temp = int(mean([r.max_temp for r in weather_records if r.max_temp]))
        avg_min_temp = int(mean([r.min_temp for r in weather_records if r.min_temp]))
        avg_mean_humidity = int(mean([r.mean_humidity for r in weather_records if r.mean_humidity]))

        return AvgTemperatureResult(avg_max_temp, avg_mean_humidity, avg_min_temp)
