
def result_e(year, records):
    monthly_max_temperatures = []
    monthly_min_temperatures = []
    monthly_max_humidity = []
    for k, v in records[year].items():
        monthly_max_temperatures.append(max(v, key=lambda wr: wr.max_temperature))
        monthly_min_temperatures.append(min(v, key=lambda wr: wr.min_temperature))
        monthly_max_humidity.append(max(v, key=lambda wr: wr.max_humidity))
    yearly_max_temperature = max(monthly_max_temperatures, key=lambda wr: wr.max_temperature)
    yearly_min_temperature = min(monthly_min_temperatures, key=lambda wr: wr.max_temperature)
    yearly_max_humidity = max(monthly_max_humidity,key=lambda wr: wr.max_humidity)
    return yearly_max_temperature, yearly_min_temperature, yearly_max_humidity


def result_a(month, year, record):
    month = record[year][month[:3]]
    max_avg_temperature = max(month, key=lambda wr: wr.mean_temperature)
    min_avg_temperature = min(month, key=lambda wr: wr.mean_temperature)
    temp2 = sum(month, key=lambda wr: wr.mean_humidity)
    temp = len(x for x in month if x.mean_humidity is not None)
    humidity = temp2/temp
    avg_mean_humidity = filter(lambda wr: wr.mean_humidity == int(humidity), month)
    return max_avg_temperature, min_avg_temperature, avg_mean_humidity


def result_c(month, year, data):
    result = {
        'month': month,
        'year': year,
        'max_temperatures': data[year][month[:3]]['Max TemperatureC'],
        'min_temperatures': data[year][month[:3]]['Min TemperatureC']
    }
    return result
