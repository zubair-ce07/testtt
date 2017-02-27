# -----------------  Importing sys for Reading Command Line Argument  ----------------------
import sys

# -----------------  Importing os.path for checking is file exist  ----------------------
import os.path

# -----------------  Importing string for using string functions  ----------------------
import string

# -----------------  Importing re for using Regular Expression to Validate Command Line Arguments  ----------------------
import re

# -----------------  Dictionary For Months for creating File Name  ----------------------
Months = {
	"Jan" : 1,
	"Feb" : 2,
	"Mar" : 3,
	"Apr" : 4,
	"May" : 5,
	"Jun" : 6,
	"Jul" : 7,
	"Aug" : 8,
	"Sep" : 9,
	"Oct" : 10,
	"Nov" : 11,
	"Dec" : 12
}

# -----------------  Dictionary For Months for Displaying Full Name  ----------------------
Complete_Month_Name = {
	"1" : "January",
	"2" : "February",
	"3" : "March",
	"4" : "April",
	"5" : "May",
	"6" : "June",
	"7" : "July",
	"8" : "August",
	"9" : "September",
	"10" : "October",
	"11" : "November",
	"12" : "December"
}

# -----------------  Dictionary For Data (Files Data)  ----------------------
Data_dict = {
	"PKT" : 0,
	"Max_TemperatureC" : 1,
	"Mean_TemperatureC" : 2,
	"Min_TemperatureC" : 3,
	"Dew_PointC" : 4,
	"MeanDew_PointC" : 5,
	"Min_DewpointC" : 6,
	"Max_Humidity" : 7,
	"Mean_Humidity" : 8,
	"Min_Humidity" : 9,
	"Max_Sea_Level_PressurehPa" : 10,
	"Mean_Sea_Level_PressurehPa" : 11,
	"Min_Sea_Level_PressurehPa" : 12,
	"Max_VisibilityKm" : 13,
	"Mean_VisibilityKm" : 14,
	"Min_VisibilitykM" : 15,
	"Max_Wind_SpeedKmh" : 16,
	"Mean_Wind_SpeedKmh" : 17,
	"Max_Gust_SpeedKmh" : 18,
	"PrecipitationCm" : 19,
	"CloudCover" : 20,
	"Events" : 21,
	"WindDirDegrees" : 22,
}

# -----------------  Todo: Need discussion with Omair Bhai  ----------------------
# -----------------  Function for converting string to Integer if string is empty then return 0  ----------------------
def convert_string_to_int(s):
	s = s.strip()
	return int(s) if s else 0


# -----------------  Function for converting string list to Integer list so that math function can work on lists  ----------------------
def ConvertStringList_to_int(strlist):
	retlist = []
	for s in strlist:
		retlist.append(convert_string_to_int(s))
	return retlist

# -----------------  Function for return month name(file name format) from Months dictionary  ----------------------
def getmonth_by_value(val):
	for key, value in Months.iteritems():
		if value == val:
			return key

# -----------------  Function for reading a single file  ----------------------
def read_singlefile(file_name, path):
	date = file_name.split('/')
	file_name = "lahore_weather_" + date[0] + "_" + str(getmonth_by_value(int(date[1]))) + ".txt"
	full = path + file_name
	
	if not os.path.isfile(full):
		sys.exit(full + " No such file is present in given path")
	with open(full, "r") as f:
		data = f.readlines()
	del data[0]
	del data[0]
	del data[len(data)-1]
	
	list_of_details = [[] for i in range(len(Data_dict))]
	
	for line in data:
		words = line.split(',')
		
		for temp in xrange(0, len(Data_dict)):
			list_of_details[temp].append(words[temp])
	
	return list_of_details

# -----------------  Task-1  ----------------------
def task_1(year, path):

	highest_temperature = 0
	highest_temperature_day_month = 0
	highest_temperature_day = 0
	lowest_temperature = 100
	lowest_temperature_day_month = 0
	lowest_temperature_day = 0
	most_humidity = 0
	most_humid_day_month = 0
	most_humid_day = 0

	tmp_highest_temperature = 0
	tmp_lowest_temperature = 0
	tmp_most_humidity = 0

	for temp in xrange(1, len(Months)+1):
		file_name = year + "/" + str(temp)
		
		
		list_of_details = read_singlefile(file_name, path)
		
		Max_TemperatureC = list_of_details[Data_dict.get("Max_TemperatureC")]
		Min_TemperatureC = list_of_details[Data_dict.get("Min_TemperatureC")]
		Max_Humidity = list_of_details[Data_dict.get("Max_Humidity")]
		
		Max_TemperatureC = ConvertStringList_to_int(Max_TemperatureC)
		Min_TemperatureC = ConvertStringList_to_int(Min_TemperatureC)
		Max_Humidity = ConvertStringList_to_int(Max_Humidity)
		
		
		tmp_highest_temperature = max(Max_TemperatureC)
		tmp_lowest_temperature = min(Min_TemperatureC)
		tmp_most_humidity = max(Max_Humidity)
		
		if tmp_highest_temperature > highest_temperature:
			highest_temperature = tmp_highest_temperature
			highest_temperature_day_month = temp
			highest_temperature_day = Max_TemperatureC.index(tmp_highest_temperature)+1
			
		
		if tmp_lowest_temperature < lowest_temperature:
			lowest_temperature = tmp_lowest_temperature
			lowest_temperature_day_month = temp
			lowest_temperature_day = Min_TemperatureC.index(tmp_lowest_temperature)+1
			
			
		if tmp_most_humidity > most_humidity:
			most_humidity = tmp_most_humidity
			most_humid_day_month = temp
			most_humid_day = Max_Humidity.index(tmp_most_humidity)+1
		
	
	print("Highest: " + str(highest_temperature) + "C on " + Complete_Month_Name.get(str(highest_temperature_day_month)) + " " + str(highest_temperature_day))
	print("Lowest: " + str(lowest_temperature) + "C on " + Complete_Month_Name.get(str(lowest_temperature_day_month)) + " " + str(lowest_temperature_day))
	print("Humid: " + str(most_humidity) + "% on " + Complete_Month_Name.get(str(most_humid_day_month)) + " " + str(most_humid_day))
	
	
