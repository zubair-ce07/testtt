import sys
import os
import glob

from parser import WeatherParser
from analyzer import WeatherAnalyzer
from reporter import WeatherReporter


program_name = sys.argv[0]

help_message = """Usage: {} 
           -e Display the highest temperature and day, lowest temperature and day, most humid day and humidity for a given year (e.g. 2002).
           -a Display the average highest temperature, average lowest temperature, average mean humidity for a given month (e.g. 2005/6).
           -c Draw two horizontal bar charts on the console for the highest and lowest temperature on each day. Highest in red and lowest in blue for a given month.
           -o Draw one horizontal bar chart on the console for the highest and lowest temperature on each day. Highest in red and lowest in blue for a given month.""".format(program_name)

if len(sys.argv) < 2:
    print("{}: Please pass path to weather readings directory".format(program_name))
    exit(1)
elif not os.path.exists(sys.argv[1]):
    print("{}: Weather readings directory path is invalid".format(program_name))
    exit(1)
elif len(sys.argv) < 3:
    print(help_message)
    exit(1)

parser = WeatherParser()
readings = []
readings_dir = sys.argv[1]
file_paths = glob.glob(readings_dir + "/*.csv")
for file_path in file_paths:
    readings = readings + parser.parse_weather_file(file_path)

analyzer = WeatherAnalyzer()
reporter = WeatherReporter()

def get_yearly_reports(readings, year):
    """Report the hottest, coldest and the most humid day in a year"""
    hottest = analyzer.get_max_temperature_year(readings, year)
    coldest = analyzer.get_min_temperature_year(readings, year)
    most_humid = analyzer.get_max_humidity_year(readings, year)
    reporter.report_year_extremes(hottest, coldest, most_humid)


def get_monthly_reports(readings, year, month):
    """Report the average highest temperature, average lowest temperature and average mean humidity for a month"""
    avg_hottest = analyzer.get_avg_max_temperature_month(readings, year, month)
    avg_coldest = analyzer.get_avg_min_temperature_month(readings, year, month)
    avg_humidity = analyzer.get_avg_mean_humidity_month(readings, year, month)
    reporter.report_month_averages(avg_hottest, avg_coldest, avg_humidity)


def get_monthly_bar_charts(readings, year, month):
    """Print bar charts for the highest and lowest temperatures in a month"""
    max_temperatures = analyzer.get_max_temperatures_month(
        readings, year, month)
    min_temperatures = analyzer.get_min_temperatures_month(
        readings, year, month)
    reporter.report_month_temperatures(max_temperatures, min_temperatures)


def get_monthly_single_bar_chart(readings, year, month):
    """Print single lined bar charts for the highest and lowest temperatures in a month"""
    max_temperatures = analyzer.get_max_temperatures_month(
        readings, year, month)
    min_temperatures = analyzer.get_min_temperatures_month(
        readings, year, month)
    reporter.report_month_temperatures(
        max_temperatures, min_temperatures, True)


if __name__ == "__main__":
    """Parse the arguments passed to the program"""
    arguments = sys.argv[2:]
    i = 0
    while i < len(arguments):
        if arguments[i] == "-e":
            try:
                year = arguments[i+1]
                year = int(year)
            except IndexError:
                print("Please pass year with argument -e e.g. 2002")
                exit(1)
            except ValueError:
                print("-e argument only accepts year e.g. 2002")
                exit(1)
            get_yearly_reports(readings, year)
        elif arguments[i] == "-a":
            try:
                year, month = arguments[i+1].split("/")
            except IndexError:
                print("Please pass year and month with argument -a e.g. 2005/6")
                exit(1)
            except ValueError:
                print("Please pass month with year with argument -e .g. 2005/6")
                exit(1)
            get_monthly_reports(readings, int(year), int(month))
        elif arguments[i] == "-c":
            try:
                year, month = arguments[i+1].split("/")
            except IndexError:
                print("Please pass year and month with argument -c e.g. 2005/6")
                exit(1)
            except ValueError:
                print("Please pass month with year with argument -c e.g. 2005/6")
                exit(1)
            get_monthly_bar_charts(readings, int(year), int(month))
        elif arguments[i] == "-o":
            try:
                year, month = arguments[i+1].split("/")
            except IndexError:
                print("Please pass year and month with argument -o e.g. 2005/6")
                exit(1)
            except ValueError:
                print("Please pass month with year with argument -o e.g. 2005/6")
                exit(1)
            get_monthly_single_bar_chart(readings, int(year), int(month))
        i = i + 2
