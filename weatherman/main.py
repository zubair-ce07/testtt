""" Controller file """
import argparse
from datetime import datetime
from report_generator import ReportGenerator


TODAY = datetime.today()


def validate_year(year):
    """ function to validate year (year < current year) string """
    if year and year.isdigit():
        if int(year) <= int(TODAY.year):
            return year
    print(f"\nInvalid option [Required year < {str(TODAY.year)})]\n")
    return False


def validate_date(date):
    """ function to validate year/month string """
    try:
        if date != datetime.strptime(date, "%Y/%m").strftime('%Y/%m'):
            raise ValueError
        return date
    except ValueError:
        print("\nInvalid option [Required year/month ie 2011/05]\n")
        return False


def prepare_parser():
    detail_str = "Weatherman: to generate different reports"
    PARSER = argparse.ArgumentParser(
                                        description=detail_str
                                    )
    PARSER.add_argument("path",
                        help="path to the dir that conatain weatherfiles.")
    PARSER.add_argument("-e", type=validate_year,
                        help=("display year report: Max temp, Min " +
                              "temp, Humidity"))
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
    report_generator = ReportGenerator()
    if ARGS.e:
        report_generator.year_controller(ARGS.path, ARGS.e, False)
    if ARGS.d:
        report_generator.year_controller(ARGS.path, ARGS.d, True)
    if ARGS.a:
        report_generator.month_controller(ARGS.path, ARGS.a, False)
    if ARGS.c:
        report_generator.month_controller(ARGS.path, ARGS.c, True)


if __name__ == '__main__':
    parser = prepare_parser()
    ARGS = parser.parse_args()
    controller(ARGS)
