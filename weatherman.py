import os
import sys
import curses
import colorama
from colorama import Fore, Back, Style
from statistics import mean

colorama.init()

file_columns = {
		"PKT":0,
		"Max_TemperatureC":1,
		"Mean_TemperatureC":2,
		"Min_TemperatureC":3,
		"Dew PointC":4,
		"MeanDew PointC":5,
		"Min DewpointC":6,
		"Max_Humidity":7, 
		"Mean_Humidity":8, 
		"Min_Humidity":9
	}

temp_stats = {
		"max_temp" : 0, # assuming no max temp would be less than this
		"min_temp" : 1000, # assuming no min temp would be greater than this
		"mean_max_temp":0,
		"mean_min_temp":0,
		
		"max_temp_date":None,
		#"max_temp_day":None,
		#"max_temp_month":None,
		#"max_temp_year":None,

		"min_temp_date":None,
		#"min_temp_day":None,
		#"min_temp_month":None,
		#"min_temp_year":None,
	}

humidity_stats = {

		"max_humidity":0,
		"min_humidity":1000,
		
		"max_humidity_date":None,
		#"max_humidity_day":None,
		#"min_humidity_month":None,
		#"max_humidity_year":None,
		"max_humidity":0.0,
		
		"min_humidity_date":None,
		#"min_humidity_day":None,
		#"min_humidity_month":None,
		#"min_humidity_year":None,
		"min_humidity":0.0,

		"mean_humidity":0.0
	}

def prettify_date(date):

	""" 
	Make the date more human friendly
	
	Inputs: 
		date: Date given in format 2003-3-03
	Output: 
		Returns a human friendly string format eg "March 03"
	"""
	
	date = date.split("-")
	m = get_month_string(int(date[1]))
	d = date[2]

	return '{0} {1}'.format(m, d)

def get_month_string(m):

	""" 
	Compute a string representation of a numeric month
	
	Inputs: 
		m: month given in number
	Output: 
		returns its corresponding string representation
	"""

	months = ['','January','February','March','April','May','June','July','August','September','October','November','December']
	if(m >= 0 and m <= 12):
		return months[m]

def print_stats():

	""" 
	Prints humidity,highest and lowest temperature for 
	a year
	
	Inputs: 
		None
	Output: 
		Prints temperature and humidity stats in a format
	"""
	
	print("-----------------Final Result--------------------------")
	print("Highest:", temp_stats["max_temp"],"C on", prettify_date(temp_stats["max_temp_date"]))
	print("Lowest:", temp_stats["min_temp"],"C on", prettify_date(temp_stats["min_temp_date"]))
	print("Humidity:", humidity_stats["max_humidity"],"% on", prettify_date(humidity_stats["max_humidity_date"]))
	print("-------------------------------------------------------")

def print_stats_avg_month():

	""" 
	Prints average humidity,highest and lowest temperature for
	a month
	
	Inputs: 
		None
	Output: 
		Prints temperature and humidity stats in a format
	"""

	print("-----------------Final Result--------------------------")
	print("Highest Average:", temp_stats["mean_max_temp"],"C")
	print("Lowest Average:", temp_stats["mean_min_temp"],"C")
	print("Average Mean Humidity:", humidity_stats["mean_humidity"])
	print("-------------------------------------------------------")

def get_month_and_year(date):
	return (date.split("/")[1], date.split("/")[0])

def create_filename_string(date):

	""" 
	Input date format is converted into weatherdata specific filname
	format. 
	
	Inputs: 
		date: Date specified in format 2006/3
	Output: 
		Return format is weatherdata compliant "Murree_weather_2006_Mar.txt"
	"""

	year = date.split("/")[0]
	month = date.split("/")[1]

	file_name = "Murree_weather_" + year + "_" + get_month_string(int(month))[:3] + ".txt"
	return file_name

def print_histogram(highest_temp_list, lowest_temp_list, month, year):
	
	""" Creates a histogram for a specified month in different colors 

	Inputs:
		highest_temp_list: List of highest temperatures for a month
		lowest_temp_list: List of lowest temperatures for a month
		year: for this year eg 2010
	Output:
		Prints a histogram.
	"""

	print(get_month_string(int(month)) +" "+ year)
	
	for day, temp in enumerate(zip(highest_temp_list, lowest_temp_list)):
		print(Fore.RED)
		print(str(day + 1) + " ", end="")
		print("+" * temp[0] + " " + str(temp[0]) + "C" , end="") 

		print(Fore.BLUE)
		print(str(day + 1) + " ", end="")
		print("+" * temp[1] + " " + str(temp[1]) + "C" , end="") 
	print("")

def process_file_for_minmax_stats(file_name):

	"""	
	Process a weather data file for max and min for temperature 
	and humidity 

	Inputs:
		file_name: filename of the weather date file to process
	Output:
		Nothing is returned, uses other helper functions to incrementally
		find min and max stats
	"""
	
	try:
		with open(file_name) as open_file:
			data_set = []
			for line in open_file:
				data_set.append(line)
			compute_incrementally_stats_minmax_month(data_set, temp_stats, humidity_stats, file_name)
	except IOError as e:
		print("No files found with this year")

