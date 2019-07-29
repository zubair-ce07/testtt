from weather_result import WeatherResult


class WeatherCalculations:
    @staticmethod
    def get_weather_results(data, year, month=''):
        results = WeatherResult()
        filter_records = WeatherCalculations.filter_records(data, year, month)
        maximum_temperature = WeatherCalculations.get_max_temp(filter_records)
        minimum_temperature = WeatherCalculations.get_min_temp(filter_records)
        maximum_humidity = WeatherCalculations.get_max_humidity(filter_records)
        max_avg_temp = WeatherCalculations.get_max_avg(filter_records)
        min_avg_temp = WeatherCalculations.get_min_avg(filter_records)
        mean_humidity = WeatherCalculations.get_avg_humidity(filter_records)
        results.max_temp = maximum_temperature
        results.min_temp = minimum_temperature
        results.max_humidity = maximum_humidity
        results.max_avg_temp = max_avg_temp
        results.min_avg_temp = min_avg_temp
        results.mean_humidity = mean_humidity
        results.monthly_temp = filter_records
        return results

    @staticmethod
    def filter_records(weather_records, year, month):
        required_records = []
        for row in weather_records:
            if (row.date.month == month if month else True) and row.date.year == year:
                required_records.append(row)
        return required_records

    @staticmethod
    def get_max_temp(filter_records):
        return max(filter_records, key=lambda weather_records: weather_records.max_temp)

    @staticmethod
    def get_min_temp(filter_records):
        return min(filter_records, key=lambda weather_records: weather_records.min_temp)

    @staticmethod
    def get_max_humidity(filter_records):
        return max(filter_records, key=lambda weather_records: weather_records.max_humidity)

    @staticmethod
    def get_max_avg(filter_records):
        return max(filter_records, key=lambda weather_records: weather_records.mean_temp)

    @staticmethod
    def get_min_avg(filter_records):
        return min(filter_records, key=lambda weather_records: weather_records.mean_temp)

    @staticmethod
    def get_avg_humidity(filter_records):
        return sum(record.mean_humidity for record in filter_records) / len(filter_records)

