from weather_result import WeatherResult


class WeatherResultCalculator:
    @staticmethod
    def get_result(weather_records):
        weather_result = WeatherResult()

        weather_result.max_temperature_record = max(weather_records, key=lambda p: p.highest_temperature)
        weather_result.min_temperature_record = min(weather_records, key=lambda p: p.lowest_temperature)
        weather_result.max_humidity_record = max(weather_records, key=lambda p: p.max_humidity)
        weather_result.max_avg_temperature_record = max(weather_records, key=lambda p: p.mean_temperature)
        weather_result.min_avg_temperature_record = min(weather_records, key=lambda p: p.mean_temperature)

        total_humidity = sum(weather_record.mean_humidity for weather_record in weather_records)
        weather_result.mean_humidity = total_humidity/len(weather_records)

        for daily_data in weather_records:
            weather_result.daily_temperatures.append(daily_data)

        return weather_result
