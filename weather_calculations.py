from weather_result import WeatherResult


class WeatherCalculations:
    @staticmethod
    def get_weather_results(data, year, month=''):
        results = WeatherResult()
        required_records = WeatherCalculations.get_required_records(data, year, month)
        maximum_temperature, minimum_temperature, maximum_humidity =\
            WeatherCalculations.get_max_min(required_records)
        max_avg_temp, min_avg_temp, mean_humidity =\
            WeatherCalculations.get_max_min_avg(required_records)
        results.max_temp = maximum_temperature
        results.min_temp = minimum_temperature
        results.max_humidity = maximum_humidity
        results.max_avg_temp = max_avg_temp
        results.min_avg_temp = min_avg_temp
        results.mean_humidity = mean_humidity
        results.monthly_temp = required_records
        return results

    @staticmethod
    def get_required_records(weather_records, year, month):
        required_records = []
        for row in weather_records:
            if (row.date.month == month if month else True) and row.date.year == year:
                required_records.append(row)

        return required_records

    @staticmethod
    def get_max_min(required_records):
        max_temp_record = max(required_records, key=lambda weatherdata: weatherdata.max_temp)
        min_temp_record = min(required_records, key=lambda weatherdata: weatherdata.min_temp)
        max_humidity_record = max(required_records, key=lambda weatherdata: weatherdata.max_humidity)
        return [max_temp_record, min_temp_record, max_humidity_record]

    @staticmethod
    def get_max_min_avg(required_records):
        max_avg_temp = min(required_records, key=lambda weatherdata: weatherdata.mean_temperature)
        min_avg_temp = min(required_records, key=lambda weatherdata: weatherdata.mean_temperature)
        mean_humidity = sum(record.mean_humidity for record in required_records) / len(required_records)
        return[max_avg_temp, min_avg_temp, mean_humidity]
