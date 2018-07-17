from weather_summary_result import WeatherResult


class WeatherResultComputer:
    @staticmethod
    def get_result(weather_records):
        required_readings = WeatherResultComputer._get_weather_reading(weather_records)
        weather_result = WeatherResult()

        weather_result.max_temperature_record = required_readings['max_temperature_record']
        weather_result.min_temperature_record = required_readings['min_temperature_record']
        weather_result.max_humidity_record = required_readings['max_humidity_record']
        weather_result.max_avg_temperature_record = required_readings['max_avg_temperature_record']
        weather_result.min_avg_temperature_record = required_readings['min_avg_temperature_record']

        weather_result.mean_humidity = required_readings['mean_humidity']
        weather_result.daily_temperatures = required_readings['daily_temperatures']

        return weather_result

    @staticmethod
    def _get_weather_reading(weather_records):
        daily_temperatures = []
        for daily_data in weather_records:
            daily_temperatures.append(daily_data)

        required_readings = {
            'max_temperature_record': max(weather_records, key=lambda p: p.highest_temperature),
            'min_temperature_record': min(weather_records, key=lambda p: p.lowest_temperature),
            'max_humidity_record': max(weather_records, key=lambda p: p.max_humidity),
            'max_avg_temperature_record': max(weather_records, key=lambda p: p.mean_temperature),
            'min_avg_temperature_record': min(weather_records, key=lambda p: p.mean_temperature),
            'total_humidity_value': sum(weather_record.mean_humidity for weather_record in weather_records),
            'daily_temperatures': daily_temperatures
        }
        required_readings['mean_humidity'] = required_readings['total_humidity_value']/len(weather_records)

        return required_readings
