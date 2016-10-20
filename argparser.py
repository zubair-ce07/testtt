import constants as const
import common as wc

import argparse
import sys


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

       if len(sys.argv) < 2 or (len(sys.argv) == 2 and args.dir_path):
           self.print_help()
           sys.exit(1)

       if args.dir_path:
           # TODO(shahbaz): Windows use forward
           # slash for for path definitions which
           # is not supported here
           self.path = args.dir_path.strip("/")

       if args.e:
           # Remove duplicate input years
           # to avoid overhead
           years = set(args.e)
           for year in years:
               wc.validate_year(year)
               self.exts.append(year)

       if args.a:
           # Remove duplicate input months
           # to avoid overhead
           months = set(args.a)
           for month in months:
               self.avgs.append(wc.parse_month(month))

       if args.c:
           # Remove duplicate input months
           # to avoid overhead
           months = set(args.c)
           for month in args.c:
               self.charts.append(wc.parse_month(month))
