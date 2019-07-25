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
        hottest_day = self.analyzer.get_maximum_reading(
            readings, 'max_temperature')
        coldest_day = self.analyzer.get_minimum_reading(
            readings, 'min_temperature')
        most_humid_day = self.analyzer.get_maximum_reading(
            readings, 'max_humidity')
        self.reporter.report_year_extremes(
            hottest_day, coldest_day, most_humid_day)

    def get_monthly_reports(self, readings_dir, year, month):
        """
            Report the average highest temperature, average lowest temperature
            and average mean humidity for a month
        """

        readings = self.parser.parse_weather_files(readings_dir, year, month)
        avg_hottest_temperature = self.analyzer.get_average_of_attributes(
            readings, 'max_temperature')
        avg_coldest_temperature = self.analyzer.get_average_of_attributes(
            readings, 'min_temperature')
        avg_humidity = self.analyzer.get_average_of_attributes(
            readings, 'mean_humidity')
        self.reporter.report_month_averages(
            avg_hottest_temperature, avg_coldest_temperature, avg_humidity)

    def get_monthly_bar_charts(self, readings_dir, year, month, single_line=False):
        """Print bar charts for the highest and lowest temperatures in a month"""
        readings = self.parser.parse_weather_files(readings_dir, year, month)
        max_temperatures = self.analyzer.get_attribute_list(
            readings, "max_temperature")
        min_temperatures = self.analyzer.get_attribute_list(
            readings, "min_temperature")
        self.reporter.report_month_temperatures(
            max_temperatures, min_temperatures, single_line)


def parse_year(year):
    """Year parser to use with argument parser"""
    if year.isdigit():
        return int(year)
    else:
        message = f"{year} is not a valid year."
        raise argparse.ArgumentTypeError(message)


def parse_month(month):
    """Month parser to use with argument parser"""

    if month[-3] != "/" and month[-2] != "/":
        message = "Please pass month with year in the format YYYY/MM e.g. 2005/6"
        raise argparse.ArgumentTypeError(message)

    year, month = month.split("/")
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
        'readings_dir', help="Path to weather readings directory")
    arg_parser.add_argument(
        '-e', type=parse_year, help="Display the highest temperature and day,\
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

    arguments = arg_parser.parse_args()

    weather_man = WeatherMan()

    if arguments.e:
        weather_man.get_yearly_reports(arguments.readings_dir, arguments.e)

    if arguments.a:
        weather_man.get_monthly_reports(arguments.readings_dir,
                                        arguments.a[0], arguments.a[1])

    if arguments.c:
        weather_man.get_monthly_bar_charts(arguments.readings_dir,
                                           arguments.c[0], arguments.c[1])

    if arguments.o:
        weather_man.get_monthly_bar_charts(arguments.readings_dir,
                                           arguments.o[0], arguments.o[1], True)
