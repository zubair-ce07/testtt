def year_peak_calculation(year_weather_data):
    calculated_data = []
    max_day = year_weather_data[0]
    min_day = year_weather_data[0]
    max_humidity_day = year_weather_data[0]

    for day_num in range(len(year_weather_data)):
        if max_day.max_temp < year_weather_data[day_num].max_temp:
            max_day = year_weather_data[day_num]
        if min_day.min_temp > year_weather_data[day_num].min_temp:
            min_day = year_weather_data[day_num]
        if max_humidity_day.max_humidity < year_weather_data[day_num].max_humidity:
            max_humidity_day = year_weather_data[day_num]

    calculated_data.append(max_day)
    calculated_data.append(min_day)
    calculated_data.append(max_humidity_day)
    return calculated_data


def month_peak_calculation(month_data):
    calculated_data = []
    max_day = month_data[0]
    min_day = month_data[0]

    for day_num in month_data:
        if max_day.max_temp < day_num.max_temp:
            max_day = day_num
        if min_day.min_temp > day_num.min_temp:
            min_day = day_num

    calculated_data.append(max_day)
    calculated_data.append(min_day)
    return calculated_data


def month_average_calculation(month_data):
    calculated_data = []
    highest_temp = [float(day.max_temp) if day.max_temp else 0 for day in month_data]
    lowest_temp = [float(day.min_temp) if day.min_temp else 0 for day in month_data]
    highest_humidity = [float(day.max_humidity) if day.max_humidity else 0 for day in month_data]

    calculated_data.append(highest_temp)
    calculated_data.append(lowest_temp)
    calculated_data.append(highest_humidity)
    return calculated_data
