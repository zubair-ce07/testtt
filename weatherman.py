""" Importing files for the program """
import sys
import re


class Days:
	
	""" This class is used to store a single day like 1,2,3
		and its Attributes as a Dictionary Object 
		like { 'attrib_name1' : 'value1', 'attribe_name2', 'value2' ...}"""
	def __init__( self, days, attributes):
		
		self.days = days
		self.attributes = attributes

class Month:
    
	""" This Class will be used to store the month name
		and a disctionary object of Days class
		like { '1' : Days_class_object, '2' : Days_class_object ...}""" 
	def __init__( self, month, days):

		self.month = month
		self.days = days

class Year:
    
	""" This Class will be used to store year like 2014
		and dictionary objects of Month Class
		like { 'Jan' : Month_Class_object, 'Feb' : Month_class_object ...}"""
	def __inti__( self, year, months):

		self.year = 0
		self.months = {}

class FileReading:
	
	""" This class condtains method for readin files and DATA Members to store 
		header of the file that will be further used in storing the data
		in the dictionary"""
	def __init__( self):

		self.header_list = []
		self.years = []    
    
	def setHeaderList( self, comma_sep_list):
		
		self.header_list = comma_sep_list.split(',')

	def get_month_list( self, month):

		month_list = [
				"Jan", "Feb", "Mar",
				"Apr", "May", "Jun",
				"Jul", "Aug", "Sep", 
				"Oct", "Nov", "Dec"
				]

		if(month == "all"):
			
			return month_list

		else:

			return [month_list[int(month) - 1]]

	def reading_data( self, file_name, path):
		
		if (len(file_name) > 4):
		
			year, month = file_name.split('/')
		
		else:
		
			year = file_name
			month = "all"
		
		month_list = self.get_month_list(month)
		
		months_dict = {}

		for month in month_list:
			
			readed_month = self.read_files_data(path + 
								"/" +
								"Murree_weather_" +
								year +
								"_" +
								month +
								".txt")
			
			temp = Month(
				month = month, 
				days = readed_month
				)
			
			months_dict.update(
						{month : temp}
					)

		return months_dict

	def read_files_data(
				self, 
				path):

        # open & read all the file and strip into line by line
		lines = [
			line.rstrip('\n') for line in open(path)
			]
        
		month_dict = {}
		
        #setting the header of the Data structure
		self.setHeaderList(lines[0])
	
		for days in range(1, len(lines)):
			list_of_data = lines[days].split(',')
			
			list_of_attributes = list_of_data[
										0:len(list_of_data)
										]
            
            # Making Dictionary from the attributes and tha values
			day_dict = {} 
			
			for i in range(0,len(list_of_attributes)):
				if list_of_attributes[i] == "":
					list_of_attributes[i] = "-9999"		# For Missing Values
				
				day_dict.update(
						{self.header_list[i]:list_of_attributes[i]}
					)
            
			month_dict.update(
					{days : Days(days = days, attributes =  day_dict)}
				)

		return month_dict

