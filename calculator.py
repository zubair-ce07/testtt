import statistics
import operator
import calendar


def parse_date(date):
    _, m, d = date.split('-')
    return calendar.month_name[int(m)], int(d)


def compute_year_info(weather_readings):
    max_temperature_day_information = max(weather_readings, key=operator.attrgetter('max_temperature'))
    max_temperature = max_temperature_day_information.max_temperature
    max_temperature_month, max_temperature_day = parse_date(date=max_temperature_day_information.date)

    min_temperature_day_information = min(weather_readings, key=operator.attrgetter('min_temperature'))
    min_temperature = min_temperature_day_information.min_temperature
    min_temperature_month, min_temperature_day = parse_date(date=min_temperature_day_information.date)

    most_humid_day_information = max(weather_readings, key=operator.attrgetter('mean_humidity'))
    most_humidity = most_humid_day_information.mean_humidity
    most_humidity_month, most_humidity_day = parse_date(date=most_humid_day_information.date)

    results = ((max_temperature, max_temperature_month, max_temperature_day),
               (min_temperature, min_temperature_month, min_temperature_day),
               (most_humidity, most_humidity_month, most_humidity_day)
               )
    return results


def compute_month_info(weather_readings):
    highest_average = statistics.mean(weather_reading.max_temperature for weather_reading in weather_readings)
    lowest_average = statistics.mean(weather_reading.min_temperature for weather_reading in weather_readings)
    average_mean_humidity = statistics.mean(weather_reading.mean_humidity for weather_reading in weather_readings)

    return highest_average, lowest_average, average_mean_humidity


def compute_month_temperature_detail(weather_readings):
    return ((parse_date(weather_reading.date)[1], weather_reading.max_temperature, weather_reading.min_temperature)
            for weather_reading in weather_readings)