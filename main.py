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


def generate_weather_reports(commandline_arguments):
    weather_reporter = WeatherReporter()
    if commandline_arguments.c:
        weather_reporter.generate_bar_chart_report(commandline_arguments.c.year,
                                                   commandline_arguments.c.month,
                                                   commandline_arguments.dir_path)
    if commandline_arguments.e:
        weather_reporter.generate_annual_report(commandline_arguments.e,
                                                commandline_arguments.dir_path)
    if commandline_arguments.a:
        weather_reporter.generate_monthly_report(commandline_arguments.a.year,
                                                 commandline_arguments.a.month,
                                                 commandline_arguments.dir_path)


if __name__ == "__main__":
    commandline_arguments = parse_cmd_arguments()
    generate_weather_reports(commandline_arguments)
