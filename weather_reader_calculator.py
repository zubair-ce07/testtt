from weather_reader_calculator_helper import *
class WeatherReaderCalculator:
	calculated_result = {}
	def compute_year_report(self,weather_reader_data):
		max_temp_dict = find_max(weather_reader_data,"Max TemperatureC")
		min_temp_dict = find_min(weather_reader_data,"Min TemperatureC")
		max_humid_dict = find_max(weather_reader_data,"Max Humidity")

		self.calculated_result["max_temp_dict"] = max_temp_dict
		self.calculated_result["min_temp_dict"] = min_temp_dict
		self.calculated_result["max_humid_dict"] = max_humid_dict

		return

	def compute_month_report(self,weather_reader_data):
		max_avg_temp_dict = find_max(weather_reader_data,"Mean TemperatureC")
		min_avg_temp_dict = find_min(weather_reader_data,"Mean TemperatureC")
		avg_humid_dict = calculate_avg(weather_reader_data,"Mean Humidity")

		self.calculated_result["max_avg_temp"] = max_avg_temp_dict
		self.calculated_result["min_avg_temp"] = min_avg_temp_dict
		self.calculated_result["avg_humidity"] = avg_humid_dict

		return

	def compute_barchart_report(self,weather_reader_data):
		i = 0
		while i < len(weather_reader_data)-1:
			try:
				self.calculated_result[i] = {"max": weather_reader_data[i]["Max TemperatureC"], 
											"min" : weather_reader_data[i]["Min TemperatureC"], 
											"day": weather_reader_data[i]["PKT"].split("-")[-1]}
			except:
				 self.calculated_result[i] = {"max": weather_reader_data[i]["Max TemperatureC"], 
											"min" : weather_reader_data[i]["Min TemperatureC"], 
											"day": weather_reader_data[i]["PKST"].split("-")[-1]}
			i += 1

		return

