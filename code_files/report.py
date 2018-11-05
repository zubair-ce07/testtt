
def calculate_monthly_report(monthly_record):
    """Generate a monthly report"""
    avg_max_temp = average_field_value([i.max_temp for i in monthly_record])
    avg_min_temp = average_field_value([i.min_temp for i in monthly_record])
    avg_mean_humidity = average_field_value([i.mean_humidity for i in monthly_record])

    report = {}
    report['avg_max_temp'] = avg_max_temp
    report['avg_min_temp'] = avg_min_temp
    report['avg_mean_humidity'] = avg_mean_humidity
    return report


def calculate_monthly_graph(monthly_record):
    """Generate a monthly graph with pluses + and minuses -"""
    return zip(
        [i.max_temp for i in monthly_record],
        [i.min_temp for i in monthly_record]
    )


def calculate_yearly_report(yearly_record):
    """Generate a yearly report"""
    max_temp_record = yearly_record[0]
    min_temp_record = yearly_record[0]
    max_humidity_record = yearly_record[0]

    for daily_record in yearly_record:
        if daily_record.max_temp > max_temp_record.max_temp:
            max_temp_record = daily_record 
        if daily_record.min_temp < min_temp_record.min_temp:
            min_temp_record = daily_record
        if daily_record.max_humidity > max_humidity_record.max_humidity:
            max_humidity_record = daily_record

    report = {}
    report['max_temp'] = max_temp_record
    report['min_temp'] = min_temp_record
    report['max_humidity'] = max_humidity_record

    return report


def average_field_value(field_values):
    refined_field_values = [value for value in field_values if value]
    return sum(refined_field_values)/len(refined_field_values)
