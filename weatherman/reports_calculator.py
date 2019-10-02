from reports_generator import display_year_record_error, display_month_record_error


def calculate_yearly_report(weather_data, year):
    weather_records = []
    year = year.strftime('%Y') 

    for yearly_weather_record in weather_data:        
        if year in yearly_weather_record.weather_record_date.strftime('%Y'):
            weather_records.append(yearly_weather_record)
    
    if weather_records:                   
        return {
            'max_temp_record': max(weather_records, key=lambda record: record.max_temperature),
            'max_humidity_record': max(weather_records, key=lambda record: record.max_humidity),
            'min_temp_record': min(weather_records, key=lambda record: record.min_temperature)
        }
    else:
        display_year_record_error()    


def calculate_monthly_report(weather_data, date):
    monthly_weather_data = []
    month_year = date.strftime('%Y-%m')

    for monthly_weather_record in weather_data:
        if month_year in monthly_weather_record.weather_record_date.strftime('%Y-%m'):
            monthly_weather_data.append(monthly_weather_record)

    if monthly_weather_data:
        max_temperature_values = [record.max_temperature for record in monthly_weather_data]
        min_temperature_values = [record.min_temperature for record in monthly_weather_data]
        mean_humidity_values = [record.mean_humidity for record in monthly_weather_data]

        average_max_temp = sum(max_temperature_values) // len(max_temperature_values)
        average_min_temp = sum(min_temperature_values) // len(min_temperature_values)
        average_mean_humidity = sum(mean_humidity_values) // len(mean_humidity_values)
       
        return {
            'avg_max_temperature': average_max_temp,
            'avg_min_temperature': average_min_temp,
            'avg_mean_humidity': average_mean_humidity
        }
    else:
        display_month_record_error()


def calculate_monthly_chart_values(weather_data, date):
    monthly_weather_data = []
    month_year = date.strftime('%Y-%m')

    for monthly_weather_record in weather_data:
        if month_year in monthly_weather_record.weather_record_date.strftime('%Y-%m'):
            monthly_weather_data.append(monthly_weather_record)

    if monthly_weather_data:        
        return {
            'max_temperatures': [record.max_temperature for record in monthly_weather_data],
            'min_temperatures': [record.min_temperature for record in monthly_weather_data]
        }
    else:
        display_month_record_error()    
