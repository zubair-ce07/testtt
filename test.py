import argparse
import sys
from datetime import datetime


def get_valid_year_range():
    return range(2004, 2017)


def valid_year(year):
    try:
        date = datetime.strptime(year, "%Y")
        if date.year in get_valid_year_range():
            return date
        else:
            msg="use a valid {}".format(get_valid_year_range())
            raise argparse.ArgumentTypeError(msg)
    except ValueError:
        msg = "Not a valid year: '{0}' (try format: YYYY).".format(year)
        raise argparse.ArgumentTypeError(msg)


def valid_month(month):
    try:
        date = datetime.strptime(month, "%Y/%m")
        if date.year in get_valid_year_range():
            return date
        else:
            raise argparse.ArgumentTypeError("use a valid {}".format(get_valid_year_range()))
    except ValueError:
        msg = "Not a valid date: '{0}' (try format: YYYY/MM).".format(month)
        raise argparse.ArgumentTypeError(msg)


def read_files(source, year, month):
    print('Error: Path is not correct: ')
    sys.exit(1)


parser = argparse.ArgumentParser()
parser.add_argument('source', help='Path to weather data files')
parser.add_argument('-e', '--extreme', type=valid_year,
                    help='Display extreme weather report for given year(format: YYYY)')
parser.add_argument('-a', '--average', type=valid_month,
                    help='Display average weather report for given month(format: YYYY/MM)')
parser.add_argument('-c', '--chart', type=valid_month,
                    help='Display char weather report for given month(format: YYYY/MM)')
# read_files()
args = parser.parse_args()
if not ( args.extreme or args.average or args.chart):
    print ("Give atleast one")

print(args)
