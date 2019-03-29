import sys
import os
import argparse
from sys import stdout
from operator import attrgetter

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
	
class WeatherReporter:


	months = ['Jan', 'Feb' , 'Mar', 'Apr', 'May', 'Jun',
			'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
	]

	def __init__(self, path):
		self.year = ''
		self.month = ''
		self.data_list = []
		self.weather_list_year = []
		self.weather_list_month = []
		for root, dirs, files in os.walk(path):  
			for filename in files:
				if '.txt' in filename:
					file_object = open(path + filename)
					line = file_object.readline()
					line = file_object.readline()
					attributes_list = line.split(',')
					while line:
						self.data_list.append(Weather(attributes_list[0],attributes_list[1],
									attributes_list[3], attributes_list[7]))
						line = file_object.readline()
						attributes_list = line.split(',')
					file_object.close()

	def populate_year_list(self):				
		self.weather_list_year = []
		for weather in self.data_list:
			if self.year in weather.weather_date:
				self.weather_list_year.append(weather)

	def populate_month_list(self):				
		self.weather_list_month = []
		for weather in self.data_list:
			if (self.year + '-' + str(self.month)) in weather.weather_date:
				self.weather_list_month.append(weather)			

	def print_bar(self, max_temperature, min_temperature, day):
		"display data of temperature length on bar in one colour"
		red_line_bar = str(day) + '- ' + '+' * max_temperature + str(max_temperature) + 'C'
		stdout.write("\033[1;31;40m" + red_line_bar + '\n' )
		blue_line_bar = str(day) + '- ' + '+' * min_temperature + str(min_temperature) + 'C'
		stdout.write("\033[1;34;40m" + blue_line_bar + '\n')

	def print_bar_single_row(self, max_temperature, min_temperature, day):
		"display data of temperature length on bar in two colours"
		partial_blue_bar = str(day) + '- ' + '+' * min_temperature 
		stdout.write("\033[1;34;40m" + partial_blue_bar)
		max_min_difference = max_temperature - min_temperature 
		max_min_range = str(min_temperature) + 'C - ' + str(max_temperature) + 'C'
		partial_red_bar = '+' * max_min_difference + max_min_range
		stdout.write("\033[1;31;40m" + partial_red_bar + '\n')

	def calculate_max_temperature(self, year):
		"""maximum minimum temperature of given year"""		
		self.year = year
		self.populate_year_list()
		max_weather = max(self.weather_list_year, key=attrgetter('max_temperature'))
		return max_weather.max_temperature, max_weather.weather_date

	def calculate_min_temperature(self):
		"""minimum temperature of given year"""		
		min_weather = min(self.weather_list_year, key=attrgetter('min_temperature'))
		return min_weather.min_temperature, min_weather.weather_date	

	def calculate_max_humidity(self):
		"""maximum humidity of given year"""		
		max_humidity = max(self.weather_list_year, key=attrgetter('max_humidity'))
		return max_humidity.max_humidity, max_humidity.weather_date

	def calculate_average_max_temperature(self, year, month):
		"""maximum average temperature of given month"""	
		self.year = year
		self.month = month
		self.populate_month_list()		
		avg_max = sum(i.max_temperature for i in self.weather_list_month)/len(self.weather_list_month)
		return avg_max

	def calculate_average_min_temperature(self):
		"""m average temperature of given month"""
		avg_min = sum(i.min_temperature for i in self.weather_list_month)/len(self.weather_list_month)
		return avg_min

	def calculate_average_max_humidity(self):
		"""maximum average humidity of given month"""	
		avg_humidity = sum(i.max_humidity for i in self.weather_list_month)/len(self.weather_list_month)
		return avg_humidity

	def calculate_daily_report(self, year, month, option):
		"""Print the highest lowest of each day in bar"""		
		self.year = year
		self.month = month
		self.populate_month_list()
		counter = 1
		for day in self.weather_list_month:
			if option == 3:
				self.print_bar(day.max_temperature, day.min_temperature, counter)
			elif option == 4:
				self.print_bar_single_row(day.max_temperature, day.min_temperature, counter)
			counter = counter + 1

def main():
	""" main function """
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-a", "--year_data", action="store_true")
	group.add_argument("-b", "--month_data", action="store_true")
	group.add_argument("-c", "--month_split_bar", action="store_true")
	group.add_argument("-d", "--month_bar", action="store_true")	
	parser.add_argument("year", help="enter year")
	parser.add_argument("month", help="enter month")
	parser.add_argument("path", help="enter path")
	args = parser.parse_args()

	weather = WeatherReporter(sys.argv[4])

	if args.year_data:
		max_temp, date = weather.calculate_max_temperature(args.year)
		print(max_temp, date)
		min_temp, date = weather.calculate_min_temperature()
		print(min_temp, date)	
		max_humidity, date = weather.calculate_max_humidity()
		print(max_humidity, date)	

	elif args.month_data:
		avg_max = weather.calculate_average_max_temperature(args.year, int(args.month))
		print(avg_max)
		avg_min = weather.calculate_average_min_temperature()
		print(avg_min)
		avg_humdity = weather.calculate_average_max_humidity()
		print(avg_humdity)

	elif args.month_split_bar:
		weather.calculate_daily_report(args.year, int(args.month), 3)

	elif args.month_bar:
		weather.calculate_daily_report(args.year, int(args.month), 4)

if __name__ == "__main__":
	main()
