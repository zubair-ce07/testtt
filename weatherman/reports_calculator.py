def calculate_min_max(weather_yearly_data):    
        max_temp = weather_yearly_data[0].max_temperature
        min_temp = weather_yearly_data[0].min_temperature
        max_humidity = weather_yearly_data[0].max_humidity

        for weather_record in weather_yearly_data:
            if weather_record.max_temperature > max_temp:
                max_temperature_record = weather_record

            if weather_record.min_temperature < min_temp:
                min_temperature_record = weather_record

            if weather_record.max_humidity > max_humidity:
                max_humidity_record = weather_record         

        min_max_yearly_record = {
            'max_temp_record': max_temperature_record,
            'max_humidity_record': max_humidity_record,
            'min_temp_record': min_temperature_record, 
        }
        
        return min_max_yearly_record


def filter_values(weather_data):
    validated_values = [value for value in weather_data if value != '']

    return validated_values


def calculate_averages(weather_data):
    max_temp_validated = filter_values([record.max_temperature for record in weather_data])
    min_temp_validated = filter_values([record.min_temperature for record in weather_data])
    mean_humidity_validated = filter_values([record.mean_humidity for record in weather_data])

    average_max_temp = sum(max_temp_validated) // len(max_temp_validated)
    average_min_temp = sum(min_temp_validated) // len(min_temp_validated)
    average_mean_humidity = sum(mean_humidity_validated) // len(mean_humidity_validated)

    average_weather_record = {
        'avg_max_temperature': average_max_temp,
        'avg_min_temperature': average_min_temp,
        'avg_mean_humidity': average_mean_humidity
    }
   
    return average_weather_record


def calculate_monthly_chart_values(weather_data):
    max_temp = [record.max_temperature for record in weather_data]
    min_temp = [record.min_temperature for record in weather_data]

    return {
        'max_temp': max_temp,
        'min_temp': min_temp
    }
