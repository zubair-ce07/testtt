import sys
from termcolor import colored

month_dict = {1: "Jan" ,2: "Feb", 3: "Mar" , 4: "Apr" , 5: "May" , 6: "Jun" , 7: "Jul" , 8: "AUg" , 9: "Sep" , 10: "Oct" , 11: "Nov" , 12: "Dec"}

#prints bar chart on the basis of is_single,
#if is_single will be 1 than chart will be printed in one single line otherwise it will be printed in two different lines.
def print_bar_chart(bar_chart_list , is_single):
	max_str = min_str = ""
	for i in bar_chart_list:
		for k in range(0,i["max"]):
			max_str += colored('+', 'red')
		for k in range(0,i["min"]):
			min_str += colored("+","blue")
		
		if is_single == 0:
			print("%d %s %dC" % (i["day"],max_str,i["max"]))
			print("%d %s %dC" % (i["day"],min_str,i["min"]))
		else:
			min_str += max_str
			print("%d %s %dC - %dC" % (i["day"],min_str,i["min"], i["max"]))
		
		max_str = min_str = ""

def read_files_and_generate_reports(year,month,file_path):
	
	#month related reports
	if month:
		try:
			file_name = file_path+"/lahore_weather_"+year+"_"+month_dict[int(month)]+".txt"
		except:
			print("Enter correct month.")
			return
		try:
			f =  open(file_name)
		except:
			print("404 --- File not Found")
			return
		next(f)
		
		bar_chart_list = []
		
		weather_report = {x.strip(): None for x in f.readline().split(",")}
		avg_temp_arr = []
		avg_humidity_arr = []
		
		for line in f: # processing every line
			line_arr = [i for i in line.split(",")]
			try:
				avg_temp_arr.append(int(line_arr[2])) # getting average temperature for a particular date
			except:
				pass	
			try:
				avg_humidity_arr.append(int(line_arr[8])) # getting all humidities level for a particular month
			except:
				avg_humidity_arr.append(0) # assuming humidity 0 for particular date if it is not specified

			try:
				date = line_arr[0].split("-")

				bar_chart_list.append({"day":int(date[2]) ,"max": int(line_arr[1]) , "min" : int(line_arr[3])}) # making bar chart list to print afterwards
			except:
				pass

		avg_temp_arr.sort()

		highest_average = avg_temp_arr[len(avg_temp_arr)-1]
		lowest_average = avg_temp_arr[0]
		average_humidity = sum(avg_humidity_arr)/len(avg_humidity_arr) # taking average
		
		#printing results
		print("Highest Average: %d"% highest_average)
		print("Lowest Average: %d"% lowest_average)
		print("Average Humidity: %d%%\n"% average_humidity)

		print_bar_chart(bar_chart_list,0)
		print("\n")
		print_bar_chart(bar_chart_list,1)
		f.close()
	else: # year related report
		max_temp_arr= []
		min_temp_arr = []
		max_humidity_arr = []
		for i in range(1,13): # loop for all months in the specified year
			file_name = file_path+"/lahore_weather_"+year+"_"+month_dict[i]+".txt" 
			#print(file_name)

			try:
				f = open(file_name)
			except:
				continue
				
			next(f)
			next(f)

			for line in f:
				line_arr = [i for i in line.split(",")]

				try:

					max_temp_arr.append({"date" : line_arr[0] ,"temp": int(line_arr[1])})
					min_temp_arr.append({"date" : line_arr[0] ,"temp": int(line_arr[3])})
					max_humidity_arr.append({"date" : line_arr[0] ,"temp": int(line_arr[7])})
				except:
					pass

			f.close()

		if (len(max_temp_arr) > 0 and len(min_temp_arr) > 0 and len(max_humidity_arr) > 0):
			max_temp_arr = sorted(max_temp_arr, key=lambda k: k['temp'])
			min_temp_arr = sorted(min_temp_arr, key=lambda k: k['temp'])
			max_humidity_arr = sorted(max_humidity_arr, key=lambda k: k['temp'])
			
			max_temp_day = max_temp_arr[len(max_temp_arr)-1]["date"].split("-")[2]
			max_temp_month = month_dict[int(max_temp_arr[len(max_temp_arr)-1]["date"].split("-")[1])]

			min_temp_day = min_temp_arr[0]["date"].split("-")[2]
			min_temp_month = month_dict[int(min_temp_arr[0]["date"].split("-")[1])]

			max_humid_day = max_humidity_arr[len(max_humidity_arr)-1]["date"].split("-")[2]
			max_humid_month = month_dict[int(max_humidity_arr[len(max_humidity_arr)-1]["date"].split("-")[1])]



			print("Highest: %dC on %s %s" % (max_temp_arr[len(max_temp_arr) - 1]["temp"] , max_temp_month , max_temp_day))
			print("Lowest: %dC on %s %s" % (min_temp_arr[0]["temp"] , min_temp_month , min_temp_day))
			print("Humid: %d%% on %s %s" % (max_humidity_arr[len(max_humidity_arr) - 1]["temp"] , max_humid_month , max_humid_day))

	
def main():
	year = month = None

	try:
		year , month = sys.argv[1].split("/")
	except:
		year = sys.argv[1]

	path = sys.argv[2]

	read_files_and_generate_reports(year,month,path)



if __name__== "__main__":
  main()