import argparse

from parser import WeatherParser
from analyzer import WeatherAnalyzer
from reporter import WeatherReporter


class WeatherMan:
    """Parses, analyzes and reports weather information"""

    def __init__(self):
        self.parser = WeatherParser()
        self.analyzer = WeatherAnalyzer()
        self.reporter = WeatherReporter()

    def get_yearly_reports(self, readings_dir, year):
        """Report the hottest, coldest and the most humid day in a year"""
        readings = self.parser.parse_weather_files(readings_dir, year)
        hottest_day = self.analyzer.get_max_reading(readings, "max_temperature")
        coldest_day = self.analyzer.get_min_reading(readings, "min_temperature")
        most_humid_day = self.analyzer.get_max_reading(readings, "max_humidity")
        self.reporter.report_year_extremes(hottest_day, coldest_day, most_humid_day)

    def get_monthly_reports(self, readings_dir, year, month):
        """
            Report the average highest temperature, average lowest temperature
            and average mean humidity for a month
        """
        readings = self.parser.parse_weather_files(readings_dir, year, month)
        avg_max_temp = self.analyzer.get_avg_of_attributes(readings, "max_temperature")
        avg_min_temp = self.analyzer.get_avg_of_attributes(readings, "min_temperature")
        avg_humidity = self.analyzer.get_avg_of_attributes(readings, "mean_humidity")
        self.reporter.report_month_avgs(avg_max_temp, avg_min_temp, avg_humidity)

    def get_monthly_bar_charts(self, readings_dir, year, month, single_line=False):
        """Print bar charts for the highest and lowest temperatures in a month"""
        readings = self.parser.parse_weather_files(readings_dir, year, month)
        max_temps = self.analyzer.extract_attributes(readings, "max_temperature")
        min_temps = self.analyzer.extract_attributes(readings, "min_temperature")
        self.reporter.report_month_temps(max_temps, min_temps, single_line)


def parse_year(year):
    """Year parser to use with argument parser"""
    if year.isdigit():
        return int(year)
    else:
        message = f"{year} is not a valid year."
        raise argparse.ArgumentTypeError(message)


def parse_month(year_month):
    """Month parser to use with argument parser"""

    if year_month[-3] != "/" and year_month[-2] != "/":
        message = "Please pass month with year in the format YYYY/MM e.g. 2005/6"
        raise argparse.ArgumentTypeError(message)

    year, month = year_month.split("/")
    year = parse_year(year)

    if month.isdigit():
        month = int(month)
    else:
        message = f"{month} is not a valid month."
        raise argparse.ArgumentTypeError(message)

    return [year, month]


if __name__ == "__main__":
    """Parse the arguments passed to the program"""

    arg_parser = argparse.ArgumentParser(
        description="Program to parse, analyze and report weather readings")
    arg_parser.add_argument(
        "readings_dir", help="Path to weather readings directory")
    arg_parser.add_argument(
        "-e", type=parse_year, help="Display the highest temperature and day,\
             lowest temperature and day, most humid day and humidity for a\
                  given year (e.g. 2002)")
    arg_parser.add_argument(
        "-a", type=parse_month, help="Display the average highest temperature,\
             average lowest temperature, average mean humidity for a given\
                  month (e.g. 2005/6)")
    arg_parser.add_argument(
        "-c", type=parse_month, help="Draw two horizontal bar charts on the \
            console for the highest and lowest temperature on each day.\
                 Highest in red and lowest in blue for a given month")
    arg_parser.add_argument(
        "-o", type=parse_month, help="Draw one horizontal bar chart on the console\
             for the highest and lowest temperature on each day. Highest in red\
                  and lowest in blue for a given month")

    args = arg_parser.parse_args()

    weather_man = WeatherMan()

    if args.e:
        weather_man.get_yearly_reports(args.readings_dir, args.e)

    if args.a:
        weather_man.get_monthly_reports(args.readings_dir,args.a[0], args.a[1])

    if args.c:
        weather_man.get_monthly_bar_charts(args.readings_dir, args.c[0], args.c[1])

    if args.o:
        weather_man.get_monthly_bar_charts(args.readings_dir, args.o[0], args.o[1], True)
