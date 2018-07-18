import os
import argparse
import calendar
import warnings

from weather_readings_reader import WeatherReadingsReader
from report_generator import ReportGenerator


class Main:

    my_path = ''

    def validate_month(self, argument):
        try:
            year, month = argument.split('/')
            if not int(year) or not int(month) in range(1, 13):
                raise argparse.ArgumentTypeError("Year should be an integer month should be an integer from 1-12")
            else:
                year, month = self.month_argument_reader(argument)
                month_name = calendar.month_abbr[month]
                weather_readings = WeatherReadingsReader.read_readings(Main.my_path, year, month_name)
                if weather_readings:
                    return weather_readings
                else:
                    argparse.ArgumentTypeError(f"No Data found for argument {argument}")
        except Exception:
            raise argparse.ArgumentTypeError("Argument Type Error. Enter in the form of int/int")

    def validate_year(self, argument):
        if int(argument):
            weather_readings = WeatherReadingsReader.read_readings(Main.my_path, argument)
            if weather_readings:
                return weather_readings
            else:
                raise argparse.ArgumentTypeError(f"No Data found for {argument}")
        else:
            raise argparse.ArgumentTypeError("Not a valid year")

    def validate_directory(self, path):
        if os.path.isdir(path):
            Main.my_path = path
            return path
        raise argparse.ArgumentTypeError(f"Invalid directory path")

    def month_argument_reader(self, argument):
        year, month = argument.split('/')
        return int(year), int(month)

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
