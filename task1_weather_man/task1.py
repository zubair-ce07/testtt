from monthweather import MonthWeatherModel


def execute_task1(file_names):
    max_temps = []
    min_temps = []
    max_humidities = []

    for file_name in file_names:

        month_model = MonthWeatherModel(file_name)

        max_temp = max(month_model.daily_weather_info, key=lambda x: x.max_temperature)
        min_temp = min(month_model.daily_weather_info, key=lambda x: x.min_temperature)
        max_humidity = max(month_model.daily_weather_info, key=lambda x: x.max_humidity)

        max_temps.append(max_temp)
        min_temps.append(min_temp)
        max_humidities.append(max_humidity)

    max_temp_day = max(max_temps, key=lambda x: x.max_temperature)
    min_temp_day = min(min_temps, key=lambda x: x.min_temperature)
    max_humid_day = max(max_humidities, key=lambda x: x.max_humidity)

    print("Highest:", max_temp_day.max_temperature, "C on", max_temp_day.date.strftime("%B %d"))
    print("Lowest:", min_temp_day.min_temperature, "C on", min_temp_day.date.strftime("%B %d"))
    print("Humidity:", max_humid_day.max_humidity, "% on", max_humid_day.date.strftime("%B %d"))
