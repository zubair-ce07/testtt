""" Controller file """
import argparse
from year_reports import display_year_report
from month_reports import display_month_report


PARSER = argparse.ArgumentParser(description="Weatherman: to generate different reports")
PARSER.add_argument("path",
                    help="path to the dir that conatain weatherfiles.")
PARSER.add_argument("-e", dest="year_false",
                    help="display year report: Max temp, Min temp, Humidity")
PARSER.add_argument("-d", dest="year_true",
                    help="display year graph of highest and lowest temperature.")
PARSER.add_argument("-a", dest="month_false",
                    help="display month average report")
PARSER.add_argument("-c", dest="month_true",
                    help="display month graph of highest and lowest temperature.")

ARGS = PARSER.parse_args()
if ARGS.year_false:
    display_year_report(ARGS.path, ARGS.year_false, False)
if ARGS.year_true:
    display_year_report(ARGS.path, ARGS.year_true, True)
if ARGS.month_false:
    display_month_report(ARGS.path, ARGS.month_false, False)
if ARGS.month_true:
    display_month_report(ARGS.path, ARGS.month_true, True)
