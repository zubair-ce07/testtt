import os
import argparse
import calendar
import time

from weather_readings_reader import WeatherReadingsReader
from report_generator import ReportGenerator


class Main:
    directory_path = ''

    def validate_month(self, argument):
        required_date = time.strptime(argument, "%Y/%m")
        year = required_date.tm_year
        month = required_date.tm_mon
        month_name = calendar.month_abbr[month]
        weather_readings = WeatherReadingsReader.read_readings(Main.directory_path, year, month_name)
        if weather_readings:
            return weather_readings
        else:
            argparse.ArgumentTypeError(f"No Data found for argument {argument}")

    def validate_year(self, argument):
        required_date = time.strptime(argument, "%Y")
        year = required_date.tm_year
        weather_readings = WeatherReadingsReader.read_readings(Main.directory_path, year)
        if weather_readings:
            return weather_readings
        else:
            raise argparse.ArgumentTypeError(f"No Data found for {argument}")

    def validate_directory(self, path):
        if os.path.isdir(path):
            Main.directory_path = path
            return path
        raise argparse.ArgumentTypeError(f"Invalid directory path")

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Report will be generated according to the Arguments')
        parser.add_argument('directory', type=self.validate_directory, help='Enter the directory')
        parser.add_argument('-e', '--type_e', type=self.validate_year, help='Annual Report')
        parser.add_argument('-a', '--type_a', type=self.validate_month, help='Monthly Report year/month')
        parser.add_argument('-c', '--type_c', type=self.validate_month, help='Dual Bar Chart year/month')
        parser.add_argument('-d', '--type_d', type=self.validate_month, help='Single Bar Chart year/month')
        return parser.parse_args()

    def __init__(self):
        arguments = self.parse_arguments()
        if arguments.type_e:
            ReportGenerator.get_annual_report(arguments.type_e)
        if arguments.type_a:
            ReportGenerator.get_month_report(arguments.type_a)
        if arguments.type_c:
            ReportGenerator.dual_bar_chart_report(arguments.type_c)
        if arguments.type_d:
            ReportGenerator.single_bar_chart_report(arguments.type_d)


if __name__ == '__main__':
    Main()
