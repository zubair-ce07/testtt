import weather_result_container


class WeatherSummary:
    date_key = "PKT"

    @staticmethod
    def get_result_for_e(data):
        result = weather_result_container.WeatherResultContainer()

        result.highest_temperature = max([daily_data.highest_temperature for daily_data in data
                                          if daily_data.highest_temperature != 'NA'])
        result.highest_temperature_day = [daily_data.date for daily_data in data
                                          if daily_data.highest_temperature == result.highest_temperature][0]

        result.lowest_temperature = min([daily_data.lowest_temperature for daily_data in data
                                         if daily_data.lowest_temperature != 'NA'])
        result.lowest_temperature_day = [daily_data.date for daily_data in data
                                         if daily_data.lowest_temperature == result.lowest_temperature][0]

        result.highest_humidity = max([daily_data.max_humidity for daily_data in data
                                       if daily_data.max_humidity != 'NA'])
        result.most_humid_day = [daily_data.date for daily_data in data
                                 if daily_data.max_humidity == result.highest_humidity][0]

        return result

    @staticmethod
    def get_result_for_a(data):
        result = weather_result_container.WeatherResultContainer()

        result.highest_temperature = max([daily_data.highest_temperature for daily_data in data
                                          if daily_data.highest_temperature != 'NA'])

        result.lowest_temperature = min([daily_data.lowest_temperature for daily_data in data
                                         if daily_data.lowest_temperature != 'NA'])

        humidity_values = [daily_data.mean_humidity for daily_data in data
                           if daily_data.mean_humidity != 'NA']

        if len(humidity_values) > 0:
            result.mean_humidity = sum(humidity_values)/len(humidity_values)
        else:
            result.mean_humidity = "NA"

        return result

    @staticmethod
    def get_result_for_c(data):
        result = weather_result_container.WeatherResultContainer()

        for daily_data in data:
            result.temperature_list.append((daily_data.highest_temperature, daily_data.lowest_temperature))

        return result
