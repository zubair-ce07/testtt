from datetime import datetime


class CalculationsResults:

    def lowest_temp_in_year(self, weather_data):
        min_temp_obj = min(weather_data.all_data_obj,
                           key=lambda day: day.min_temperature if day.min_temperature is not None else 99999999)
        date = datetime.strptime(min_temp_obj.pkt, '%Y-%m-%d')
        return min_temp_obj.min_temperature, date.strftime("%d")+" "+date.strftime("%b")

    def highest_temp_in_year(self, weather_data):
        max_temp_obj = max(weather_data.all_data_obj,
                           key=lambda day: day.max_temperature if day.min_temperature is not None else -99999999)
        date = datetime.strptime(max_temp_obj.pkt, '%Y-%m-%d')
        return max_temp_obj.max_temperature, date.strftime("%d") + " " + date.strftime("%b")

    def most_humid_day_of_year(self, weather_data):
        max_humidity_obj = max(weather_data.all_data_obj,
                           key=lambda day: day.max_humidity if day.min_temperature is not None else -99999999)
        date = datetime.strptime(max_humidity_obj.pkt, '%Y-%m-%d')
        return max_humidity_obj.max_humidity, date.strftime("%d") + " " + date.strftime("%b")
    def avg_lowest_temp(self, weather_data):
        sum_temp = sum(i.min_temperature for i in weather_data.all_data_obj)
        length = len(filter(
            lambda x: x.min_temperature is not None,
            weather_data.all_data_obj
        ))
        return sum_temp/length

    def avg_highest_temp(self, weather_data):
        sum_temp = sum(i.max_temperature for i in weather_data.all_data_obj)
        length = len(filter(
            lambda x: x.max_temperature is not None,
            weather_data.all_data_obj
        ))
        return sum_temp / length


    def avg_mean_humidity(self, weather_data):
        sum_temp = sum(i.mean_humidity for i in weather_data.all_data_obj)
        length = len(filter(
            lambda x: x.mean_humidity is not None,
            weather_data.all_data_obj
        ))
        return sum_temp / length
