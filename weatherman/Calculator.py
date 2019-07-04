
def minimum_value(weather_data, key):
    filtered_readings = [row for row in weather_data if key(row)]
    return min(filtered_readings, key=key)


def maximum_value(weather_data, key):
    filtered_readings = [row for row in weather_data if key(row)]
    return max(filtered_readings, key=key)


def mean_value(weather_data, key):
    filtered_readings = [key(row) for row in weather_data if key(row)]
    return sum(filtered_readings) / len(filtered_readings)
