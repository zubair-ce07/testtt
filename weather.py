class Weather:

	def __init__(self, attribute_date, attribute_max, attribute_min, attribute_humidity):
		self.weather_date = attribute_date
		
		self.max_temperature = int(attribute_max) if attribute_max else 0	
		self.min_temperature = int(attribute_min) if attribute_min else 0		
		self.max_humidity = int(attribute_humidity) if attribute_humidity else 0
		