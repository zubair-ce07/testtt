
def minimum_temperature_calculate(data):
    """"Calculates the minimum temperature and day through out the year"""
    first_iteration = True
    for month in data:
        for day in month.days:
            if day.readings['Mean TemperatureC'] == '':
                continue
            if first_iteration:
                minimum_temperature_date = day.readings['PKT']
                minimum_temperature = int(day.readings['Mean TemperatureC'])
                first_iteration = False
            temperature = int(day.readings['Mean TemperatureC'])
            if temperature < minimum_temperature:
                minimum_temperature = temperature
                minimum_temperature_date = day.readings['PKT']

    return [minimum_temperature_date, str(minimum_temperature)]


def maximum_temperature_calculate(data):
    """"Calculates the maximum temperature and day through out the year"""
    first_iteration = True

    for month in data:
        for day in month.days:
            if day.readings['Mean TemperatureC'] == '':
                continue
            if first_iteration:
                maximum_temperature_date = day.readings['PKT']
                maximum_temperature = int(day.readings['Mean TemperatureC'])
                first_iteration = False
            temperature = int(day.readings['Mean TemperatureC'])
            if temperature > maximum_temperature:
                maximum_temperature = temperature
                maximum_temperature_date = day.readings['PKT']

    return [maximum_temperature_date, str(maximum_temperature)]


def maximum_humidity_calculate(data):
    """"Calculates the day when the humidity was highest through out the year"""
    first_iteration = True

    for month in data:
        for day in month.days:
            if day.readings[' Mean Humidity'] == '':
                continue
            if first_iteration:
                maximum_humidity_date = day.readings['PKT']
                maximum_humidity = int(day.readings[' Mean Humidity'])
                first_iteration = False
            humidity = int(day.readings[' Mean Humidity'])
            if humidity > maximum_humidity:
                maximum_humidity = humidity
                maximum_humidity_date = day.readings['PKT']

    return [maximum_humidity_date, str(maximum_humidity)]


def average_maximum_temperature_calculate(data):
    total_temperature = 0
    days_count = 0
    for month in data:
        for day in month.days:
            if day.readings['Max TemperatureC'] == '':
                continue
            temperature = int(day.readings['Max TemperatureC'])
            total_temperature = total_temperature + temperature
            days_count += 1

    return str(total_temperature//days_count)


def average_minimum_temperature_calculate(data):
    total_temperature = 0
    days_count = 0
    for month in data:
        for day in month.days:
            if day.readings['Min TemperatureC'] == '':
                continue
            temperature = int(day.readings['Min TemperatureC'])
            total_temperature = total_temperature + temperature
            days_count += 1

    return str(total_temperature // days_count)


def average_humidity_calculate(data):
    total_humidity = 0
    days_count = 0
    for month in data:
        for day in month.days:
            if day.readings[' Mean Humidity'] == '':
                continue
            humidity = int(day.readings[' Mean Humidity'])
            total_humidity = total_humidity + humidity
            days_count += 1

    return str(total_humidity // days_count)