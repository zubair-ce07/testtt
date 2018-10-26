from math import inf


class Calculations:

    def calculate_extreme_weather(self, weather_data):
        extreme_weather = {
            "max_temp_date": None, "max_temp": -inf,
            "min_temp_date": None, "min_temp": +inf,
            "max_humidity_date": None, "max_humidity": -inf
        }
        for data in weather_data:

            if data["Max TemperatureC"]:
                if extreme_weather["max_temp"] <= int(data["Max TemperatureC"]):
                    extreme_weather["max_temp_date"] = data["PKT"]
                    extreme_weather["max_temp"] = int(data["Max TemperatureC"])

            if data["Min TemperatureC"]:
                if extreme_weather["min_temp"] >= int(data["Min TemperatureC"]):
                    extreme_weather["min_temp_date"] = data["PKT"]
                    extreme_weather["min_temp"] = int(data["Min TemperatureC"])

            if data["Max Humidity"]:
                if extreme_weather["max_humidity"] <= int(data["Max Humidity"]):
                    extreme_weather["max_humidity_date"] = data["PKT"]
                    extreme_weather["max_humidity"] = int(data["Max Humidity"])
        return extreme_weather

    def calculate_average_weather(self, weather_data):
        sum_max_temp = 0
        max_temp_count = 0
        sum_min_temp = 0
        min_temp_count = 0
        sum_mean_humidity = 0
        mean_humidity_count = 0
        for data in weather_data:

            if data["Max TemperatureC"]:
                sum_max_temp += int(data["Max TemperatureC"])
                max_temp_count += 1

            if data["Min TemperatureC"]:
                sum_min_temp += int(data["Min TemperatureC"])
                min_temp_count += 1

            if data[" Mean Humidity"]:
                sum_mean_humidity += int(data[" Mean Humidity"])
                mean_humidity_count += 1
        average_weather = {"avg_max_temp": sum_max_temp // max_temp_count,
                           "avg_min_temp": sum_min_temp // min_temp_count,
                           "avg_mean_humidity": (sum_mean_humidity // mean_humidity_count)}
        return average_weather
