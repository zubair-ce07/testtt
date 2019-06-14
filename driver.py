import argparse

from argument_validator import ArgumentValidator
from weather_reporter import WeatherReporter


def read_cmd_arg():
    """
    reads cmd line args
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path",
                        help="the path of directory where files are allocated")
    parser.add_argument("-e", type=ArgumentValidator.validate_year,
                        help="specify year for required information")
    parser.add_argument("-c",
                        type=ArgumentValidator.validate_month_year,
                        help="specify month for required information")
    parser.add_argument("-a",
                        type=ArgumentValidator.validate_month_year,
                        help="specify month for required information")

    args = parser.parse_args()
    weather_reporter = WeatherReporter()
    if args.c:
        weather_reporter.generate_barchart_report(args.c, args.dir_path)
    if args.e:
        weather_reporter.generate_year_report(args.e, args.dir_path)
    if args.a:
        weather_reporter.generate_month_report(args.a, args.dir_path)


if __name__ == "__main__":
    read_cmd_arg()
