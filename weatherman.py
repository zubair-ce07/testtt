from weather_reader import WeatherReader
from weather_reader_calculator import WeatherReaderCalculator
from generate_report import GenerateReport
import argparse
	
def main():
	
	parser = argparse.ArgumentParser()
	parser.add_argument("path")
	parser.add_argument("-e" , "--yearreport", help="year" , type=int)
	parser.add_argument("-a" ,"--monthreport", help="year/month")
	parser.add_argument("-c" , "--monthchart", help="year/month")
	

	args = parser.parse_args()

	weather_report = WeatherReader()
	weather_report_calculator = WeatherReaderCalculator()
	final_report = GenerateReport()
	is_valid = 0

	if args.yearreport:

		is_valid = weather_report.parse_files(args.yearreport,args.path)

		if is_valid == 1:
			weather_report_calculator.compute_year_report(weather_report.weather_reading_list)
			final_report.generate_report_year(weather_report_calculator.calculated_result)

	elif args.monthreport:
		try:
			year , month = args.monthreport.split("/")
		except:
			parser.print_help()
			return
		
		is_valid = weather_report.parse_files(year,args.path,month)
		
		if is_valid == 1:
			weather_report_calculator.compute_month_report(weather_report.weather_reading_list)
			final_report.generate_report_month(weather_report_calculator.calculated_result)

	elif args.monthchart:
		try:
			year , month = args.monthchart.split("/")
		except:
			parser.print_help()
			return
		
		is_valid = weather_report.parse_files(year,args.path,month)
		
		if is_valid == 1:
			weather_report_calculator.compute_barchart_report(weather_report.weather_reading_list)
			final_report.generate_bar_chart(weather_report_calculator.calculated_result,0)
			print("\n")
			final_report.generate_bar_chart(weather_report_calculator.calculated_result,1)


if __name__== "__main__":
  main()