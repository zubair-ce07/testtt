from weather_files_parser import WeatherFilesParser
from weather_readings_calculator import WeatherReadingsCalculator
from weather_results_report_generator import WeatherResultReportGenerator
import sys


def main():
    """
    command and argument given to calculator
    then initializing report generator and printing report
    sys.argv[1] is path if directory
    sys.argv[2:] is list of arguments
    :return:
    """
    try:
        weather_files_parser = WeatherFilesParser(sys.argv[1])
        weather_files_parser.read()

        WeatherReadingsCalculator(sys.argv[2:])
        weather_report_generator = WeatherResultReportGenerator()
        weather_report_generator.print_report()

    except IndexError as ie:
        print(f'Arguments have not passed or maybe {str(ie).upper()}')


if __name__ == "__main__":
    main()
