import sys
import argparse
from driver import WeatherReporter

def main():
	""" main function """
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-a", "--year_data", action="store_true")
	group.add_argument("-b", "--month_data", action="store_true")
	group.add_argument("-c", "--month_split_bar", action="store_true")
	group.add_argument("-d", "--month_bar", action="store_true")	
	parser.add_argument("year", help="enter year")
	parser.add_argument("month", help="enter month")
	parser.add_argument("path", help="enter path")
	args = parser.parse_args()

	path_to_files = sys.argv[4]
	weather = WeatherReporter(path_to_files)

	if args.year_data:
		max_temp, date = weather.calculate_max_temperature(args.year)
		print(max_temp, date)
		min_temp, date = weather.calculate_min_temperature()
		print(min_temp, date)	
		max_humidity, date = weather.calculate_max_humidity()
		print(max_humidity, date)	

	elif args.month_data:
		avg_max = weather.calculate_average_max_temperature(args.year, int(args.month))
		print(avg_max)
		avg_min = weather.calculate_average_min_temperature()
		print(avg_min)
		avg_humdity = weather.calculate_average_max_humidity()
		print(avg_humdity)

	elif args.month_split_bar:
		weather.calculate_daily_report(args.year, int(args.month), 3)

	elif args.month_bar:
		weather.calculate_daily_report(args.year, int(args.month), 4)

if __name__ == "__main__":
	main()
