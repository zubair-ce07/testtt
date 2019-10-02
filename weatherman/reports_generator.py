import error_messages


def display_month_bar_chart(min_max_record):        
    max_temp_values = min_max_record['max_temperatures']
    min_temp_values = min_max_record['min_temperatures']
    day_counter = 1
    
    for (max_temp, min_temp) in zip(max_temp_values, min_temp_values):            
        print(f'{day_counter} ', end='')
        print("\033[1;34m+\033[1;m" * min_temp, end='')
        print("\033[1;31m+\033[1;m" * max_temp, end='')
        print(f' {min_temp}C-{max_temp}C')
        day_counter += 1   


def display_yearly_report(min_max_record):   
    max_temp_record = min_max_record['max_temp_record']  
    min_temp_record = min_max_record['min_temp_record']  
    max_humidity_record = min_max_record['max_humidity_record']  
   
    print(f'Highest: {max_temp_record.max_temperature}C on {max_temp_record.weather_record_date.strftime("%B %d")}')
    print(f'Lowest: {min_temp_record.min_temperature}C on {min_temp_record.weather_record_date.strftime("%B %d")}')
    print(f'Humidity: {max_humidity_record.max_humidity}% on {max_humidity_record.weather_record_date.strftime("%B %d")}')    


def display_monthly_report(average_values):          
    print(f'Highest Average: {average_values["avg_max_temperature"]}C')
    print(f'Lowest Average: {average_values["avg_min_temperature"]}C')
    print(f'Average Mean Humidity: {average_values["avg_mean_humidity"]}%')


def display_year_record_error():    
    print(error_messages.YEAR_DATA_NOT_FOUND_ERROR)


def display_month_record_error():
    print(error_messages.MONTH_DATA_NOT_FOUND_ERROR)
