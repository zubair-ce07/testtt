import weather_result


class WeatherResultComputer:
    @staticmethod
    def get_result_for_e(weather_records):
        if weather_records:
            result = weather_result.WeatherResult()
            result.highest_temperature = max([daily_data.highest_temperature for daily_data in weather_records
                                              if daily_data.highest_temperature != ''])
            result.highest_temperature_day = [daily_data.weather_record_date for daily_data in weather_records
                                              if daily_data.highest_temperature == result.highest_temperature][0]

            result.lowest_temperature = min([daily_data.lowest_temperature for daily_data in weather_records
                                             if daily_data.lowest_temperature != ''])
            result.lowest_temperature_day = [daily_data.weather_record_date for daily_data in weather_records
                                             if daily_data.lowest_temperature == result.lowest_temperature][0]

            result.highest_humidity = max([daily_data.max_humidity for daily_data in weather_records
                                           if daily_data.max_humidity != ''])
            result.most_humid_day = [daily_data.weather_record_date for daily_data in weather_records
                                     if daily_data.max_humidity == result.highest_humidity][0]

            return result

    @staticmethod
    def get_result_for_a(weather_records):
        if weather_records:
            result = weather_result.WeatherResult()
            result.highest_temperature = max([daily_data.highest_temperature for daily_data in weather_records
                                              if daily_data.highest_temperature != ''])

            result.lowest_temperature = min([daily_data.lowest_temperature for daily_data in weather_records
                                             if daily_data.lowest_temperature != ''])

            humidity_values = [daily_data.mean_humidity for daily_data in weather_records
                               if daily_data.mean_humidity != '']

            if len(humidity_values) > 0:
                result.mean_humidity = sum(humidity_values)/len(humidity_values)

            return result

    @staticmethod
    def get_result_for_c(weather_records):
        daily_temperatures = []

        if weather_records:
            for daily_data in weather_records:
                daily_temperatures.append((daily_data.highest_temperature, daily_data.lowest_temperature))

            return weather_result.WeatherResult(daily_temperatures=daily_temperatures)
