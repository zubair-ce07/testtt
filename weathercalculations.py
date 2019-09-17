import datetime


def get_highest_temperature_reading(temperature_readings):
    max_temperature_reading = temperature_readings[0]
    for reading in temperature_readings:
        if reading.max_temperature_c is not None:
            if reading.max_temperature_c > max_temperature_reading.max_temperature_c:
                max_temperature_reading = reading

    return max_temperature_reading


def get_lowest_temperature_reading(temperature_readings):
    min_temperature_reading = temperature_readings[0]
    for reading in temperature_readings:
        if reading.min_temperature_c is not None:
            if reading.min_temperature_c < min_temperature_reading.min_temperature_c:
                min_temperature_reading = reading

    return min_temperature_reading


def get_most_humid_day(temperature_readings):
    most_humid_day = temperature_readings[0]
    for reading in temperature_readings:
        if reading.max_humidity is not None:
            if reading.max_humidity > most_humid_day.max_humidity:
                most_humid_day = reading

    return most_humid_day


def get_highest_temperature_average_reading(temperature_readings):
    sum_of_temperatures = 0
    no_of_readings = 0
    for reading in temperature_readings:
        if reading.max_temperature_c is not None:
            sum_of_temperatures = sum_of_temperatures + reading.max_temperature_c
            no_of_readings = no_of_readings + 1

    return sum_of_temperatures // no_of_readings


def get_lowest_temperature_average_reading(temperature_readings):
    sum_of_temperatures = 0
    no_of_readings = 0
    for reading in temperature_readings:
        if reading.min_temperature_c is not None:
            sum_of_temperatures = sum_of_temperatures + reading.min_temperature_c
            no_of_readings = no_of_readings + 1

    return sum_of_temperatures // no_of_readings


def get_mean_humid_day_average(temperature_readings):
    sum_of_temperatures = 0
    no_of_readings = 0
    for reading in temperature_readings:
        if reading.mean_humidity is not None:
            sum_of_temperatures = sum_of_temperatures + reading.mean_humidity
            no_of_readings = no_of_readings + 1

    return sum_of_temperatures // no_of_readings


def draw_chart_for_lowest_and_highest_temperature_each_day(weather_readings):
    reading_month = datetime.datetime.strptime(weather_readings[0].reading_date, '%Y-%m-%d')
    print(reading_month.strftime('%B'), reading_month.strftime('%Y'))
    for reading in weather_readings:
        reading_date = datetime.datetime.strptime(reading.reading_date, '%Y-%m-%d')
        if reading.min_temperature_c is not None:
            print("\033[0;35;2m{} ".format(reading_date.strftime('%d')),
                  ("\033[0;34;2m{}".format('+')*reading.min_temperature_c),
                  '\033[0;35;2m{}C'.format(reading.min_temperature_c))
        if reading.max_temperature_c is not None:
            print("\033[0;35;2m{} " .format(reading_date.strftime('%d')),
                  ("\033[0;31;2m{}" .format('+')*reading.max_temperature_c),
                  '\033[0;35;2m{}C'.format(reading.max_temperature_c))


def draw_chart_for_lowest_and_highest_temperature_each_day_bonus(weather_readings):
    reading_month = datetime.datetime.strptime(weather_readings[0].reading_date, '%Y-%m-%d')
    print(reading_month.strftime('%B'), reading_month.strftime('%Y'))
    for reading in weather_readings:
        reading_date = datetime.datetime.strptime(reading.reading_date, '%Y-%m-%d')
        if reading.min_temperature_c is not None:
            bars = "\033[0;34;2m{}".format('+')*reading.min_temperature_c + \
                   "\033[0;31;2m{}" .format('+')*reading.max_temperature_c
            print("\033[0;35;2m{} ".format(reading_date.strftime('%d')), bars,
                  " \033[0;35;2m{}C".format(reading.min_temperature_c), '-'
                  " \033[0;35;2m{}C".format(reading.max_temperature_c))
