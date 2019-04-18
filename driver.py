import sys
import argparse
from weather_reporter import WeatherReporter, Constants

def main():
	""" main function """
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-a", "--year_data", action="store_true")
	group.add_argument("-b", "--month_data", action="store_true")
	group.add_argument("-c", "--month_split_bar", action="store_true")
	group.add_argument("-d", "--month_bar", action="store_true")	
	parser.add_argument("date", help="enter date")
	parser.add_argument("path", help="enter path")
	args = parser.parse_args()
	path_to_files = sys.argv[3]
	weather = WeatherReporter(path_to_files)
	date_arguments = [] 
	date_arguments = args.date.split('/')

	if args.year_data:
		max_temp, date = weather.calculate_max_temperature(date_arguments[0])
		if max_temp is not None:
			print('Max Tempterature: ' +  str(max_temp) + ' Date: ' + date)
		min_temp, date = weather.calculate_min_temperature()
		if min_temp is not None:	
			print('Min Tempterature: ' +  str(min_temp) + ' Date: ' + date)
		max_humidity, date = weather.calculate_max_humidity()
		if max_humidity is not None:	
			print('Max Humidity: ' +  str(max_humidity) + ' Date: ' + date)
		else :
			print ('The year list is empty')		
		
	elif args.month_data:
		avg_max = weather.calculate_average_max_temperature(date_arguments[0], int(date_arguments[1]))
		if avg_max is not None:
			print('Maximum average temperature: ' + str(avg_max))
		avg_min = weather.calculate_average_min_temperature()
		if avg_min is not None:	
			print('Minimum average temperature: ' + str(avg_min))
		avg_humdity = weather.calculate_average_max_humidity()
		if avg_humdity is not None:
			print('Maximum average humidity: ' + str(avg_humdity))
		else:
			print('The month list is empty')

	elif args.month_split_bar:
		weather.calculate_daily_report(date_arguments[0], int(date_arguments[1]), Constants.bar)

	elif args.month_bar:
		weather.calculate_daily_report(date_arguments[0], int(date_arguments[1]), Constants.single_bar)

if __name__ == "__main__":
	main()
