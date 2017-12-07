import sys
import argparse

from Reports.yearlyreport import YearlyReport
from Reports.monthlyreport import MonthlyReport
from Reports.monthlybarreport import MonthlyBarReport
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

        if len(sys.argv) < 2:
            print("Incomplete arguments")
            return

        for report_year in arg_list.e:

            if len(report_year.split('/')) != 1:
                print("Argument " + report_year + " is invalid for option -e.")

            weather = parser.parse(path, report_year)
            if(weather is not None):
                report = YearlyReport()
                report.print(weather)

        for report_month in arg_list.a:

            if len(report_month.split('/')) != 2:
                print("Argument " + report_month + " is invalid for option -a.")
                continue

            year = report_month.split('/')[0]
            month = report_month.split('/')[1]
            weather = parser.parse(path, year, int(month))
            if (weather is not None):
                report = MonthlyReport()
                report.print(weather)

        for report_month in arg_list.c:

            if len(report_month.split('/')) != 2:
                print("Argument " + report_month + " is invalid for option -c.")
                continue

            year = report_month.split('/')[0]
            month = report_month.split('/')[1]
            weather = parser.parse(path, year, int(month))

            if (weather is not None):
                report = MonthlyBarReport()
                report.print(weather, year)

        return

if __name__ == "__main__":
    WeatherMan.main()

