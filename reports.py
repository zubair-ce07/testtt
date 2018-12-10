from datetime import datetime


def yearly_report(files_data,  year):
    reading, result = {}, {}
    for record in files_data:
        record_year = datetime.strptime(record.date, '%Y-%m-%d').strftime('%Y')
        if record_year == year:
            reading[record.date] = ({'max_temp': record.max_temp, 'low_temp': record.low_temp, 'max_humid': record.max_humid})

    if reading:
        low_temp_day = min(reading, key=lambda k: reading[k]['low_temp'])
        low_temp = reading.get(low_temp_day)
        low_temp = low_temp.get('low_temp')

        max_humid_day = max(reading, key=lambda k: reading[k]['max_humid'])
        max_humid = reading.get(max_humid_day)
        max_humid = max_humid.get('max_humid')

        max_temp_day = max(reading, key=lambda k: reading[k]['max_temp'])
        max_temp = reading.get(max_temp_day)
        max_temp = max_temp.get('max_temp')

        max_temp_day = datetime.strptime(max_temp_day, '%Y-%m-%d').strftime('%B %d')
        low_temp_day = datetime.strptime(low_temp_day, '%Y-%m-%d').strftime('%B %d')
        max_humid_day = datetime.strptime(max_humid_day, '%Y-%m-%d').strftime('%B %d')

        result = ({'max_temp': max_temp, 'max_temp_day': max_temp_day, 'low_temp': low_temp,
                   'max_humid': max_humid, 'low_temp_day': low_temp_day, 'max_humid_day': max_humid_day})
    return result


def monthly_report(files_data, time_period):
    year = datetime.strptime(time_period, '%Y/%m').strftime('%Y')
    month = datetime.strptime(time_period, '%Y/%m').strftime('%b')
    max_temp, low_temp, mean_humid = [], [], []

    for record in files_data:
        record_year = datetime.strptime(record.date, '%Y-%m-%d').strftime('%Y')
        record_month = datetime.strptime(record.date, '%Y-%m-%d').strftime('%b')

        if (record_year == year) & (record_month == month):
            max_temp.append(record.max_temp)
            low_temp.append(record.low_temp)
            mean_humid.append(record.mean_humid)

    no_days = len(max_temp)

    avg_max_temp = sum(max_temp) // no_days
    avg_low_temp = sum(low_temp) // no_days
    avg_mean_humid = sum(mean_humid) // no_days

    result = ({'avg_max_temp': avg_max_temp, 'avg_low_temp': avg_low_temp, 'avg_mean_humid': avg_mean_humid})

    return result


def bar_chart_report(files_data, time_period):
    output = []
    year = datetime.strptime(time_period, '%Y/%m').strftime('%Y')
    month = datetime.strptime(time_period, '%Y/%m').strftime('%b')

    for record in files_data:
        record_year = datetime.strptime(record.date, '%Y-%m-%d').strftime('%Y')
        record_month = datetime.strptime(record.date, '%Y-%m-%d').strftime('%b')

        if (record_year == year) & (record_month == month):
            day = datetime.strptime(record.date, '%Y-%m-%d').strftime('%d')
            output.append({'day': day,'max_temp': record.max_temp, 'low_temp': record.low_temp})
    return output

