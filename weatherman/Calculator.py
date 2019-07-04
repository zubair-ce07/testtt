
def minimum_value(weather_data, key):
    return min(weather_data, key=key)


def maximum_value(weather_data, key):
    return max(weather_data, key=key)


def mean_value(weather_data, key):
    filtered_readings = [key(row) for row in weather_data if key(row)]
    return sum(filtered_readings) / len(filtered_readings)
