from datetime import datetime


def get_max_temp(days_list):
    return max(days_list, key=lambda day: day.max_temperature if
               day.max_temperature is not None else 0)


def get_min_temp(days_list):
    return min(days_list, key=lambda day: day.min_temperature if
               day.min_temperature is not None else 1000)


def get_max_hum(days_list):
    return max(days_list, key=lambda day: day.max_humidity if
               day.max_humidity is not None else 0)


def get_avg_max_temp(days_list):
    return sum(day.max_temperature for day in days_list
               if day.max_temperature is not None)/len(days_list)


def get_avg_min_temp(days_list):
    return sum(day.min_temperature for day in days_list
               if day.min_temperature is not None)/len(days_list)


def get_avg_mean_hum(days_list):
    return sum(day.mean_humidity for day in days_list
               if day.mean_humidity is not None)/len(days_list)


def date_convert(date):
    return datetime.strptime(date, "%Y-%m-%d").date()

