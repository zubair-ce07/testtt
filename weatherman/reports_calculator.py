def find_yearly_record(weather_data, date):    
    weather_records = []    

    for yearly_weather_record in weather_data:        
        if date.year == yearly_weather_record.weather_record_date.year:            
            weather_records.append(yearly_weather_record)

    return weather_records        


def find_monthly_records(weather_data, date):
    monthly_weather_records = []
        
    for monthly_weather_record in weather_data:
        if date.year == monthly_weather_record.weather_record_date.year and date.month == monthly_weather_record.weather_record_date.month:
            monthly_weather_records.append(monthly_weather_record)

    return monthly_weather_records        


def calculate_yearly_report(weather_data, date):    
    weather_records = find_yearly_record(weather_data, date)            

    if weather_records:                   
        return {
            'max_temp_record': max(weather_records, key=lambda record: record.max_temperature),
            'max_humidity_record': max(weather_records, key=lambda record: record.max_humidity),
            'min_temp_record': min(weather_records, key=lambda record: record.min_temperature)
        }
    

def calculate_average_values(weather_records):
    return sum(weather_records)//len(weather_records)  


def calculate_monthly_report(weather_data, date):        
    monthly_weather_records = find_monthly_records(weather_data, date)

    if monthly_weather_records:      
        return {
            'avg_max_temperature': calculate_average_values([record.max_temperature for record in monthly_weather_records]),
            'avg_min_temperature': calculate_average_values([record.min_temperature for record in monthly_weather_records]),
            'avg_mean_humidity': calculate_average_values([record.mean_humidity for record in monthly_weather_records])
        }
   

def calculate_monthly_chart_values(weather_data, date):       
    monthly_weather_records = find_monthly_records(weather_data, date)

    if monthly_weather_records:        
        return {
            'max_temperatures': [record.max_temperature for record in monthly_weather_records],
            'min_temperatures': [record.min_temperature for record in monthly_weather_records],
            'weather_record_date': [record.weather_record_date for record in monthly_weather_records]
        }
