import datetime
import calendar
from populate_data import PopulateData
from result_calculation import CalculateResult
from weather_report import WeatherReport
import constants
import argparse


class WeatherMan:
    """class takes command line arguments and initiate computation accordingly"""
    def __init__(self, args):
        self.args = args

    # method to start computation on the basis of specified argument
    def start_computation(self):
        if self.args.year:
            year = self.args.year
            date = datetime.datetime.now()
            now_year = date.strftime("%Y")
            if year <= now_year:
                self.calculate_and_print_report(self.args.file_directory_path,
                                                constants.YEAR, year)
            else:
                print("you just entered invalid year")

        if self.args.month:
            data = str(self.args.month).split('/')
            year = data[0]
            imonth = int(data[1])
            if 0 < imonth and imonth < 13:
                month = calendar.month_abbr[imonth]
                self.calculate_and_print_report(self.args.file_directory_path,
                                                constants.MONTH, year, month)

        if self.args.monthchart:
            data = str(self.args.monthchart).split('/')
            year = data[0]
            imonth = int(data[1])
            if imonth > 0 and imonth < 13:
                month = calendar.month_abbr[imonth]
                self.calculate_and_print_report(self.args.file_directory_path,
                                                constants.MONTHCHART, year, month)

    # funtion to calculate and print report
    def calculate_and_print_report(self, file_directory, arg_type, year, month=""):
        data_populator = PopulateData(year=year, month=month, filedir_path=file_directory)
        data_populator.populate_data()
        if not data_populator.wheather_data.__len__():
            print("no record for month of this year exist you provide")
        else:
            result = CalculateResult(data_populator.wheather_data, arg_type)
            result.calculate()
            report = WeatherReport(result.result_record, arg_type, year, month)
            report.generate_report()
            report.print_report()
            print("\n")


# main method to take input from command line and parse and
# start compution throug weatherman
def main():
    parser = argparse.ArgumentParser(prog="Weatherman", description="")
    parser.add_argument("file_directory_path", type=str,
                        help="Path of the wheather file directory")
    parser.add_argument("-e", "--year", help="input year only e.g 2010")
    parser.add_argument("-a", "--month",
                        help="input year and month in format of year/month e.g 2014/8")
    parser.add_argument("-c", "--monthchart",
                        help="input year and month for chart in format of year/month e.g 2014/8")
    args = parser.parse_args()
    weatherman = WeatherMan(args)
    weatherman.start_computation()


if __name__ == "__main__":
    main()
