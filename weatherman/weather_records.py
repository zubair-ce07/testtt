import datetime

class WeatherRecord:

    def __init__(self, record):   
        date = record.get("PKT") or record.get("PKST")
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        self.max_temp = int(record.get("Max TemperatureC"))
        self.min_temp = int(record.get("Min TemperatureC"))
        self.max_humidity = int(record.get("Max Humidity"))
        self.mean_humidity = int(record.get(" Mean Humidity"))
        
