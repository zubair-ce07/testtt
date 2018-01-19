import datetime
import calendar
import populatedata
import calculationresult
import weatherreport
import constants
import argparse


class Weatherman:
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
            try:
                data = str(self.args.month).split('/')
                year = data[0]
                imonth = int(data[1])
                if imonth > 0 and imonth < 13:
                    month = calendar.month_abbr[imonth]
                    self.calculate_and_print_report(self.args.file_directory_path,
                                                    constants.MONTH, year, month)
            except:
                print("you enter some invalid value")

        if self.args.monthchart:
            try:
                data = str(self.args.monthchart).split('/')
                year = data[0]
                imonth = int(data[1])
                if imonth > 0 and imonth < 13:
                    month = calendar.month_abbr[imonth]
                    self.calculate_and_print_report(self.args.file_directory_path,
                                                    constants.MONTHCHART, year, month)
            except Exception as ex:
                print("you enter some invalid value or an exception occured")

    # funtion to calculate and print report
    def calculate_and_print_report(self, file_directory, arg_type,year, month=""):
        try:
            obj = populatedata.Populatedata(year=year, month=month, filedir_path=file_directory)
            obj.populatedata()
            if not obj.datalist.__len__():
                print("no record for month of this year exist you provide")
            else:
                rslt = calculationresult.Calculateresult(obj.datalist, arg_type)
                rslt.calculate()
                report = weatherreport.Weathereport(rslt.resultdict, arg_type, year, month)
                report.generate_report()
                report.print_report()
                print("\n")
        except Exception as ex:
            print("you may just enter invalid data or exception occurs")


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
    weatherman = Weatherman(args)
    weatherman.start_computation()


if __name__ == "__main__":
    main()
