from datetime import date
from datetime import datetime
from statistics import mean

from weatherman_data_structure import CalculationHolder


def str_to_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d')


def extreme_values_days(weather_readings, max_temp, min_temp,
                        max_humid, extreme_type):
    if extreme_type == 'max':
        for row in weather_readings:
            if row.max_temp == max_temp:
                highest_temp_day = str_to_date(row.pkt).ctime()[:-14]
        return highest_temp_day
    elif extreme_type == 'min':
        for row in weather_readings:
            if row.min_temp == min_temp:
                lowest_temp_day = str_to_date(row.pkt).ctime()[:-14]
        return lowest_temp_day
    else:
        for row in weather_readings:
            if row.max_humidity == max_humid:
                max_humidity_day = str_to_date(row.pkt).ctime()[:-14]
        return max_humidity_day


def calculate_extreme_readings(weather_readings, given_date):

    ext_max_temp = max(row.max_temp for row in weather_readings
                       if str_to_date(row.pkt).year == given_date.year)
    ext_min_temp = min(row.min_temp for row in weather_readings
                       if str_to_date(row.pkt).year == given_date.year)
    ext_max_humid = max(row.max_humidity for row in weather_readings
                        if str_to_date(row.pkt).year == given_date.year)

    max_temp_day = extreme_values_days(weather_readings, ext_max_temp,
                                       ext_min_temp, ext_max_humid, 'max')
    min_temp_day = extreme_values_days(weather_readings, ext_max_temp,
                                       ext_min_temp, ext_max_humid, 'min')
    max_humid_day = extreme_values_days(weather_readings, ext_max_temp,
                                        ext_min_temp, ext_max_humid, 'humid')

    return CalculationHolder(max_temp=ext_max_temp, min_temp=ext_min_temp,
                             max_humidity=ext_max_humid,
                             max_temp_day=max_temp_day,
                             min_temp_day=min_temp_day,
                             max_humid_day=max_humid_day)


def calculate_average_readings(weather_readings, given_date):
    mean_temps = list(row.mean_temp for row in weather_readings
                      if str_to_date(row.pkt).year == given_date.year and
                      str_to_date(row.pkt).month == given_date.month)

    mean_humid = mean(row.mean_humidity for row in weather_readings
                      if str_to_date(row.pkt).year == given_date.year and
                      str_to_date(row.pkt).month == given_date.month)

    highest_mean_temp = max(mean_temps)
    lowest_mean_temp = min(mean_temps)

    return CalculationHolder(max_mean_temp=highest_mean_temp,
                             min_mean_temp=lowest_mean_temp,
                             avg_mean_humidity=mean_humid)


def calculate_readings(weather_readings, report_type, given_date):
    if report_type == 'e':
        return calculate_extreme_readings(weather_readings, given_date)

    if report_type == 'a':
        return calculate_average_readings(weather_readings, given_date)
