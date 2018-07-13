from datetime import date
from datetime import datetime
from statistics import mean

from weatherman_data_structure import CalculationHolder


def str_to_date(str_date, format='%Y-%m-%d'):
    return datetime.strptime(str_date, format)


def extreme_values_days(weather_readings, max_temp, min_temp, max_humid):
    for reading in weather_readings:
        if reading.max_temp == max_temp:
            highest_temp_day = str_to_date(reading.pkt).strftime("%A %B %d")
        if reading.min_temp == min_temp:
            lowest_temp_day = str_to_date(reading.pkt).strftime("%A %B %d")
        if reading.max_humidity == max_humid:
            max_humidity_day = str_to_date(reading.pkt).strftime("%A %B %d")

    return {'max': highest_temp_day, 'min': lowest_temp_day,
            'humid': max_humidity_day}


def calculate_extreme_readings(weather_readings, given_date):

    ext_max_temp = max(reading.max_temp for reading in weather_readings
                       if str_to_date(reading.pkt).year == given_date.year)
    ext_min_temp = min(reading.min_temp for reading in weather_readings
                       if str_to_date(reading.pkt).year == given_date.year)
    ext_max_humid = max(reading.max_humidity for reading in weather_readings
                        if str_to_date(reading.pkt).year == given_date.year)

    extreme_days = extreme_values_days(weather_readings, ext_max_temp,
                                       ext_min_temp, ext_max_humid)
    max_temp_day = extreme_days.get('max')
    min_temp_day = extreme_days.get('min')
    max_humid_day = extreme_days.get('humid')

    return CalculationHolder(max_temp=ext_max_temp, min_temp=ext_min_temp,
                             max_humidity=ext_max_humid,
                             max_temp_day=max_temp_day,
                             min_temp_day=min_temp_day,
                             max_humid_day=max_humid_day)


def calculate_average_readings(weather_readings, given_date):
    mean_temps = list(reading.mean_temp for reading in weather_readings
                      if str_to_date(reading.pkt).year == given_date.year and
                      str_to_date(reading.pkt).month == given_date.month)

    mean_humid = mean(reading.mean_humidity for reading in weather_readings
                      if str_to_date(reading.pkt).year == given_date.year and
                      str_to_date(reading.pkt).month == given_date.month)

    highest_mean_temp = max(mean_temps)
    lowest_mean_temp = min(mean_temps)

    return CalculationHolder(max_mean_temp=highest_mean_temp,
                             min_mean_temp=lowest_mean_temp,
                             avg_mean_humidity=mean_humid)
