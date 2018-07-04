
def minimum_temperature_calculate(data):
    """"Calculates the minimum temperature and day through out the year"""
    minimum_temperature_date = data[0].days[0].readings['PKT']
    minimum_temperature = int(data[0].days[0].readings['Min TemperatureC'])
    for month in data:
        for day in month.days:
            if day.readings['Min TemperatureC'] == '':
                continue
            temperature = int(day.readings['Min TemperatureC'])
            if temperature < minimum_temperature:
                minimum_temperature = temperature
                minimum_temperature_date = day.readings['PKT']

    print(minimum_temperature_date+" : "+str(minimum_temperature))


def maximum_temperature_calculate(data):
    """"Calculates the maximum temperature and day through out the year"""
    maximum_temperature_date = data[0].days[0].readings['PKT']
    maximum_temperature = int(data[0].days[0].readings['Max TemperatureC'])
    for month in data:
        for day in month.days:
            if day.readings['Max TemperatureC'] == '':
                continue
            temperature = int(day.readings['Max TemperatureC'])
            if temperature > maximum_temperature:
                maximum_temperature = temperature
                maximum_temperature_date = day.readings['PKT']

    print(maximum_temperature_date+" : "+str(maximum_temperature))


def maximum_humidity_calculate(data):
    """"Calculates the day when the humidity was highest through out the year"""
    maximum_humidity_date = data[0].days[0].readings['PKT']
    maximum_humidity = int(data[0].days[0].readings['Max Humidity'])
    for month in data:
        for day in month.days:
            print(day.readings['Max Humidity'])
            if day.readings['Max Humidity'] == '':
                continue
            humidity = int(day.readings['Max Humidity'])
            if humidity > maximum_humidity:
                maximum_humidity = humidity
                maximum_humidity_date = day.readings['PKT']

    print(maximum_humidity_date + " : " + str(maximum_humidity))