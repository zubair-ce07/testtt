
def minimum_value(weather_data, key):
    min_temp_obj = min(weather_data,
                       key=key)
    return min_temp_obj


def maximum_value(weather_data, key):
    max_temp_obj = max(weather_data,
                       key=key)
    return max_temp_obj


def mean_value(weather_data, key):
    filtered_readings = [key(row) for row in weather_data if key(row)]
    return sum(filtered_readings) / len(filtered_readings)
