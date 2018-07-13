def max_temperature_record(days_list):
    return max(days_list, key=lambda day: day.max_temperature if
               day.max_temperature is not None else 0)


def min_temperature_record(days_list):
    return min(days_list, key=lambda day: day.min_temperature if
               day.min_temperature is not None else 1000)


def max_humidity_record(days_list):
    return max(days_list, key=lambda day: day.max_humidity if
               day.max_humidity is not None else 0)


def total_max_temp_recorded_days(days_list):
    recorded_days = 1
    for i, day in enumerate(days_list):
        if day.max_temperature is not None:
            recorded_days = i
    return recorded_days


def total_min_temp_recorded_days(days_list):
    recorded_days = 1
    for i, day in enumerate(days_list):
        if day.min_temperature is not None:
            recorded_days = i
    return recorded_days


def total_mean_humidity_recorded_days(days_list):
    recorded_days = 1
    for i, day in enumerate(days_list):
        if day.mean_humidity is not None:
            recorded_days = i
    return recorded_days


def get_avg_max_temp(days_list):
    total_days = total_max_temp_recorded_days(days_list)
    return sum(day.max_temperature for day in days_list
               if day.max_temperature is not None)/total_days


def get_avg_min_temp(days_list):
    total_days = total_min_temp_recorded_days(days_list)
    return sum(day.min_temperature for day in days_list
               if day.min_temperature is not None)/total_days


def get_avg_mean_humidity(days_list):
    total_days = total_mean_humidity_recorded_days(days_list)
    return sum(day.mean_humidity for day in days_list
               if day.mean_humidity is not None)/total_days


