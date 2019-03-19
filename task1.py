import sys
from sys import stdout
from operator import attrgetter

def read_file(year, month):
	""" open file """
	path = './weatherfiles/Murree_weather_' + year + '_' + month + '.txt'
	try:
		file_object = open(path)
		weather_list = []
		if file_object:
			line = file_object.readline()
			line = file_object.readline()

			while line:
				weather_list.append(Weather(line))
				line = file_object.readline()

			file_object.close()
		return weather_list
	except IOError:
		print('file ' + path  + ' does not exist')
	
def print_bar(max_temperature, min_temperature, day):
	"display data of temperature length on bar in one colour"
	red_line_bar = str(day) + '- ' + '+' * max_temperature + str(max_temperature) + 'C'
	stdout.write("\033[1;31;40m" + red_line_bar + '\n' )
	blue_line_bar = str(day) + '- ' + '+' * min_temperature + str(min_temperature) + 'C'
	stdout.write("\033[1;34;40m" + blue_line_bar + '\n')

def print_bar_single_row(max_temperature, min_temperature, day):
	"display data of temperature length on bar in two colours"
	partial_blue_bar = str(day) + '- ' + '+' * min_temperature 
	stdout.write("\033[1;34;40m" + partial_blue_bar)
	max_min_difference = max_temperature - min_temperature 
	max_min_range = str(min_temperature) + 'C - ' + str(max_temperature) + 'C'
	partial_red_bar = '+' * max_min_difference + max_min_range
	stdout.write("\033[1;31;40m" + partial_red_bar + '\n')

class Weather:
	weather_date = ''
	max_temperature = 0
	min_temperature = 0
	max_humidity = 0
	def __init__(self, weather):
		weather_attributes_list = weather.split(',')
		self.weather_date = weather_attributes_list[0]
		if weather_attributes_list[1]:
			self.max_temperature = int(weather_attributes_list[1])
		if weather_attributes_list[3]:
			self.min_temperature = int(weather_attributes_list[3])
		if weather_attributes_list[7]:
			self.max_humidity = int(weather_attributes_list[7])
	
class Calculator:

	months = ['Jan', 'Feb' , 'Mar', 'Apr', 'May', 'Jun',
			'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
	]
	year = ''

	def calculate_max_temperature(self, year):
		"""maximum minimum temperature of given year"""		
		self.year = year
		weather_list_month = []
		weather_list_year = []

		for month in self.months:
			weather_list_month	= read_file(self.year, month)	
			if weather_list_month :	
				weather_list_year = weather_list_year + weather_list_month  
		max_weather = max(weather_list_year, key=attrgetter('max_temperature'))
		return max_weather.max_temperature, max_weather.weather_date

	def calculate_min_temperature(self, year):
		"""minimum temperature of given year"""		
		self.year = year
		weather_list_month = []
		weather_list_year = []

		for month in self.months:
			weather_list_month	= read_file(self.year, month)	
			if weather_list_month :	
				weather_list_year = weather_list_year + weather_list_month  
		min_weather = min(weather_list_year, key=attrgetter('min_temperature'))
		return min_weather.min_temperature, min_weather.weather_date	

	def calculate_max_humidity(self, year):
		"""maximum humidity of given year"""		
		self.year = year
		weather_list_month = []
		weather_list_year = []

		for month in self.months:
			weather_list_month	= read_file(self.year, month)	
			if weather_list_month :	
				weather_list_year = weather_list_year + weather_list_month  
		max_humidity = max(weather_list_year, key=attrgetter('max_humidity'))
		return max_humidity.max_humidity, max_humidity.weather_date

	def calculate_average_max_temperature(self, year, month):
		"""maximum average temperature of given month"""	
		self.year = year
		weather_list = []
		weather_list = read_file(self.year, self.months[month])
		avg_max = sum(i.max_temperature for i in weather_list)/len(weather_list)
		return avg_max

	def calculate_average_min_temperature(self, year, month):
		"""m average temperature of given month"""	
		self.year = year
		weather_list = []
		weather_list = read_file(self.year, self.months[month])
		avg_min = sum(i.min_temperature for i in weather_list)/len(weather_list)
		return avg_min

	def calculate_average_max_humidity(self, year, month):
		"""maximum average humidity of given month"""	
		self.year = year
		weather_list = []
		weather_list = read_file(self.year, self.months[month])
		avg_humidity = sum(i.max_humidity for i in weather_list)/len(weather_list)
		return avg_humidity

	def calculate_daily_report(self, year, month, option):
		"""Print the highest lowest of each day in bar"""		
		self.year = year
		weather_list = []
		weather_list = read_file(self.year, self.months[month])
		counter = 1
		for day in weather_list:
			if option == 3:
				print_bar(day.max_temperature, day.min_temperature, counter)
			elif option == 4:
				print_bar_single_row(day.max_temperature, day.min_temperature, counter)
			counter = counter + 1

def main():
	""" main function """
	weather = Calculator()

	if int(sys.argv[1]) == 1:
		max_temp, date = weather.calculate_max_temperature(sys.argv[2])
		print(max_temp, date)
		min_temp, date = weather.calculate_min_temperature('2004')
		print(min_temp, date)	
		max_humidity, date = weather.calculate_max_humidity('2004')
		print(max_humidity, date)	

	elif int(sys.argv[1]) == 2:
		avg_max = weather.calculate_average_max_temperature(sys.argv[2], int(sys.argv[3]))
		print(avg_max)
		avg_min = weather.calculate_average_min_temperature(sys.argv[2], int(sys.argv[3]))
		print(avg_min)
		avg_humdity = weather.calculate_average_max_humidity(sys.argv[2], int(sys.argv[3]))
		print(avg_humdity)

	elif int(sys.argv[1]) == 3:
		weather.calculate_daily_report(sys.argv[2], int(sys.argv[3]), int(sys.argv[1]))

	elif int(sys.argv[1]) == 4:
		weather.calculate_daily_report(sys.argv[2], int(sys.argv[3]), int(sys.argv[1]))
if __name__ == "__main__":
	main()
