import operator


def yearly_report(weather_records, date):
    dates, max_temp, low_temp, max_humid = [], [], [], []

    for record in weather_records:
        if record.date.year == date.year:
            max_temp.append(record.max_temp)
            low_temp.append(record.low_temp)
            max_humid.append(record.max_humid)
            dates.append(record.date)

    max_tmp_index, max_temp = max(enumerate(max_temp), key=operator.itemgetter(1))
    low_tmp_index, low_temp = min(enumerate(low_temp), key=operator.itemgetter(1))
    max_humid_index, max_humid = max(enumerate(max_humid), key=operator.itemgetter(1))

    max_temp_day = dates[max_tmp_index]
    low_temp_day = dates[low_tmp_index]
    max_humid_day = dates[max_humid_index]

    return {'max_temp': max_temp, 'max_temp_day': max_temp_day, 'low_temp': low_temp,
            'low_temp_day': low_temp_day, 'max_humid': max_humid, 'max_humid_day': max_humid_day}


def monthly_report(weather_records, date):
    month_record = extract_month_data(weather_records, date)

    total_records = len(month_record)
    avg_max_temp = sum(map(lambda record: record['max_temp'], month_record)) // total_records
    avg_low_temp = sum(map(lambda record: record['low_temp'], month_record)) // total_records
    avg_mean_humid = sum(map(lambda record: record['mean_humid'], month_record)) // total_records

    return {'avg_max_temp': avg_max_temp, 'avg_low_temp': avg_low_temp, 'avg_mean_humid': avg_mean_humid}


def bar_chart_report(weather_records, date):
    return extract_month_data(weather_records, date)


def extract_month_data(weather_records, date):
    month_records = []

    for record in weather_records:
        if record.date.year == date.year and record.date.month == date.month:
            month_records.append({'date': record.date, 'max_temp': record.max_temp, 'low_temp': record.low_temp,
                                  'mean_humid': record.mean_humid})

    return month_records
