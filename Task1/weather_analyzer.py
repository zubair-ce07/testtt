from weather_result import WeatherResult


class WeatherAnalyzer:
    @staticmethod
    def get_result(weather_records, year, month=None):
        weather_result = WeatherResult()
        filtered_records = WeatherAnalyzer.get_filtered_records(weather_records, year, month)

        weather_result.max_temperature_record = WeatherAnalyzer.get_max_temperature(filtered_records)
        weather_result.min_temperature_record = WeatherAnalyzer.get_min_temperature(filtered_records)
        weather_result.max_humidity_record = WeatherAnalyzer.get_max_humidity(filtered_records)
        weather_result.max_avg_temperature_record = WeatherAnalyzer.get_max_avg_temperature(filtered_records)
        weather_result.min_avg_temperature_record = WeatherAnalyzer.get_min_avg_temperature(filtered_records)
        weather_result.mean_humidity = WeatherAnalyzer.get_mean_humidity(filtered_records)
        weather_result.daily_temperatures = filtered_records

        return weather_result

    @staticmethod
    def get_filtered_records(weather_records, year, month):
        filtered_records = []
        for weather_record in weather_records:
            if (weather_record.date.month == month if month else True) and weather_record.date.year == year:
                filtered_records.append(weather_record)

        return filtered_records

    @staticmethod
    def get_max_temperature(filtered_records):
        return max(filtered_records, key=lambda p: p.highest_temperature)

    @staticmethod
    def get_min_temperature(filtered_records):
        return min(filtered_records, key=lambda p: p.lowest_temperature)

    @staticmethod
    def get_max_humidity(filtered_records):
        return max(filtered_records, key=lambda p: p.max_humidity)

    @staticmethod
    def get_max_avg_temperature(filtered_records):
        return max(filtered_records, key=lambda p: p.mean_temperature)

    @staticmethod
    def get_min_avg_temperature(filtered_records):
        return min(filtered_records, key=lambda p: p.mean_temperature)

    @staticmethod
    def get_mean_humidity(filtered_records):
        return sum(record.mean_humidity for record in filtered_records)/len(filtered_records)
