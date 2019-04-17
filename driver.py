import sys
import os
import argparse
from sys import stdout
from operator import attrgetter
from weather import Weather

class WeatherReporter:

	months = ['Jan', 'Feb' , 'Mar', 'Apr', 'May', 'Jun',
			'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
	]

	def __init__(self, path):
		self.year = ''
		self.month = ''
		self.data_list = []
		for root, dirs, files in os.walk(path):  
			for filename in files:
				if '.txt' in filename:
					self.read_file(path + filename)		

	def read_file(self, path_to_file):
		file_object = open(path_to_file)
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
		weather_list_year = []
		for weather in self.data_list:
			if self.year in weather.weather_date:
				weather_list_year.append(weather)
		return weather_list_year		

	def populate_month_list(self):				
		weather_list_month = []
		for weather in self.data_list:
			if (self.year + '-' + str(self.month)) in weather.weather_date:
				weather_list_month.append(weather)			
		return weather_list_month

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
		max_weather = max(self.populate_year_list(), key=attrgetter('max_temperature'))	
		return max_weather.max_temperature, max_weather.weather_date

	def calculate_min_temperature(self):
		"""minimum temperature of given year"""		
		min_weather = min(self.populate_year_list(), key=attrgetter('min_temperature'))
		return min_weather.min_temperature, min_weather.weather_date	

	def calculate_max_humidity(self):
		"""maximum humidity of given year"""		
		max_humidity = max(self.populate_year_list(), key=attrgetter('max_humidity'))
		return max_humidity.max_humidity, max_humidity.weather_date

	def calculate_average_max_temperature(self, year, month):
		"""maximum average temperature of given month"""	
		self.year = year
		self.month = month
		self.populate_month_list()		
		avg_max = sum(i.max_temperature for i in self.populate_month_list())/len(self.populate_month_list())
		return avg_max

	def calculate_average_min_temperature(self):
		"""m average temperature of given month"""
		avg_min = sum(i.min_temperature for i in self.populate_month_list())/len(self.populate_month_list())
		return avg_min

	def calculate_average_max_humidity(self):
		"""maximum average humidity of given month"""	
		avg_humidity = sum(i.max_humidity for i in self.populate_month_list())/len(self.populate_month_list())
		return avg_humidity

	def calculate_daily_report(self, year, month, option):
		"""Print the highest lowest of each day in bar"""		
		self.year = year
		self.month = month
		self.populate_month_list()
		counter = 1
		for day in self.populate_month_list():
			if option == 3:
				self.print_bar(day.max_temperature, day.min_temperature, counter)
			elif option == 4:
				self.print_bar_single_row(day.max_temperature, day.min_temperature, counter)
			counter = counter + 1

