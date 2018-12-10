from datetime import datetime


def yearly_report(files_data, year):
    date, max_temp, low_temp, max_humid = [], [], [], []
    for record in files_data:
        record_year = record.date.strftime('%Y')
        if record_year == year:
            max_temp.append(record.max_temp)
            low_temp.append(record.low_temp)
            max_humid.append(record.max_humid)
            date.append(record.date)

    max_temp_value = max(max_temp)
    max_temp_day = date[max_temp.index(max_temp_value)]

    low_temp_value = min(low_temp)
    low_temp_day = date[low_temp.index(low_temp_value)]

    max_humid_value = max(max_humid)
    max_humid_day = date[max_humid.index(max_humid_value)]

    result = {'max_temp': max_temp_value, 'max_temp_day': max_temp_day, 'low_temp': low_temp_value,
              'low_temp_day': low_temp_day, 'max_humid': max_humid_value, 'max_humid_day': max_humid_day}

    return result


def monthly_report(files_data, date):
    year = get_date_formatted(date, '%Y', '%Y/%m')
    month = get_date_formatted(date, '%b', '%Y/%m')
    max_temp, low_temp, mean_humid = [], [], []

    for record in files_data:
        record_year = record.date.strftime('%Y')
        record_month = record.date.strftime('%b')

        if record_year == year and record_month == month:
            max_temp.append(record.max_temp)
            low_temp.append(record.low_temp)
            mean_humid.append(record.mean_humid)

    no_days = len(max_temp)
    avg_max_temp = sum(max_temp) // no_days
    avg_low_temp = sum(low_temp) // no_days
    avg_mean_humid = sum(mean_humid) // no_days

    return {'avg_max_temp': avg_max_temp, 'avg_low_temp': avg_low_temp, 'avg_mean_humid': avg_mean_humid}


def bar_chart_report(files_data, date):
    result = []
    year = get_date_formatted(date, '%Y', '%Y/%m')
    month = get_date_formatted(date, '%b', '%Y/%m')
    
    for record in files_data:
        record_year = record.date.strftime('%Y')
        record_month = record.date.strftime('%b')
        if record_year == year and record_month == month:
            result.append({'date': record.date, 'max_temp': record.max_temp, 'low_temp': record.low_temp})

    return result


def get_date_formatted(date, date_format, source_format):
    return datetime.strptime(date, source_format).strftime(date_format)
