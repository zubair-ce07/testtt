class Weather:

	def __init__(self, attribute_date, attribute_max, attribute_min, attribute_humidity):
		self.weather_date = attribute_date
		
		if attribute_max:
			self.max_temperature = int(attribute_max)
		else :
			self.max_temperature = 0
		if attribute_min:
			self.min_temperature = int(attribute_min)
		else : 
			self.min_temperature = 0
		if attribute_humidity:
			self.max_humidity = int(attribute_humidity)
		else :
			self.max_humidity = 0
