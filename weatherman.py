from weather_files_parser import WeatherFilesParser
from weather_readings_calculator import WeatherReadingsCalculator
from weather_results_report_generator import WeatherResultReportGenerator
import sys


def main():
    try:
        parser = WeatherFilesParser(sys.argv[1])
        parser.read()
        # command and argument given to calculator
        WeatherReadingsCalculator(sys.argv[2:])
        # initializing report generator and print report
        # calculated by Calculator
        report_generator = WeatherResultReportGenerator()
        report_generator.print_report()
    except IndexError as ie:
        print('Arguments have not passed or maybe {0}'.format(str(ie).upper()))


if __name__ == "__main__":
    main()
