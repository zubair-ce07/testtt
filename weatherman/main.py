""" Controller file """
import argparse
from datetime import datetime
import weatherman


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
    """take actions on the bases of arguments """
    file_handler = weatherman.FileHandler(args.path)
    if args.e:
        file_names = file_handler.get_file_names(args.e, None)
        list = file_handler.get_list(file_names)
        weatherman.display_extremes(list, True)
    if args.d:
        weatherman.generate_graph(args.d, None, file_handler)
    if args.a:
        [year, month] = args.a.split('/')
        file_names = file_handler.get_file_names(year, month)
        list = file_handler.get_list(file_names)
        weatherman.display_extremes(list, False)
    if args.c:
        [year, month] = args.c.split('/')
        weatherman.generate_graph(year, month, file_handler)


if __name__ == '__main__':
    parser = prepare_parser()
    args = parser.parse_args()
    controller(args)