# -----------------  Task-2  ----------------------
def task_2(file_name, path):

	list_of_details = read_singlefile(file_name, path)
		
	Max_TemperatureC = list_of_details[Data_dict.get("Max_TemperatureC")]
	Min_TemperatureC = list_of_details[Data_dict.get("Min_TemperatureC")]
	Mean_Humidity = list_of_details[Data_dict.get("Mean_Humidity")]

	Max_TemperatureC = ConvertStringList_to_int(Max_TemperatureC)
	Min_TemperatureC = ConvertStringList_to_int(Min_TemperatureC)
	Mean_Humidity = ConvertStringList_to_int(Mean_Humidity)

	print ("Highest Average: " + str(sum(Max_TemperatureC)/len(Max_TemperatureC)) + "C")
	print ("Lowest Average: " + str(sum(Min_TemperatureC)/len(Min_TemperatureC)) + "C")
	print ("Average Humidity: " + str(sum(Mean_Humidity)/len(Mean_Humidity)) + "%")

# -----------------  Function for creating bar graph according to given parameters  ----------------------
def create_bar_graph(temp_list, colortype, count):
	ptr = ""
	if colortype == 1:
		ptr +=	"\033[1;31m"
	else:
		ptr += "\033[1;34m"
	lop = convert_string_to_int(temp_list[count])
	for temp in xrange(0, lop):
		ptr += "+"
	ptr += "\033[1;m"
	return ptr

# -----------------  Task-3  ----------------------
def task_3(file_name, path):
	
	list_of_details = read_singlefile(file_name, path)
	
	PKT = list_of_details[Data_dict.get("PKT")]	
	Max_TemperatureC = list_of_details[Data_dict.get("Max_TemperatureC")]
	Min_TemperatureC = list_of_details[Data_dict.get("Min_TemperatureC")]
	
	
	count = 0
	for date in PKT:
		ptr = ""
		day = date.split('-')
		month = convert_string_to_int(day[2])
		if month < 10:
			month = "0" + str(month)
		else:
			month = day[2]
		ptr += month + " "
		ptr += 	create_bar_graph(Max_TemperatureC,1,count)
		ptr += " "
		ptr += Max_TemperatureC[count]
		ptr += "C"
		print (ptr)

		ptr = ""
		ptr += month + " "
		ptr += 	create_bar_graph(Min_TemperatureC,2,count)
		ptr += " "
		ptr += Min_TemperatureC[count]
		ptr += "C"
		print (ptr)
		count = count + 1

# -----------------  Task-4  ----------------------
def task_4(file_name, path):
	
	list_of_details = read_singlefile(file_name, path)
		
	PKT = list_of_details[Data_dict.get("PKT")]
	Max_TemperatureC = list_of_details[Data_dict.get("Max_TemperatureC")]
	Min_TemperatureC = list_of_details[Data_dict.get("Min_TemperatureC")]
	
	count = 0
	for date in PKT:
		ptr = ""
		day = date.split('-')
		month = convert_string_to_int(day[2])
		if month < 10:
			month = "0" + str(month)
		else:
			month = day[2]
		ptr += month + " "
		ptr += 	create_bar_graph(Min_TemperatureC,2,count)		
		ptr += 	create_bar_graph(Max_TemperatureC,1,count)
		ptr += " " + Min_TemperatureC[count] + "C - " + Max_TemperatureC[count] + "C"
				
		print (ptr)
		count = count + 1


# -----------------  Function to validate the Command Line Arguments  -----------------
def validate(option, detail):
	regex_for_option_a = r"^\d{4}$"
	regex_for_other_options = r"^\d{4}/\d{1,2}$"

	if option == '-e':
		if re.match(regex_for_option_a , detail, re.M|re.I):
			return True
		else:
			return False
	else:
		if re.match(regex_for_other_options , detail, re.M|re.I):
			return True
		else:
			return False
	
	      	

# -----------------  Reading Command Line Arguments and calling appropriate function according to given function ----------------------

if len(sys.argv) < 4:
	sys.exit("Please provide full arguments")

o = sys.argv[1]

if not validate(o, sys.argv[2]):
	sys.exit("Given arguments are not correct")
	
if o == '-e':
	task_1(sys.argv[2], sys.argv[3])
elif o == '-a':
        task_2(sys.argv[2], sys.argv[3])
elif o == '-c':
	task_3(sys.argv[2], sys.argv[3])
elif o == '-b':
	task_4(sys.argv[2], sys.argv[3])
else:
	print("No Option Match the Requirements")

