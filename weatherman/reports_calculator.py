def calculate_yearly_report(weather_yearly_data):                           
    max_temperature = max([weather_record.max_temperature for weather_record in weather_yearly_data])
    min_temperature = min([weather_record.min_temperature for weather_record in weather_yearly_data])
    max_humidity = max([weather_record.max_humidity for weather_record in weather_yearly_data])

    for weather_record in weather_yearly_data:
        if weather_record.max_temperature == max_temperature:            
            max_temperature_record = weather_record

        if weather_record.min_temperature == min_temperature:
            min_temperature_record = weather_record

        if weather_record.max_humidity == max_humidity:
            max_humidity_record = weather_record         

    min_max_yearly_record = {
        'max_temp_record': max_temperature_record,
        'max_humidity_record': max_humidity_record,
        'min_temp_record': min_temperature_record, 
    }
    
    return min_max_yearly_record


def calculate_monthly_report(monthly_weather_data):                
    max_temperature_values = [record.max_temperature for record in monthly_weather_data]
    min_temperature_values = [record.min_temperature for record in monthly_weather_data]
    mean_humidity_values = [record.mean_humidity for record in monthly_weather_data]

    average_max_temp = sum(max_temperature_values) // len(max_temperature_values)
    average_min_temp = sum(min_temperature_values) // len(min_temperature_values)
    average_mean_humidity = sum(mean_humidity_values) // len(mean_humidity_values)

    average_weather_record = {
        'avg_max_temperature': average_max_temp,
        'avg_min_temperature': average_min_temp,
        'avg_mean_humidity': average_mean_humidity
    }
   
    return average_weather_record


def calculate_monthly_chart_values(monthly_weather_data):
    max_temperatures = [record.max_temperature for record in monthly_weather_data]
    min_temperatures = [record.min_temperature for record in monthly_weather_data]

    return {
        'max_temperatures': max_temperatures,
        'min_temperatures': min_temperatures
    }
