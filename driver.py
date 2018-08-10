import argparse
from weather_reporter import WeatherReporter
from argument_validator import ArgumentValidator


def read_cmd_arg():
    """
    reads cmd line args
    """
    arg_validator = ArgumentValidator()

    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path",
                        help="the path of directory where files are allocated",
                        default=1, nargs='?')
    parser.add_argument("-e", type=arg_validator.validate_arguments_year,
                        help="specify year for required information")
    parser.add_argument("-c",
                        type=arg_validator.validate_arguments_month_year,
                        help="specify month for required information")
    parser.add_argument("-a",
                        type=arg_validator.validate_arguments_month_year,
                        help="specify month for required information")

    args = parser.parse_args()
    arg_validator.check_number_arguments(args, parser)
    given_arg_list = []
    if args.e:
        given_arg_list.append('-e')
        given_arg_list.append(args.e)
    elif args.a:
        given_arg_list.append('-a')
        given_arg_list.append(args.a)
    elif args.c:
        given_arg_list.append('-c')
        given_arg_list.append(args.c)
    else:
        print("Invalid Arguments provided")
        exit()
    given_arg_list.append(args.dir_path)
    return given_arg_list


if __name__ == "__main__":
    weather_reporter_obj = WeatherReporter()
    given_arg_list = read_cmd_arg()
    report_type = given_arg_list[0]
    if report_type == '-e':
        weather_reporter_obj.genrate_year_report(given_arg_list)
    elif report_type == '-a':
        weather_reporter_obj.genrate_month_report(given_arg_list)
    elif report_type == '-c':
        weather_reporter_obj.genrate_barchart_report(given_arg_list)
    else:
        print("Invalid Argumnent")
        exit()
