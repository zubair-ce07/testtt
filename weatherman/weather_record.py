from datetime import datetime


class WeatherRecord:    
    def __init__(self, weather_record):          
        date = weather_record.get('PKT') or weather_record.get('PKST')             
        self.max_temperature = int(weather_record.get('Max TemperatureC'))
        self.min_temperature = int(weather_record.get('Min TemperatureC'))
        self.max_humidity = int(weather_record.get('Max Humidity'))
        self.mean_humidity = int(weather_record.get(' Mean Humidity'))
        self.weather_record_date = datetime.strptime(date, '%Y-%m-%d')            
