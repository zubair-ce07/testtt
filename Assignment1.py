import glob
import os
import sys



def Weather_compare(date_max_temp,Max_Temp,date_min_temp,Min_Temp,
							Max_Humidity,Min_Humidity, weather_dic,year):
	if(Max_Temp != ''): 
		if  int(Max_Temp) > int(weather_dic[year]['Max_Temp_Dic']['Max_Temp']):
					weather_dic[year]['Max_Temp_Dic']['Max_Temp'] = Max_Temp
					weather_dic[year]['Max_Temp_Dic']['date'] = date_max_temp

	if(Min_Temp != ''): 				
		if int(Min_Temp) < int(weather_dic[year]['Min_Temp_Dic']['Min_Temp']) or weather_dic[year]['Min_Temp_Dic']['Min_Temp'] == '':	
					weather_dic[year]['Min_Temp_Dic']['Min_Temp'] = Min_Temp
					weather_dic[year]['Min_Temp_Dic']['date'] = date_min_temp

	if(Max_Humidity != ''): 
		if int(Max_Humidity) > int(weather_dic[year]['Max_Humidity']):
					weather_dic[year]['Max_Humidity'] = Max_Humidity
	if(Min_Humidity != ''): 
		if int(Min_Humidity) < int(weather_dic[year]['Min_Humidity']) or weather_dic[year]['Min_Humidity'] == '':
					weather_dic[year]['Min_Humidity'] = Min_Humidity

def value_replace ( weather_dic,year):
	if  weather_dic[year]['Max_Temp_Dic']['Max_Temp'] == '':
		weather_dic[year]['Max_Temp_Dic']['Max_Temp'] = -1000

	if  weather_dic[year]['Min_Temp_Dic']['Min_Temp'] == '':
		weather_dic[year]['Min_Temp_Dic']['Min_Temp'] = 1000

	if  weather_dic[year]['Max_Humidity'] == '':
		weather_dic[year]['Max_Humidity'] = -1000

	if  weather_dic[year]['Min_Humidity'] == '':
		weather_dic[year]['Min_Humidity'] = 1000



#Read data From File
def read_weather_data(data_directory):
	os.chdir(data_directory)

	for file_name in glob.glob("*.txt"):

		file_data = open(file_name)
		line_counter = 0
		for line in file_data:
			if line_counter > 1:
				weather_variables = line.split(',')
				year = weather_variables[0].split('-')
				if line_counter == 2 and year[0] not in weather_dic:
					weather_dic[year[0]] ={'Max_Temp_Dic' : {'date' : weather_variables[0],'Max_Temp' : weather_variables[1]},
							   	   		'Min_Temp_Dic':{'date' : weather_variables[0],'Min_Temp' : weather_variables[3]}, 
							   	   		'Max_Humidity' : weather_variables[7],'Min_Humidity' : weather_variables[9]}
					value_replace(weather_dic,year[0])
				else:
					if len(weather_variables) > 1:
						Weather_compare(weather_variables[0],weather_variables[1],weather_variables[0],
												weather_variables[3],weather_variables[7],
												weather_variables[9],weather_dic,year[0])

						
			
			line_counter = line_counter + 1

def report_genrate_Annual():
	print "Annual Max/Min Temperature"+'\n'
	print  "   Year 	" + "MAX Temp 	" + "MIN Temp 	" + "MAX Humidity 	" + "MIN Humidity 	"
	print '\n' + "   -------------------------------------------------------------------------"

	for key in weather_dic:
		print "   " + key + "		 " + weather_dic[key]['Max_Temp_Dic']['Max_Temp'] + "	 	  "+ weather_dic[key]['Min_Temp_Dic']['Min_Temp'] + "		   "+weather_dic[key]['Max_Humidity'] + " 	    	  " + weather_dic[key]['Min_Humidity'] 
	print '\n'

def report_genrate_coolday():
	print '\n'
	print  "   Year 	 " + "  Date 	" + "MAX Temp"
	print '\n' + "   ------------------------------------"

	for key in weather_dic:
		print "   " + key + " 	" + weather_dic[key]['Max_Temp_Dic']['date'] + " 	 "+ weather_dic[key]['Max_Temp_Dic']['Max_Temp']
	print '\n'
def report_genrate_Hotday():
	print '\n'
	print  "   Year 	 " + "  Date 	" + "MIN Temp"
	print '\n' + "   ------------------------------------"

	for key in weather_dic:
		print "   " + key + " 	" + weather_dic[key]['Min_Temp_Dic']['date'] + " 	 "+ weather_dic[key]['Min_Temp_Dic']['Min_Temp']
	print '\n'


def main():
	
	arg_list = []
	for arg in sys.argv:
		arg_list.append(arg)
	if len(arg_list) > 1:

		read_weather_data(arg_list[2])

		if int(arg_list[1]) == 1:
			report_genrate_Annual()

		if int(arg_list[1]) == 2:
			report_genrate_coolday()

		if int(arg_list[1]) == 3:
			report_genrate_Hotday()
	else:
		read_weather_data('weatherdata')
		report_genrate_Annual()
		report_genrate_coolday()
		report_genrate_Hotday()

weather_dic = {}
if __name__ == "__main__":
   main()

