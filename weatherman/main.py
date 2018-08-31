""" Controller file """
import argparse
from datetime import datetime
#from year_reports import display_year_report
from month_report import MonthReportGenerator
from year_report import YearReportGenerator


TODAY = datetime.today()


def validate_year(year):
    """ function to validate year string """
    if year and year.isdigit():
        if int(year) <= int(TODAY.year):
            return year
    print(f"Invalid option [Required year < {str(TODAY.year)})]")
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


def prepare_parser():
    PARSER = argparse.ArgumentParser(
                                        description=("Weatherman: to generate different reports")
                                    )
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
    return PARSER

def controller(ARGS):
    if ARGS.e:
        year_report = YearReportGenerator()
        year_report.year_controller(ARGS.path, ARGS.e, False)
    if ARGS.d:
        year_report = YearReportGenerator()
        year_report.year_controller(ARGS.path, ARGS.d, True)
    if ARGS.a:
        month_report = MonthReportGenerator()
        month_report.month_controller(ARGS.path, ARGS.a, False)
    if ARGS.c:
        month_report = MonthReportGenerator()
        month_report.month_controller(ARGS.path, ARGS.c, True)


if __name__ == '__main__':
    parser = prepare_parser()
    ARGS = parser.parse_args()
    controller(ARGS)


    
