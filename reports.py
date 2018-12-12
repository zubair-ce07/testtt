from operator import attrgetter


def generate_yearly_report(weather_records, date):
    year_records = list(filter(lambda record: record.date.year == date.year, weather_records))

    max_temp_record = max(year_records, key=attrgetter('max_temp'))
    low_temp_record = min(year_records, key=attrgetter('low_temp'))
    humidity_record = max(year_records, key=attrgetter('max_humid'))

    return max_temp_record, low_temp_record, humidity_record


def generate_monthly_report(weather_records, date):
    month_records = extract_month_data(weather_records, date)

    total_records = len(month_records)
    avg_max_temp = sum([record.max_temp for record in month_records]) // total_records
    avg_low_temp = sum([record.low_temp for record in month_records]) // total_records
    avg_mean_humid = sum([record.mean_humid for record in month_records]) // total_records

    return avg_max_temp, avg_low_temp, avg_mean_humid


def generate_bar_chart_report(weather_records, date):
    return extract_month_data(weather_records, date)


def extract_month_data(weather_records, date):
    month_records = []

    for record in weather_records:
        if record.date.year == date.year and record.date.month == date.month:
            month_records.append(record)

    return month_records
