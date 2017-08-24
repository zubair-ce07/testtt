import csv
import glob
import os
month_dict = {1: "Jan" ,2: "Feb", 3: "Mar" , 4: "Apr" , 5: "May" , 6: "Jun" ,
			 7: "Jul" , 8: "Aug" , 9: "Sep" , 10: "Oct" , 11: "Nov" , 12: "Dec"}

class WeatherReader:

	weather_reading_list = []

	def parse_files(self, year,
					 path, month=None):
	
		for filepath in glob.glob(os.path.join(path, '*.txt')):
			filename = filepath.split("/")[-1].split(".")[0]
			try:
				if month:
					month_str = month_dict[int(month)]
			except:
				print("Invalid month entered.")
				return -1

			#print(year)
			if filename.split("_")[-2] == str(year):
				if (month == None or (month and filename.split("_")[-1] == month_str)):
				#print("yesasdfadsfasdfasdfad")
					try:
						f = open(filepath)
						next(f)
					except:
						print("File not found")
						return -1

					input_file = csv.DictReader(f)

					for row in input_file:
						row = {x.strip(): y for x,y in row.items()}
						self.weather_reading_list.append(row)
						#print(row)
					f.close()

		if len(self.weather_reading_list) == 0:
			print("Something went wrong")
			return -1
		return 1
	


