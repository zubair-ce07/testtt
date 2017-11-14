from termcolor import colored
month_dict = {1: "Jan" ,2: "Feb", 3: "Mar" , 4: "Apr" , 5: "May" , 6: "Jun" , 7: "Jul" 
				, 8: "Aug" , 9: "Sep" , 10: "Oct" , 11: "Nov" , 12: "Dec"}
class GenerateReport:

	def generate_report_year(self, result_data):

		month1 = (result_data["max_temp_dict"].get("PKT") or
				 result_data["max_temp_dict"].get("PKST")).split("-")[-2]
		
		day1 = (result_data["max_temp_dict"].get("PKT") or 
				result_data["max_temp_dict"].get("PKST")).split("-")[-1]
	
		month2 = (result_data["min_temp_dict"].get("PKT") or
				 result_data["min_temp_dict"].get("PKST")).split("-")[-2]

		day2 = (result_data["min_temp_dict"].get("PKT") or 
				result_data["min_temp_dict"].get("PKST")).split("-")[-1]

		month3 = (result_data["max_humid_dict"].get("PKT") or
				 result_data["max_humid_dict"].get("PKST")).split("-")[-2]
		
		day3 = (result_data["max_humid_dict"].get("PKT") or 
				result_data["max_humid_dict"].get("PKST")).split("-")[-1]


		print("Highest: %sC on %s %s" % (result_data["max_temp_dict"]["Max TemperatureC"]
										, month_dict[int(month1)], day1))

		print("Lowest: %sC on %s %s" % (result_data["min_temp_dict"]["Min TemperatureC"]
										, month_dict[int(month2)], day2))

		print("Humid: %s%% on %s %s" % (result_data["max_humid_dict"]["Max Humidity"]
										, month_dict[int(month3)], day3))


	def generate_report_month(self, result_data):

		print("Highest Average: %s"% result_data["max_avg_temp"]["Mean TemperatureC"])
		print("Lowest Average: %s"% result_data["min_avg_temp"]["Mean TemperatureC"])
		print("Average Humidity: %s%%"% result_data["avg_humidity"]["average"])
	
	def generate_bar_chart(self, result_data, is_single):
		
		max_str = min_str = ""
		for i in result_data:
			if result_data[i]["max"] != '' and result_data[i]["min"] != '':
				for k in range(0,int(result_data[i]["max"])):
					max_str += colored('+', 'red')
				for k in range(0,int(result_data[i]["min"])):
					min_str += colored("+","blue")

				if is_single:
					min_str += max_str
					print("%s %s %sC - %sC"% (result_data[i]["day"], min_str,
											 result_data[i]["min"], result_data[i]["max"]))
				else:
					print("%s %s %sC"% (result_data[i]["day"], max_str, result_data[i]["max"]))
					print("%s %s %sC"% (result_data[i]["day"], min_str, result_data[i]["min"]))
				
				max_str = min_str = ""

