
def result_e(year, data):
    sub_results = {
            'Jan': None,
            'Feb': None,
            'Mar': None,
            'Apr': None,
            'May': None,
            'Jun': None,
            'Jul': None,
            'Aug': None,
            'Sep': None,
            'Oct': None,
            'Nov': None,
            'Dec': None,
        }
    for k, v in data[year].items():
        if v:
            pkt = v['PKT']
            max_temperatures = v['Max TemperatureC']
            min_temperatures = v['Min TemperatureC']
            max_humidity = v['Max Humidity']
            temp = {
                'max_temperature': {'temperature': None, 'date': None},
                'min_temperature': {'temperature': None, 'date': None},
                'max_humidity': {'humidity': None, 'date': None}
            }
            for i in range(len(max_temperatures)):
                if max_temperatures[i] is not None:
                    if (temp['max_temperature']['temperature'] is None
                            or max_temperatures[i] > temp['max_temperature']['temperature']):
                        temp['max_temperature']['temperature'] = max_temperatures[i]
                        temp['max_temperature']['date'] = pkt[i]
                if min_temperatures[i] is not None:
                    if (temp['min_temperature']['temperature'] is None
                            or min_temperatures[i] < temp['min_temperature']['temperature']):
                        temp['min_temperature']['temperature'] = min_temperatures[i]
                        temp['min_temperature']['date'] = pkt[i]
                if max_humidity[i] is not None:
                    if (temp['max_humidity']['humidity'] is None
                            or max_humidity[i] > temp['max_humidity']['humidity']):
                        temp['max_humidity']['humidity'] = max_humidity[i]
                        temp['max_humidity']['date'] = pkt[i]
            sub_results[k] = temp
    result = {
        'max_temperature': {'temperature': None, 'date': None},
        'min_temperature': {'temperature': None, 'date': None},
        'max_humidity': {'humidity': None, 'date': None}
    }
    for k, v in sub_results.items():
        if v:
            if v['max_temperature']['temperature'] is not None:
                if (result['max_temperature']['temperature'] is None
                        or v['max_temperature']['temperature'] > result['max_temperature']['temperature']):
                    result['max_temperature']['temperature'] = v['max_temperature']['temperature']
                    result['max_temperature']['date'] = v['max_temperature']['date']
            if v['min_temperature']['temperature'] is not None:
                if (result['min_temperature']['temperature'] is None
                        or v['min_temperature']['temperature'] < result['min_temperature']['temperature']):
                    result['min_temperature']['temperature'] = v['min_temperature']['temperature']
                    result['min_temperature']['date'] = v['min_temperature']['date']
            if v['max_humidity']['humidity'] is not None:
                if (result['max_humidity']['humidity'] is None
                        or v['max_humidity']['humidity'] > result['max_humidity']['humidity']):
                    result['max_humidity']['humidity'] = v['max_humidity']['humidity']
                    result['max_humidity']['date'] = v['max_humidity']['date']
    return result


def result_a(month, year, data):
    avg_temperatures = data[year][month[:3]]['Mean TemperatureC']
    mean_humidity = data[year][month[:3]]['Mean Humidity']
    result = {
        'max_avg_temperature': None,
        'min_avg_temperature': None,
        'max_avg_humidity': None
    }
    for i in range(len(avg_temperatures)):
        if avg_temperatures[i] is not None:
            if result['max_avg_temperature'] is None or avg_temperatures[i] > result['max_avg_temperature']:
                result['max_avg_temperature'] = avg_temperatures[i]
        if avg_temperatures[i] is not None:
            if result['min_avg_temperature'] is None or avg_temperatures[i] < result['min_avg_temperature']:
                result['min_avg_temperature'] = avg_temperatures[i]
        if mean_humidity[i] is not None:
            if result['max_avg_humidity'] is None or mean_humidity[i] > result['max_avg_humidity']:
                result['max_avg_humidity'] = mean_humidity[i]
    return result


def result_c(month, year, data):
    result = {
        'month': month,
        'year': year,
        'max_temperatures': data[year][month[:3]]['Max TemperatureC'],
        'min_temperatures': data[year][month[:3]]['Min TemperatureC']
    }
    return result
