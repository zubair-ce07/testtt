from monthweather import MonthWeatherModel


def execute_task2(file_name):
    month_model = MonthWeatherModel(file_name)
    print("\n")

    high_temp_sum = sum(day_weather.max_temperature for day_weather in month_model.daily_weather_info)
    highest_average = high_temp_sum/len(month_model.daily_weather_info)
    print("Highest Average : " + str(round(highest_average)) + "C")

    low_temp_sum = sum(day_weather.min_temperature for day_weather in month_model.daily_weather_info)
    lowest_average = low_temp_sum / len(month_model.daily_weather_info)
    print("Lowest Average : " + str(round(lowest_average)) + "C")

    mean_humidity_sum = sum(day_weather.mean_humidity for day_weather in month_model.daily_weather_info)
    mean_humidity_average = mean_humidity_sum / len(month_model.daily_weather_info)
    print("Average Mean Humidity: " + str(round(mean_humidity_average)) + "%")
