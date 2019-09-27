from datetime import datetime


def display_month_bar_chart(weather_data):
    max_temp_values = weather_data['max_temperature']
    min_temp_values = weather_data['min_temperature']
    date_values = weather_data['weather_record_date']

    print('\n ************************************************************* \n')
    for (max_temp, min_temp, max_day) in zip(max_temp_values, min_temp_values, date_values):
        max_day = max_day.split('-')[2]            
        print(max_day + ' ', end='')
        print("\033[1;34m+\033[1;m" * min_temp, end='')
        print("\033[1;31m+\033[1;m" * max_temp, end='')
        print(f' {min_temp}C-{max_temp}C')
    print('\n ************************************************************* \n')
        

def display_yearly_report(min_max_values):       
    max_temp_day = datetime.strptime(min_max_values['max_temp_date'], '%Y-%m-%d')
    max_temp_day_formatted = max_temp_day.strftime('%B %d')
    min_temp_day = datetime.strptime(min_max_values['min_temp_date'], '%Y-%m-%d')
    min_temp_day_formatted = min_temp_day.strftime('%B %d')
    max_humid_day = datetime.strptime(min_max_values['max_humidity_date'], '%Y-%m-%d')
    max_humid_day_formatted = max_humid_day.strftime('%B %d')

    print('\n ************************************************************* \n')
    print(f'Highest: {min_max_values["max_temperature"]}C on {max_temp_day_formatted}')
    print(f'Lowest: {min_max_values["min_temperature"]}C on {min_temp_day_formatted}')
    print(f'Humidity: {min_max_values["max_humidity"]}% on {max_humid_day_formatted}')
    print('\n ************************************************************* \n')


def display_averages(avg_values):        
    print('\n ************************************************************* \n')
    print(f'Highest Average: {avg_values["avg_max_temperature"]}C')
    print(f'Lowest Average: {avg_values["avg_min_temperature"]}C')
    print(f'Average Mean Humidity: {avg_values["avg_mean_humidity"]}%')
    print('\n ************************************************************* \n')