class Reporting:
	
	""" This class is solely responsiable for report calculation
		and show it on console"""
	def __init__( self):
		
		self.highest = 0
		self.lowest = 9999

	""" Method of -a action """
	def calculate_and_show_avg_report ( self, months):
		
		humid_val_sum = 0
		temp_high_avg = 0
		temp_low_avg = 0
		numbers_of_days = 0

		months_key_list = list(
							months.keys()
						)
		
		for month_key in months_key_list:
			
			days_key_list = list(months[month_key].days)

			for day_key in days_key_list:
				
				if months[month_key].days[day_key].attributes[' Mean Humidity'] != "-1":
					humid_val_sum += int(months[month_key].days[day_key].attributes[' Mean Humidity'])
					temp_high_avg += int(months[month_key].days[day_key].attributes['Max TemperatureC'])
					temp_low_avg += int(months[month_key].days[day_key].attributes['Min TemperatureC'])
					numbers_of_days += 1
				
		print ( "Highest Average: ", round(temp_high_avg/numbers_of_days, 2), 
				"C"),
		
		print ( "Lowest Average: ", round(temp_low_avg/numbers_of_days, 2), 
				"C"),
		
		print ( "Average Mean Humidity:", round(humid_val_sum/numbers_of_days, 2), 
				"% ")

	""" Method of -c action """
	def calculate_and_show_chart_report( self, months):
		
		high_temp_val = 0
		low_temp_val = 0

		months_key_list = list(
							months.keys()
						)
		
		for month_key in months_key_list:
			
			days_key_list = list( 
								months[month_key].days
							)

			#print(numbers_of_days)
			for day_key in days_key_list:

				if months[month_key].days[day_key].attributes['Max TemperatureC'] != "-1":

					high_temp_val = int(months[month_key].days[day_key].attributes['Max TemperatureC'])
					
					low_temp_val = int(months[month_key].days[day_key].attributes['Min TemperatureC'])

					print(day_key, " ", end = '')
					
					for i in range(high_temp_val):
						
						print (
							'\033[1;31m+\033[1;m', end = ''
							)
					
					print (
						" ", high_temp_val,
						"C\n", sep = ""
						)

					print (
						day_key, " ", end = ''
						)
					
					for i in range(low_temp_val):
						
						print (
							'\033[1;34m+\033[1;m', end = ''
							)
					
					print (
						" ", low_temp_val,
						'C\n', sep = ""
						)
	
	""" Method of -c action One Line Chart Report"""
	def show_Single_line_report( self, months):
		
		high_temp_val = 0
		low_temp_val = 0

		months_key_list = list(
							months.keys()
						)
		
		for month_key in months_key_list:
			
			days_key_list = list( 
							months[month_key].days
						)

			#print(numbers_of_days)
			for day_key in days_key_list:

				if months[month_key].days[day_key].attributes['Max TemperatureC'] != "-1":

					high_temp_val = int(months[month_key].days[day_key].attributes['Max TemperatureC'])
					
					low_temp_val = int(months[month_key].days[day_key].attributes['Min TemperatureC'])

					print(day_key, " ", end = '')
					
					for i in range(low_temp_val):
						
						print (
							'\033[1;34m+\033[1;m', end = ''
							)
					
					for i in range(high_temp_val):
						
						print (
							'\033[1;31m+\033[1;m', end = '')
					
					print (
						" ", low_temp_val, "C"
						" - ", high_temp_val,
						'C\n', sep = ""
						)

	""" Class for -e Calculation """	
	def calculate_and_show_report( self, months):

		humid_highest_day = ""
		humid_highest_month = ""
		humid_highest_val = 0

		months_key_list = list( months.keys())
		
		for month_key in months_key_list:

			
			days_key_list = list( months[month_key].days)

			for day_key in days_key_list:

				if int( months[month_key].days[day_key].attributes['Max TemperatureC']) > self.highest:

					self.highest = int(months[month_key].days[day_key].attributes['Max TemperatureC'])
					highest_day = months[month_key].days[day_key].days
					highest_month = months[month_key].month
				
				if (int( months[month_key].days[day_key].attributes['Min TemperatureC']) < self.lowest and 
						months[month_key].days[day_key].attributes['Min TemperatureC'] != "-9999"):

					self.lowest = int(months[month_key].days[day_key].attributes['Min TemperatureC'])
					lowest_day = months[month_key].days[day_key].days
					lowest_month = months[month_key].month
				
				if int( months[month_key].days[day_key].attributes['Max Humidity']) > humid_highest_val:

					humid_highest_day = months[month_key].days[day_key].days
					humid_highest_month = months[month_key].month
					humid_highest_val = int(months[month_key].days[day_key].attributes['Max Humidity'])
				
		print(
			"Highest: ", self.highest,
			"C on ",highest_month, 
			" ", highest_day, 
			sep = ""
			)
		
		print(
			"Lowest Value : ", self.lowest, 
			"C on ", lowest_month, 
			" ", lowest_day, 
			sep = ""
			)
		
		print(
			"Humidity:", humid_highest_val, 
			"% ", "on ", humid_highest_month, 
			" ", humid_highest_day, 
			sep = ""
			)
		
	
class FileAndAction:

	""" This Class is for storing file name and its action """
	def __init__( self, action = None, file_name = None):

		self.action = action
		self.file_name = file_name
	

""" Defineing the main Function logic here """
def main():

	# Empty List for the FILE AND REPORT Class objects
	list_of_file_and_actions = []
	path_to_files = ""
	
	if ( len( sys.argv) > 1):
		
		# Extracting the path of the file
		path_to_files = sys.argv[1]
		
		""" Extracting the number of files provided
			by the user for reporting"""
		file_count = ( len(sys.argv) - 2)/2

		""" Making a seperate List of Actions
			and File names"""
		file_action_and_name = sys.argv[2:]

		for index in range( int( file_count)):

			# Checking the input is valid and correct
			if ( re.match(
						'-[ace]', 							# RE for checking Action
						file_action_and_name[index*2]) and 
					re.match(
						'20[0-10-9]', 						# RE for Checking the Year Formate
						file_action_and_name[index*2+1]
						)
					):

				""" stroing file name and action into FileAndAction Class object
					into Temperory Object """
				temp_object_for_filereport = FileAndAction ( 
													action = file_action_and_name[index*2], 
													file_name = file_action_and_name[(index*2)+1]
												)

				# Appending the Temporaobjy object into the List
				list_of_file_and_actions.append (
								temp_object_for_filereport
							)
			else:
				
				print("Invalid Input Aurguments")
	else:
		print("No File Name Passed!")

	"""	 Checking if files are given then to perform the actions
		 accordingly"""
	if( len( list_of_file_and_actions) > 0):
		
		for index in list_of_file_and_actions:
			
			temp_file_reading = FileReading()	
			
			Months = FileReading.reading_data (
						temp_file_reading,
						index.file_name, 
						path_to_files
					)
			
			# Making Temperory object for send as self argument
			temp_reporting = Reporting()

			if index.action == "-a":
				
				# Calling Function for '-a ' Action
				print (
					"\n"
				)
				Reporting.calculate_and_show_avg_report (
							temp_reporting, 
							Months
						)
			
			elif index.action == "-c":
				# Calling Function for '-c ' Action
				print (
					"\n"
				)
				Reporting.calculate_and_show_chart_report (
							temp_reporting, 
							Months
						)
				Reporting.show_Single_line_report (
							temp_reporting, 
							Months
						)
			
			else:
				# Calling Function for '-e ' Action
				print (
					"\n"
				)
				Reporting.calculate_and_show_report (
							temp_reporting, 
							Months
						)


""" Calling the "main" Method from here """
if __name__ == "__main__":

    main()