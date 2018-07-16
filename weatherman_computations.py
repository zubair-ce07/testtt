from statistics import mean
from collections import namedtuple


def extreme_values_days(weather_readings, max_temp, min_temp, max_humid):
    for reading in weather_readings:
        if reading.max_temp == max_temp:
            highest_temp_day = reading.pkt.strftime("%A %B %d")
        if reading.min_temp == min_temp:
            lowest_temp_day = reading.pkt.strftime("%A %B %d")
        if reading.max_humidity == max_humid:
            max_humidity_day = reading.pkt.strftime("%A %B %d")

    return {'max': highest_temp_day, 'min': lowest_temp_day,
            'humid': max_humidity_day}


def calculate_extreme_readings(weather_readings, given_date):

    max_temperature = max(reading.max_temp for reading in weather_readings
                          if reading.pkt.year == given_date.year)
    min_temperature = min(reading.min_temp for reading in weather_readings
                          if reading.pkt.year == given_date.year)
    max_humid = max(reading.max_humidity for reading in weather_readings
                    if reading.pkt.year == given_date.year)

    extreme_days = extreme_values_days(weather_readings, max_temperature,
                                       min_temperature, max_humid)
    max_temp_day = extreme_days.get('max')
    min_temp_day = extreme_days.get('min')
    max_humid_day = extreme_days.get('humid')

    calculation_holder = namedtuple('calculation_holder', 'maximum_temp,\
                                    minimum_temp, maximum_humidity,\
                                    maximum_temp_day, minimum_temp_day,\
                                    maximum_humidity_day')
    return calculation_holder(max_temperature,
                              min_temperature,
                              max_humid,
                              max_temp_day,
                              min_temp_day,
                              max_humid_day)


def calculate_average_readings(weather_readings, given_date):
    mean_temps = list(reading.mean_temp for reading in weather_readings
                      if reading.pkt.year == given_date.year and
                      reading.pkt.month == given_date.month)

    mean_humid = mean(reading.mean_humidity for reading in weather_readings
                      if reading.pkt.year == given_date.year and
                      reading.pkt.month == given_date.month)

    highest_mean_temp = max(mean_temps)
    lowest_mean_temp = min(mean_temps)

    calculation_holder = namedtuple('calculation_holder', 'max_mean_temp,\
                                    min_mean_temp, average_mean_humidity')
    return calculation_holder(highest_mean_temp,
                              lowest_mean_temp,
                              mean_humid)
