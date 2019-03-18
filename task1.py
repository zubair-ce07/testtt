import sys
from sys import stdout
from operator import attrgetter

def print_bar(highest_temperature, lowest_temperature, day):
	"display data of temperature length on bar in one colour"
	stdout.write(str(day))
	stdout.write('- ')

	for temp in range(0, highest_temperature):
		stdout.write("\033[1;31;40m+")

	stdout.write(str(highest_temperature) + 'C')
	print(' ')
	stdout.write(str(day))
	stdout.write('- ')

	for temp in range(0, lowest_temperature):
		stdout.write("\033[1;34;40m+")

	stdout.write(str(lowest_temperature) + 'C')
	print(' ')

def print_bar_single_row(highest_temperature, lowest_temperature, day):
	"display data of temperature length on bar in two colours"
	stdout.write(str(day))
	stdout.write('- ')

	for temp in range(0, highest_temperature):
		if temp < lowest_temperature:
			stdout.write("\033[1;34;40m+")
		else:
			stdout.write("\033[1;31;40m+")

	stdout.write(str(lowest_temperature) + 'C - ' + str(highest_temperature) + 'C')
	print(' ')

class Weather:
	weather_date = ''
	maximum_temperature = 0
	minimum_temperature = 0
	maximum_humidity = 0
	def __init__(self, weather):
		weather_attributes_list = weather.split(',')
		self.weather_date = weather_attributes_list[0]
		if weather_attributes_list[1]:
			self.maximum_temperature = int(weather_attributes_list[1])
		if weather_attributes_list[3]:
			self.minimum_temperature = int(weather_attributes_list[3])
		if weather_attributes_list[7]:
			self.maximum_humidity = int(weather_attributes_list[7])
	

class WeatherCalculator:

	months = ['Jan', 'Feb' , 'Mar', 'Apr', 'May', 'Jun',
			'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
	]
	year = ''


	def maximum_minimum_temperature_of_year(self, year):
		"""Print maximum and minimum temperature of given year"""		
		self.year = year
		weather_list = []

		try:
			
			for month in self.months:
				path = './weatherfiles/Murree_weather_' +  self.year + '_' + month + '.txt'
				try:
					file_object = open(path)
					line = file_object.readline()
					line = file_object.readline()

					while line:

						weather_list.append(Weather(line))
						line = file_object.readline()
					file_object.close()		

				except:
					print('file ' + path  + ' does not exist')	
	
			weather_maximum = max(weather_list, key=attrgetter('maximum_temperature'))
			weather_minimum = min(weather_list, key=attrgetter('minimum_temperature'))
			weather_humidity = max(weather_list, key=attrgetter('maximum_humidity'))
			print('Highest ' + str(weather_maximum.maximum_temperature) + 'C on '+ weather_maximum.weather_date)
			print('Lowest ' + str(weather_minimum.minimum_temperature) + 'C on '+ weather_minimum.weather_date)
			print('Humidity ' + str(weather_humidity.maximum_humidity) + ' on ' + weather_humidity.weather_date)

		except:

			print('file ' + path  + ' does not exist')	

	def maximum_minimum_average_temperature_of_month(self, year, month):
		"""Print maximum, minimum, average temperature of given month"""		
		self.year = year
		weather_list = []

		try:
			
			path = './weatherfiles/Murree_weather_' +  self.year + '_' + self.months[month] + '.txt'
			try:
				file_object = open(path)
				line = file_object.readline()
				line = file_object.readline()

				while line:

					weather_list.append(Weather(line))
					line = file_object.readline()

				file_object.close()		
			except:
				print('file ' + path  + ' does not exist')	

			sum_maximum_temperature = sum(i.maximum_temperature for i in weather_list)
			sum_minimum_temperature = sum(i.minimum_temperature for i in weather_list)
			sum_maximum_humidity = sum(i.maximum_humidity for i in weather_list)
			print('Highest Average ' + str(sum_maximum_temperature/len(weather_list)))
			print('Lowest Average ' + str(sum_minimum_temperature/len(weather_list)))
			print('Average Humidity ' + str(sum_maximum_humidity/len(weather_list)))
			
		except:
			print('file ' + path  + ' does not exist')	
		
	def daily_report_of_month(self, year, month, option):
		"""Print the highest lowest of each day in bar"""		
		self.year = year
		weather_list = []

		try:
			counter = 1
			path = './weatherfiles/Murree_weather_' +  self.year + '_' + self.months[month] + '.txt'
			
			file_object = open(path)
			line = file_object.readline()
			line = file_object.readline()

			while line: 

				weather_list.append(Weather(line))
				line = file_object.readline()
			file_object.close()

			for day in weather_list:
				if option == 3:
					print_bar(day.maximum_temperature , day.minimum_temperature , counter)
				elif option == 4:
					print_bar_single_row(day.maximum_temperature , day.minimum_temperature, counter)
				counter = counter + 1

		except:
			print('file ' + path  + ' does not exist')	

weather_calculator = WeatherCalculator()

if int(sys.argv[1]) == 1:
	weather_calculator.maximum_minimum_temperature_of_year(sys.argv[2])

elif int(sys.argv[1]) == 2:
	weather_calculator.maximum_minimum_average_temperature_of_month(sys.argv[2], int(sys.argv[3]))

elif int(sys.argv[1]) == 3:
	weather_calculator.daily_report_of_month(sys.argv[2], int(sys.argv[3]), int(sys.argv[1]))

elif int(sys.argv[1]) == 4:
	weather_calculator.daily_report_of_month(sys.argv[2], int(sys.argv[3]), int(sys.argv[1]))