def compute_incrementally_stats_minmax_month(data_set, temp_stats, humidity_stats, file_name):

	"""
	Computes stats of max temp, min temp and min humidity for a month 
	identified by file name, the result is incrementally updated in corresponding 
	dictionaries temp_stats, humidity_stats

	Inputs:
		data_set: all the data of a month
		temp_stats: dictionary recording stats for temperature
		humidity_stats: dictionary recording stats for humidity
		file_name: weather data file name used
	Output:
		Nothing is returned, incrementally
		find min and max stats and use dictionary for record
		saving.
	"""

	i = 0
	for line in data_set:
		if(i != 0):
			line = line.split(",")

			if(line[file_columns["Max_TemperatureC"]] is not ""):
				max_day_temp = int(line[file_columns["Max_TemperatureC"]])
				if((max_day_temp) > temp_stats["max_temp"]):
					temp_stats["max_temp"] = max_day_temp
					temp_stats["max_temp_date"] = line[file_columns["PKT"]]
					
			if(line[file_columns["Min_TemperatureC"]] is not ""):
				min_day_temp = int(line[file_columns["Min_TemperatureC"]])
				if((min_day_temp) < temp_stats["min_temp"]):
					temp_stats["min_temp"] = min_day_temp
					temp_stats["min_temp_date"] = line[file_columns["PKT"]]

			if(line[file_columns["Max_Humidity"]] is not ""):
				max_day_humidity = int(line[file_columns["Max_Humidity"]])
				if((max_day_humidity) > humidity_stats["max_humidity"]):
					humidity_stats["max_humidity"] = max_day_humidity
					humidity_stats["max_humidity_date"] = line[file_columns["PKT"]]
		i = i + 1

def process_file_avg_month(file_name):
	
	"""
	Process a weather data file for average max and min for temperature 
	and humidity 

	Inputs:
		file_name: filename of the weather date file to process
	Output:
		Nothing is returned, uses other helper functions to 
		find min and max stats
	"""

	try:
		with open(file_name) as open_file:
			data_set = []
			for line in open_file:
				data_set.append(line)
			compute_stats_avg_month(data_set, temp_stats, humidity_stats, file_name)
		print_stats_avg_month()
	except IOError as e:
		print("No files found with this year")

def compute_stats_avg_month(data_set, temp_stats, humidity_stats, file_name):
	
	"""
	Computes stats of average of max,min temp and humidity for a month 
	identified by file name

	Inputs:
		data_set: all the data of a month
		temp_stats: dictionary recording stats for temperature
		humidity_stats: dictionary recording stats for humidity
		file_name: weather data file name used
	Output:
		Nothing is returned, find mean and use dictionary for record
		saving.
	"""
	
	humidity_list = []
	max_temp_list = []
	min_temp_list = []

	i = 0
	for line in data_set:
		if(i != 0):
			line = line.split(",")

			if(line[file_columns["Max_TemperatureC"]] is not ""):
				max_day_temp = int(line[file_columns["Max_TemperatureC"]])
				max_temp_list.append(max_day_temp)

			if(line[file_columns["Min_TemperatureC"]] is not ""):
				min_day_temp = int(line[file_columns["Min_TemperatureC"]])
				min_temp_list.append(min_day_temp)
					
			if(line[file_columns["Mean_Humidity"]] is not ""):
				avg_day_humidity = int(line[file_columns["Mean_Humidity"]])
				humidity_list.append(avg_day_humidity)
		i = i + 1


	temp_stats["mean_max_temp"] = mean(max_temp_list)
	temp_stats["mean_min_temp"] = mean(min_temp_list)
	humidity_stats["mean_humidity"] = mean(humidity_list)
	
def process_file_for_minmax_month_histogram(file_name, month, year):
	
	"""
	Process a weather data file for  printing a histogram of
	max and min temperatures.

	Inputs:
		file_name: filename of the weather date file to process
		month: month
		year: year 
	Output:
		Nothing is returned, uses other helper functions to 
		find min and max stats
	"""

	try:
		with open(file_name) as open_file:
			data_set = []
			for line in open_file:
				data_set.append(line)
			#print(data_set)
			compute_stats_minmax_month(data_set, month, year)
	except IOError as e:
		print("No files found with this year")

def compute_stats_minmax_month(data_set, month, year):
	
	""" 
	Computes  max,min temperatures for a month 
	identified by file name

	Inputs:
		data_set: all the data of a month
		month: month
		year: year
	Output:
		Nothing is returned, use helper function 
	"""

	
	highest_temp_list = []
	lowest_temp_list = []
	
	i = 0
	for line in data_set:

		if (i != 0):
			line = line.split(",")
			
			if (line[file_columns["Max_TemperatureC"]] is not ""):
				highest_day_temp = int(line[file_columns["Max_TemperatureC"]])
				highest_temp_list.append(highest_day_temp)

			if (line[file_columns["Min_TemperatureC"]] is not ""):
				lowest_day_temp = int(line[file_columns["Min_TemperatureC"]])
				lowest_temp_list.append(lowest_day_temp)
		i = i + 1

	print_histogram(highest_temp_list, lowest_temp_list, month, year)

