from weather_result import WeatherResult


class WeatherAnalyzer:
    @staticmethod
    def get_result(weather_records, year, month=None):
        weather_result = WeatherResult()
        filtered_records = WeatherAnalyzer.get_filtered_records(weather_records, year, month)

        weather_result.max_temperature_record = max(filtered_records, key=lambda p: p.highest_temperature)
        weather_result.min_temperature_record = min(filtered_records, key=lambda p: p.lowest_temperature)
        weather_result.max_humidity_record = max(filtered_records, key=lambda p: p.max_humidity)
        weather_result.max_avg_temperature_record = max(filtered_records, key=lambda p: p.mean_temperature)
        weather_result.min_avg_temperature_record = min(filtered_records, key=lambda p: p.mean_temperature)
        weather_result.mean_humidity = sum(record.mean_humidity for record in filtered_records)/len(filtered_records)

        for daily_data in filtered_records:
            weather_result.daily_temperatures.append(daily_data)

        return weather_result

    @staticmethod
    def get_filtered_records(weather_records, year, month):
        filtered_records = []
        for weather_record in weather_records:
            if (weather_record.date.month == month if month else True) and weather_record.date.year == year:
                filtered_records.append(weather_record)

        return filtered_records
