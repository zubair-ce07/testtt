from statistics import mean
from collections import namedtuple
from operator import attrgetter


def calculate_ext_readings(weather_readings):

    max_temperatures = list(filter(attrgetter('max_temp'), weather_readings))
    min_temperatures = list(filter(attrgetter('min_temp'), weather_readings))
    max_humidity = list(filter(attrgetter('max_humidity'), weather_readings))

    max_temperature = max(max_temperatures, key=attrgetter('max_temp'))
    min_temperature = min(min_temperatures, key=attrgetter('min_temp'))
    max_humid = max(max_humidity, key=attrgetter('max_humidity'))

    calculation_holder = namedtuple('calculation_holder', 'maximum_temp,\
                                    minimum_temp, maximum_humidity,\
                                    maximum_temp_day, minimum_temp_day,\
                                    maximum_humidity_day')
    return calculation_holder(max_temperature.max_temp,
                              min_temperature.min_temp,
                              max_humid.max_humidity,
                              max_temperature.pkt.strftime("%A %B %d"),
                              min_temperature.pkt.strftime("%A %B %d"),
                              max_humid.pkt.strftime("%A %B %d"))


def calculate_avg_readings(weather_readings):
    mean_temps = list(filter(attrgetter('mean_temp'), weather_readings))
    mean_humid = list(filter(attrgetter('mean_humidity'), weather_readings))

    mean_value = mean(m.mean_humidity for m in mean_humid)

    highest_mean_temp = max(mean_temps, key=attrgetter('mean_temp'))
    lowest_mean_temp = min(mean_temps, key=attrgetter('mean_temp'))

    calculation_holder = namedtuple('calculation_holder', 'max_mean_temp,\
                                    min_mean_temp, average_mean_humidity')
    return calculation_holder(highest_mean_temp.mean_temp,
                              lowest_mean_temp.mean_temp,
                              mean_value)
