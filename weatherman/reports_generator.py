import constants


def display_month_bar_chart(month_records):
    if month_records:
        for record in month_records:            
            print(f'{record.record_date.day} ', end='')
            print("\033[1;34m+\033[1;m" * record.min_temperature, end='')
            print("\033[1;31m+\033[1;m" * record.max_temperature, end='')
            print(f' {record.min_temperature}C-{record.max_temperature}C')
    else:
        print(constants.MONTH_RECORD_NOT_FOUND_ERROR)        
          

def display_yearly_report(yearly_report):
    if yearly_report:   
        max_temp_record = yearly_report['max_temp_record']  
        min_temp_record = yearly_report['min_temp_record']  
        max_humidity_record = yearly_report['max_humidity_record']  
    
        print(f'Highest: {max_temp_record.max_temperature}C on {max_temp_record.record_date.strftime("%B %d")}')
        print(f'Lowest: {min_temp_record.min_temperature}C on {min_temp_record.record_date.strftime("%B %d")}')
        print(f'Humidity: {max_humidity_record.max_humidity}% on {max_humidity_record.record_date.strftime("%B %d")}')    
    else:
        print(constants.YEAR_RECORD_NOT_FOUND_ERROR)    


def display_monthly_report(monthly_report):
    if monthly_report:          
        print(f'Highest Average: {monthly_report["avg_max_temperature"]}C')
        print(f'Lowest Average: {monthly_report["avg_min_temperature"]}C')
        print(f'Average Mean Humidity: {monthly_report["avg_mean_humidity"]}%')
    else:
        print(constants.MONTH_RECORD_NOT_FOUND_ERROR)
