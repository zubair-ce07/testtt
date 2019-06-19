import argparse

from argument_validator import ArgumentValidator
from weather_reporter import WeatherReporter


def parse_cmd_arguments():
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

    return parser.parse_args()


def generate_weather_reports(cli_args):
    weather_reporter = WeatherReporter()
    if cli_args.c:
        weather_reporter.generate_bar_chart(cli_args.c.year, cli_args.c.month, cli_args.dir_path)
    if cli_args.e:
        weather_reporter.generate_annual_report(cli_args.e, cli_args.dir_path)
    if cli_args.a:
        weather_reporter.generate_monthly_report(cli_args.a.year, cli_args.a.month, cli_args.dir_path)


if __name__ == "__main__":
    commandline_arguments = parse_cmd_arguments()
    generate_weather_reports(commandline_arguments)
