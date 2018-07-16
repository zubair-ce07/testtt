def max_temperature_record(readings):
    readings = [day for day in readings if day.max_temperature]
    return max(readings, key=lambda day: day.max_temperature)


def min_temperature_record(readings):
    readings = [day for day in readings if day.min_temperature]
    return min(readings, key=lambda day: day.min_temperature)


def max_humidity_record(readings):
    readings = [day for day in readings if day.max_humidity]
    return max(readings, key=lambda day: day.max_humidity)


def get_avg_max_temp(readings):
    total_days = len([day for day in readings if day.max_temperature])
    return sum(day.max_temperature for day in readings
               if day.max_temperature)//total_days


def get_avg_min_temp(readings):
    total_days = len([day for day in readings if day.min_temperature])
    return sum(day.min_temperature for day in readings
               if day.min_temperature )//total_days


def get_avg_mean_humidity(readings):
    total_days = len([day for day in readings if day.mean_humidity])
    return sum(day.mean_humidity for day in readings
               if day.mean_humidity)//total_days


