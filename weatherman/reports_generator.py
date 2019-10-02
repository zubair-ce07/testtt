import constants


def display_month_bar_chart(monthly_records):
    if monthly_records:
        for (max_temp, min_temp, record_date) in zip(monthly_records['max_temperatures'],
                monthly_records['min_temperatures'], monthly_records['weather_record_date']):            
            print(f'{record_date.day} ', end='')
            print("\033[1;34m+\033[1;m" * min_temp, end='')
            print("\033[1;31m+\033[1;m" * max_temp, end='')
            print(f' {min_temp}C-{max_temp}C')
    else:
        print(constants.MONTH_DATA_NOT_FOUND_ERROR)        
          

def display_yearly_report(yearly_report):
    if yearly_report:   
        max_temp_record = yearly_report['max_temp_record']  
        min_temp_record = yearly_report['min_temp_record']  
        max_humidity_record = yearly_report['max_humidity_record']  
    
        print(f'Highest: {max_temp_record.max_temperature}C on {max_temp_record.weather_record_date.strftime("%B %d")}')
        print(f'Lowest: {min_temp_record.min_temperature}C on {min_temp_record.weather_record_date.strftime("%B %d")}')
        print(f'Humidity: {max_humidity_record.max_humidity}% on {max_humidity_record.weather_record_date.strftime("%B %d")}')    
    else:
        print(constants.YEAR_DATA_NOT_FOUND_ERROR)    


def display_monthly_report(monthly_report):
    if monthly_report:          
        print(f'Highest Average: {monthly_report["avg_max_temperature"]}C')
        print(f'Lowest Average: {monthly_report["avg_min_temperature"]}C')
        print(f'Average Mean Humidity: {monthly_report["avg_mean_humidity"]}%')
    else:
        print(constants.MONTH_DATA_NOT_FOUND_ERROR)