def generate_report_minmax_stats_for_year(path, year_to_search):
	
	"""	
	Generate report that prints out stats like 
	min, max temperature and date for a year. It 
	process data incrementally.

	Inputs:
		path: weather data files location
		year_to_search: year to search for the stats
	Output:
		Nothing is returned, use helper function 
	"""

	data_files_list = os.listdir(path)
	year_to_search = year_to_search

	for file in data_files_list:
		if(file[-12:-8] == year_to_search):
			process_file_for_minmax_stats(file)
	print_stats()

def generate_report_avg_minmax_stats_for_month(path, to_search):

	"""	
	Generate report showing avg of min,max and humidity  
	for a year/month specified.

	Inputs:
		path: weather data files location
		to_search: search string eg 2009/3
	Output:
		Nothing is returned, use helper function 
	"""

	data_files_list = os.listdir(path)

	file_name = create_filename_string(to_search)
	process_file_avg_month(file_name)
	
def generate_report_minmax_histogram_for_month(path, to_search):

	"""	
	Generate report that prints out a histogram of a 
	min and max temperature  for a year/month specified

	Inputs:
		path: weather data files location
		to_search: search string eg 2009/3
	Output:
		Nothing is returned, use helper function 
	"""
	
	data_files_list = os.listdir(".")
	
	month, year =  get_month_and_year(to_search)
	file_name = create_filename_string(to_search)

	process_file_for_minmax_month_histogram(file_name, month, year)

def sanitize_directory(directory_path):

	"""	
	Checks if directory sent to the script through command line 
	arguments is valid .

	Inputs:
		directory_path: weather data files location
	Output:
		Nothing is returned, use helper function 
	"""

	try:
		#print(directory_path)
		data_files_list = os.listdir(directory_path)
	except Exception as e:
		print("Input contains invalid directory, no such directory path found")
		sys.exit(0)

def sanitize_command_flags(command_flags):

	"""	
	Checks if commands flags sent to the script are valid 
	
	Inputs:
		command_flags: command flags list eg ['-a',-e]
	Output:
		Nothing is returned, use helper function to
		check their validity.

	"""

	commands=['-e','-a','-c']
	try:
		for flags in command_flags:
			if flags not in commands:
				raise Exception
	except Exception as e:
		print_invalid_flags_error()		

def sanitize_input_format(arguments_list):

	"""	
	Check the command line arguments passed 
	to script are valid 

	Inputs:
		arguments_list: command line argument eg "sys.argv"
	Output:
		Nothing is returned, use helper function to
		check their validity.

	"""

	arg_len = len(arguments_list)
	if(arg_len < 4 or 
		arg_len > 8):
		print_input_format_error()
	else:
		command_flags = []
		directory_path = arguments_list[1]

		if(arg_len not in [4,6,8]):
			print_input_format_error()

		if(arg_len == 4):
			command_flags.append(arguments_list[2])
		elif(arg_len == 6):
			command_flags.append(arguments_list[2])
			command_flags.append(arguments_list[4])
		elif(arg_len == 8):
			command_flags.append(arguments_list[2])
			command_flags.append(arguments_list[4])
			command_flags.append(arguments_list[6])

		sanitize_directory(directory_path)
		sanitize_command_flags(command_flags)

def print_input_format_error():

	"""	
	Prints error message for incorrect format 

	Inputs:
		None
	Output:
		Nothing is returned, use helper function. 
	"""
	
	print("Script arguments missing, please check the input")
	print("weatherman.py path/to/weatherdata command_flag year|month")	
	sys.exit(0)

def print_invalid_flags_error():

	"""	
	Prints error message for invalid flags choice 

	Inputs:
		None
	Output:
		Nothing is returned, use helper function. 
	"""

	print("Incorrect flags entered, choice available are -e,-a,-c")
	sys.exit(0)


def main():

	"""	
	Entry point for script 

	Inputs:
		None
	Output:
		Nothing is returned, use helper function. 
	"""
	
	sanitize_input_format(sys.argv)

	arguments_list = sys.argv
	path = arguments_list[1]
	arg_len = len(sys.argv)

	i = 2
	while(i < arg_len):
		cmd_flag = arguments_list[i]
		cmd_string = arguments_list[i+1]

		if(cmd_flag == '-e'):
			#sanitize_command_string(cmd_string)
			#print(cmd_flag)
			#print(cmd_string)
			generate_report_minmax_stats_for_year(path, cmd_string)
		elif(cmd_flag == "-a"):
			#sanitize_command_string(cmd_string)
			#print(cmd_flag)
			#print(cmd_string)
			generate_report_avg_minmax_stats_for_month(path, cmd_string)
		elif(cmd_flag == "-c"):
			#sanitize_command_string(cmd_string)
			#print(cmd_flag)
			#print(cmd_string)
			generate_report_minmax_histogram_for_month(path, cmd_string)
		i = i + 2	
main()




