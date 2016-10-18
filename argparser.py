import argparse
import sys


# This is an ordered list please do not change order of elements
MONTHS=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', \
        'Nov', 'Dec']


class ArgParser(argparse.ArgumentParser):

    path = ""
    exts = []
    avgs = []
    charts = []

    def __init__(self):
        super(ArgParser, self).__init__(description="A utility to process"
                                            " weather data")

        self.add_argument("dir_path", nargs="?", default="",
                          metavar="DIRECTORY PATH", help="Directory path for "
                          "weather data files")
        self.add_argument("-e", required=False, metavar="YYYY",
                          action="append", help="Gets extreme weather stats "
                          "for given year")
        self.add_argument("-a", required=False, metavar="YYYY/MM",
                          action="append", help="Gets average temperature "
                          "stats for given month")
        self.add_argument("-c", required=False, metavar="YYYY/MM",
                          action="append", help="Bar chart "
                          "representation of extereme weather for the "
                          "given month")

    def get_args(self):
       return (self.path, self.exts, self.avgs, self.charts)

    def process_args(self):
       args = self.parse_args()

       if len(sys.argv) == 2 and args.dir_path:
           self.print_help()
           sys.exit(1)
       elif len(sys.argv) < 2:
           self.print_help()
           sys.exit(1)

       if args.dir_path:
           self.path = args.dir_path.strip("/\\")

       if args.e:
           # Remove duplicate years overhead
           years = set(args.e)
           for year in years:
               self.validate_year(year)
               self.exts.append(year)

       if args.a:
           # Remove duplicate months overhead
           months = set(args.a)
           for month in months:
               self.avgs.append(self.parse_month(month))

       if args.c:
           # Remove duplicate months overhead
           months = set(args.c)
           for month in args.c:
               self.avgs.append(self.parse_month(month))

    def parse_month(self, month):
        date = month.split("/")
        if len(date) != 2:
            raise Exception("(%s) Invalid month format. Please follow: YYYY/MM" % month)

        self.validate_year(date[0])
        month  = self.validate_month(date[1])
        return date[0] + '_' + MONTHS[month-1]
        

    def validate_year(self, year):
        try:
            year = int(year)
        except:
            raise

        if year < 0:
            raise Exception("Year cannot be negative value")

        return year

    def validate_month(self, month):
        try:
            month = int(month)
        except:
            raise

        if month < 1 or month > 12:
            raise Exception("(%d) Month out of valid range: [1, 12]" % month)

        return month
