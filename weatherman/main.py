""" Controller file """
import argparse
from datetime import datetime
from report_generator import ReportGenerator


TODAY = datetime.today()


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
    parser = argparse.ArgumentParser(
                                        description=detail_str
                                    )
    parser.add_argument("path",
                        help="path to the dir that conatain weatherfiles.")
    parser.add_argument("-e",
                        help=("display year report: Max temp, Min " +
                              "temp, Humidity"))
    parser.add_argument("-d",
                        help=("display year graph of highest " +
                              "and lowest temperature."))
    parser.add_argument("-a", type=validate_date,
                        help="display month average report")
    parser.add_argument("-c", type=validate_date,
                        help=("display month graph of highest " +
                              "and lowest temperature."))
    return parser


def controller(args):
    report_generator = ReportGenerator()
    if args.e:
        report_generator.year_controller(args.path, args.e, False)
    if args.d:
        report_generator.year_controller(args.path, args.d, True)
    if args.a:
        report_generator.month_controller(args.path, args.a, False)
    if args.c:
        report_generator.month_controller(args.path, args.c, True)


if __name__ == '__main__':
    parser = prepare_parser()
    args = parser.parse_args()
    controller(args)
