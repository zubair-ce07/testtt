import sys
import argparse
import datetime

from Reports.report import Report
from Parsers.weatherparser import WeatherParser


class WeatherMan:

    @staticmethod
    def main():

        arg_parser = argparse.ArgumentParser(description='Create Reports')
        arg_parser.add_argument("path", help="path to files")
        arg_parser.add_argument('-e', metavar='N', nargs='+',
                                help='Print Yearly Report for given year')
        arg_parser.add_argument('-a', metavar='N', nargs='+',
                                help='Print Monthly Report for given month')
        arg_parser.add_argument('-c', metavar='N', nargs='+',
                                help='Print Monthly Bar Report for given year')
        arg_list = arg_parser.parse_args()

        parser = WeatherParser()
        report = Report()

        if len(sys.argv) < 2:
            print("Incomplete arguments")
            return

        for report_year in arg_list.e:

            if len(report_year.split('/')) != 1:
                print(f"Argument {report_year} is invalid for option -e.")
            date = datetime.datetime.strptime(report_year, '%Y').date()
            weather = parser.parse(arg_list.path, date, True)
            if(weather is not None):
                report.print_yearly(weather)

        for report_month in arg_list.a:

            if len(report_month.split('/')) != 2:
                print(f"Argument {report_month} is invalid for option -a.")
                continue
            date = datetime.datetime.strptime(report_month, '%Y/%m').date()
            weather = parser.parse(arg_list.path, date)
            if (weather is not None):
                report.print_monthly(weather)

        for report_month in arg_list.c:

            if len(report_month.split('/')) != 2:
                print(f"Argument {report_month} is invalid for option -c.")
                continue
            date = datetime.datetime.strptime(report_month, '%Y/%m').date()
            weather = parser.parse(arg_list.path, date)

            if (weather is not None):
                report.print_monthly_bar_graph(weather, date.year)

        return

if __name__ == "__main__":
    WeatherMan.main()

