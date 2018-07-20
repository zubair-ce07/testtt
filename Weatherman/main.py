import os
import argparse
import calendar
import time

from weather_readings_reader import WeatherReadingsReader
from report_generator import ReportGenerator


class Main:
    my_path = ''

    def validate_month(self, argument):
        required_date = time.strptime(argument, "%Y/%m")
        year = required_date.tm_year
        month = required_date.tm_mon
        month_name = calendar.month_abbr[month]
        weather_readings = WeatherReadingsReader.read_readings(Main.my_path, year, month_name)
        if weather_readings:
            return weather_readings
        else:
            argparse.ArgumentTypeError(f"No Data found for argument {argument}")

    def validate_year(self, argument):
        required_date = time.strptime(argument, "%Y")
        year = required_date.tm_year
        weather_readings = WeatherReadingsReader.read_readings(Main.my_path, year)
        if weather_readings:
            return weather_readings
        else:
            raise argparse.ArgumentTypeError(f"No Data found for {argument}")

    def validate_directory(self, path):
        if os.path.isdir(path):
            Main.my_path = path
            return path
        raise argparse.ArgumentTypeError(f"Invalid directory path")

    def run(self, args):
        if args.type_e:
            ReportGenerator.get_annual_report(args.type_e)
        if args.type_a:
            ReportGenerator.get_month_report(args.type_a)
        if args.type_c:
            ReportGenerator.dual_bar_chart_report(args.type_c)
        if args.type_d:
            ReportGenerator.single_bar_chart_report(args.type_d)

    def main(self):
        parser = argparse.ArgumentParser(description='Report will be generated according to the Arguments')
        parser.add_argument('directory', type=self.validate_directory, help='Enter the directory')
        parser.add_argument('-e', '--type_e', type=self.validate_year, help='Annual Report')
        parser.add_argument('-a', '--type_a', type=self.validate_month, help='Monthly Report year/month')
        parser.add_argument('-c', '--type_c', type=self.validate_month, help='Dual Bar Chart year/month')
        parser.add_argument('-d', '--type_d', type=self.validate_month, help='Single Bar Chart year/month')
        args = parser.parse_args()
        self.run(args)


if __name__ == '__main__':
    Main.main(Main())
