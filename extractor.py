import statistics


def extract_year_info(weather_readings):
    max_temperature_day_information = max(weather_readings, key=lambda reading: reading.max_temperature)
    min_temperature_day_information = min(weather_readings, key=lambda reading: reading.min_temperature)
    most_humid_day_information = max(weather_readings, key=lambda reading: reading.mean_humidity)

    return max_temperature_day_information, min_temperature_day_information, most_humid_day_information


def extract_month_info(weather_readings):
    highest_average = statistics.mean(weather_reading.max_temperature for weather_reading in weather_readings)
    lowest_average = statistics.mean(weather_reading.min_temperature for weather_reading in weather_readings)
    average_mean_humidity = statistics.mean(weather_reading.mean_humidity for weather_reading in weather_readings)

    return highest_average, lowest_average, average_mean_humidity
