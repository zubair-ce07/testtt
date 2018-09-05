""" Controller file """
import argparse
from datetime import datetime
import weatherman
from file_handler import FileHandler


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
                        help=("display year report the max temperature, min "
                              "temperature and most humid day and humidity"))
    parser.add_argument("-a", type=validate_date,
                        help="display month average report the average max "
                             "temperature, average min temperature and "
                             "average mean humidity.")
    parser.add_argument("-c", type=validate_date,
                        help=("display month two line graph of highest " +
                              "and lowest temperature of each day."))
    parser.add_argument("-d", type=validate_date,
                        help=("display month oneline graph of highest " +
                              "and lowest temperature of each day."))
    return parser


def controller(args):
    """take actions on the bases of arguments """
    file_handler = FileHandler(args.path)
    if args.e:
        file_names = file_handler.get_file_names(args.e, None)
        list = file_handler.get_list(file_names)
        weatherman.display_extremes(list, args.e)
    if args.d:
        [year, month] = args.c.split('/')
        weatherman.generate_graph(year, month, file_handler, True)
    if args.a:
        [year, month] = args.a.split('/')
        file_names = file_handler.get_file_names(year, month)
        list = file_handler.get_list(file_names)
        weatherman.display_extremes(list, False)
    if args.c:
        [year, month] = args.c.split('/')
        weatherman.generate_graph(year, month, file_handler, False)


if __name__ == '__main__':
    parser = prepare_parser()
    args = parser.parse_args()
    controller(args)
