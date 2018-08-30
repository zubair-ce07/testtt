""" Controller file """
import argparse
from datetime import datetime
from year_reports import display_year_report
from month_reports import display_month_report


TODAY = datetime.today()


def validate_year(year):
    """ function to validate year string """
    if year and year.isdigit():
        if int(year) <= int(TODAY.year) and int(year) >= 1990:
            return year
    print(f"Invalid option [Required year in range (1990, {str(TODAY.year)})]")
    return False


def validate_date(date):
    """ function to validate year/month string """
    try:
        if date != datetime.strptime(date, "%Y/%m").strftime('%Y/%m'):
            raise ValueError
        return date
    except ValueError:
        print("Invalid option [Required year/month ie 2011/05]")
        return False


PARSER = argparse.ArgumentParser(description=(
    "Weatherman: to generate different reports"))

PARSER.add_argument("path",
                    help="path to the dir that conatain weatherfiles.")

PARSER.add_argument("-e", type=validate_year,
                    help="display year report: Max temp, Min temp, Humidity")
PARSER.add_argument("-d", type=validate_year,
                    help=("display year graph of highest " +
                          "and lowest temperature."))
PARSER.add_argument("-a", type=validate_date,
                    help="display month average report")
PARSER.add_argument("-c", type=validate_date,
                    help=("display month graph of highest " +
                          "and lowest temperature."))

ARGS = PARSER.parse_args()

if ARGS.e is not None and ARGS.e is not False:
    print(display_year_report(ARGS.path, ARGS.e, False))
if ARGS.d is not None and ARGS.d is not False:
    print(display_year_report(ARGS.path, ARGS.d, True))
if ARGS.a is not None and ARGS.a is not False:
    print(display_month_report(ARGS.path, ARGS.a, False))
if ARGS.c is not None and ARGS.c is not False:
    print(display_month_report(ARGS.path, ARGS.c, True))
