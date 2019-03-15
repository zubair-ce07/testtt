import sys
from sys import stdout
from operator import attrgetter

class Weather :
	
	weather_date = ''
	maximum_temperature =0
	minimum_temperature = 0
	maximum_humidity = 0
	
	def __init__(self, weather):  
		weather_attributes_list = weather.split(',')
		self.weather_date = weather_attributes_list[0]
		if weather_attributes_list[1] :
			self.maximum_temperature = int(weather_attributes_list[1])
		if weather_attributes_list[3] :
			self.minimum_temperature = int(weather_attributes_list[3])
		if weather_attributes_list[7] : 
			self.maximum_humidity = int(weather_attributes_list[7]) 
	

class WeatherCalculator :

	months = [
		'Jan', 'Feb' , 'Mar', 'Apr', 'May', 'Jun', 
		'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
	]
	year = ''


	def print_bar(self, highest_temperature , lowest_temperature, day):
		stdout.write(str(day))
		stdout.write('- ')

		for i in range(0, highest_temperature):	
			stdout.write("\033[1;31;40m+")

		stdout.write(str(highest_temperature) + 'C' )
		print(' ')
		stdout.write(str(day))
		stdout.write('- ')

		for x in range(0, lowest_temperature):	
			stdout.write("\033[1;34;40m+")	

		stdout.write(str(lowest_temperature) + 'C' )
		print(' ')	

	def print_bar_single_row(self, highest_temperature , lowest_temperature, day):
		stdout.write(str(day))
		stdout.write('- ')

		for x in range(0, highest_temperature):
			if x < lowest_temperature :	
				stdout.write("\033[1;34;40m+")
			else :
				stdout.write("\033[1;31;40m+")

		stdout.write(str(lowest_temperature) + 'C - ' + str(highest_temperature) + 'C' )
		print(' ')

	def maximum_minimum_temperature_of_year(self, year) :
		
		self.year = year
		weatherList = []

		try :
			
			for month in self.months :
				path = './weatherfiles/Murree_weather_' +  self.year + '_' + month + '.txt'
				try :
					f = open(path)
					line = f.readline()
					line = f.readline()

					while line :

						weatherList.append(Weather(line))
						line = f.readline()

					f.close()		
				except :
					print('file ' + path  + ' does not exist')	
	
			weather_maximum = max(weatherList, key=attrgetter('maximum_temperature'))
			weather_minimum = min(weatherList, key=attrgetter('minimum_temperature'))
			weather_humidity = max(weatherList, key=attrgetter('maximum_humidity'))
			print('Highest ' + str(weather_maximum.maximum_temperature) + 'C on '+ weather_maximum.weather_date)
			print('Lowest ' + str(weather_minimum.minimum_temperature) + 'C on '+ weather_minimum.weather_date)
			print('Humidity ' + str(weather_humidity.maximum_humidity) + ' on ' + weather_humidity.weather_date)

		except :

			print('file ' + path  + ' does not exist')	

	def maximum_minimum_average_temperature_of_month(self, year, month) :
		
		self.year = year
		weatherList = []

		try :
			
			path = './weatherfiles/Murree_weather_' +  self.year + '_' + self.months[month] + '.txt'
			try :
				f = open(path)
				line = f.readline()
				line = f.readline()

				while line :

					weatherList.append(Weather(line))
					line = f.readline()

				f.close()		
			except :
				print('file ' + path  + ' does not exist')	

			sum_maximum_temperature = sum(i.maximum_temperature for i in weatherList)
			sum_minimum_temperature = sum(i.minimum_temperature for i in weatherList)
			sum_maximum_humidity = sum(i.maximum_humidity for i in weatherList)
			print('Highest Average ' + str(sum_maximum_temperature/len(weatherList)))
			print('Lowest Average ' + str(sum_minimum_temperature/len(weatherList)))
			print('Average Humidity ' + str(sum_maximum_humidity/len(weatherList)))
			
		except :
			print('file ' + path  + ' does not exist')	
		
	def daily_report_of_month(self, year, month, option) :
		
		self.year = year
		weatherList = []

		try :
			counter = 1
			path = './weatherfiles/Murree_weather_' +  self.year + '_' + self.months[month] + '.txt'
			
			f = open(path)
			line = f.readline()
			line = f.readline()

			while line :

				weatherList.append(Weather(line))
				line = f.readline()
			f.close()

			for day in weatherList :
				if option == 3  :
					self.print_bar(day.maximum_temperature , day.minimum_temperature , counter)
				elif option == 4 :
					self.print_bar_single_row(day.maximum_temperature , day.minimum_temperature, counter)
				counter = counter + 1

		except :
			print('file ' + path  + ' does not exist')	

calculator = WeatherCalculator()

if int(sys.argv[1]) == 1 :
	calculator.maximum_minimum_temperature_of_year(sys.argv[2])

elif int(sys.argv[1]) == 2 :
	calculator.maximum_minimum_average_temperature_of_month(sys.argv[2], int(sys.argv[3]))

elif int(sys.argv[1]) == 3 :
	calculator.daily_report_of_month(sys.argv[2], int(sys.argv[3]), int(sys.argv[1]))

elif int(sys.argv[1]) == 4 :
	calculator.daily_report_of_month(sys.argv[2], int(sys.argv[3]), int(sys.argv[1]))
