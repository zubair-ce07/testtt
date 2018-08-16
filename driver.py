import argparse
from weather_reporter import WeatherReporter
from argument_validator import ArgumentValidator


def read_cmd_arg():
    """
    reads cmd line args
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path",
                        help="the path of directory where files are allocated",
                        default=1, nargs='?')
    parser.add_argument("-e", type=ArgumentValidator.validate_arguments_year,
                        help="specify year for required information")
    parser.add_argument("-c",
                        type=ArgumentValidator.validate_arguments_month_year,
                        help="specify month for required information")
    parser.add_argument("-a",
                        type=ArgumentValidator.validate_arguments_month_year,
                        help="specify month for required information")

    args = parser.parse_args()
    ArgumentValidator.check_number_arguments(args, parser)
    arg_type = ""
    arg_input = ""
    if args.e:
        arg_type = '-e'
        arg_input = args.e
    elif args.a:
        arg_type = '-a'
        arg_input = args.a
    elif args.c:
        arg_type = '-c'
        arg_input = args.c
    else:
        print("Invalid Arguments provided")
        exit()
    return arg_type, arg_input, args.dir_path

if __name__ == "__main__":
    weather_reporter_obj = WeatherReporter()
    report_type, report_year, dir_path  = read_cmd_arg()
    if report_type == '-e':
        weather_reporter_obj.generate_year_report(report_year, dir_path)
    elif report_type == '-a':
        weather_reporter_obj.generate_month_report(report_year, dir_path)
    elif report_type == '-c':
        weather_reporter_obj.generate_barchart_report(report_year, dir_path)
    else:
        print("Invalid Argumnent")
        exit()
