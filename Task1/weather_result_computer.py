import weather_summary_result


class WeatherResultComputer:
    @staticmethod
    def get_result(weather_records):
        weather_result = weather_summary_result.WeatherResult()

        h_temp_weather_record = max(weather_records, key=lambda p: p.highest_temperature)
        weather_result.highest_temperature = h_temp_weather_record.highest_temperature
        weather_result.highest_temperature_day = h_temp_weather_record.weather_record_date

        l_temp_weather_record = min(weather_records, key=lambda p: p.lowest_temperature)
        weather_result.lowest_temperature = l_temp_weather_record.lowest_temperature
        weather_result.lowest_temperature_day = l_temp_weather_record.weather_record_date

        h_humid_weather_record = max(weather_records, key=lambda p: p.max_humidity)
        weather_result.highest_humidity = h_humid_weather_record.max_humidity
        weather_result.most_humid_day = h_humid_weather_record.weather_record_date

        h_temp_weather_record = max(weather_records, key=lambda p: p.mean_temperature)
        weather_result.highest_temperature = h_temp_weather_record.highest_temperature

        l_temp_weather_record = min(weather_records, key=lambda p: p.mean_temperature)
        weather_result.lowest_temperature = l_temp_weather_record.lowest_temperature

        total_humidity_value = sum(weather_record.mean_humidity for weather_record in weather_records)
        weather_result.mean_humidity = total_humidity_value/len(weather_records)

        for daily_data in weather_records:
            weather_result.daily_temperatures.append((daily_data.highest_temperature,
                                                      daily_data.lowest_temperature))

        return weather_result
