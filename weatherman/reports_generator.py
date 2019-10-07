import constants


def display_month_bar_chart(month_records):
    if not month_records:
        print(constants.MONTH_RECORD_NOT_FOUND_ERROR)
        return -1 

    for record in month_records:            
        print(f'{record.record_date.day} ', end='')
        print(constants.MIN_TEMP_CHART_COLOR * record.min_temperature, end='')
        print(constants.MAX_TEMP_CHART_COLOR * record.max_temperature, end='')
        print(f' {record.min_temperature}C-{record.max_temperature}C')            
          

def display_yearly_report(yearly_report):
    if not yearly_report:
        print(constants.YEAR_RECORD_NOT_FOUND_ERROR)
        return -1

    max_temp_record = yearly_report['max_temp_record']  
    min_temp_record = yearly_report['min_temp_record']  
    max_humidity_record = yearly_report['max_humidity_record']  

    print(f'Highest: {max_temp_record.max_temperature}C on {max_temp_record.record_date.strftime("%B %d")}')
    print(f'Lowest: {min_temp_record.min_temperature}C on {min_temp_record.record_date.strftime("%B %d")}')
    print(f'Humidity: {max_humidity_record.max_humidity}% on {max_humidity_record.record_date.strftime("%B %d")}')      


def display_monthly_report(monthly_report):
    if not monthly_report:
        print(constants.MONTH_RECORD_NOT_FOUND_ERROR)
        return -1

    print(f'Highest Average: {monthly_report["avg_max_temperature"]}C')
    print(f'Lowest Average: {monthly_report["avg_min_temperature"]}C')
    print(f'Average Mean Humidity: {monthly_report["avg_mean_humidity"]}%')    
