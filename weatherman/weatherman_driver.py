import argparse
from weather_reporter import WeatherReporter
from argument_validator import ArgumentValidator


class WeathermanDriver:

    def __init__(self):
        self.weather_reporter = WeatherReporter()
        self.arg_validator = ArgumentValidator()

    def get_year_month(self, year_month):
        year_month = year_month.split('/')
        year = year_month[0]
        month = year_month[1]
        return year, month

    def read_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "dir_path",
            help="the path of directory where files are allocated",
            default=1,
            nargs='?'
        )
        parser.add_argument(
            "-e",
            type=ArgumentValidator.validate_year,
            help="specify year for required information"
        )
        parser.add_argument(
            "-c",
            type=ArgumentValidator.validate_month_year,
            help="specify month for required information"
        )
        parser.add_argument(
            "-a",
            type=ArgumentValidator.validate_month_year,
            help="specify month for required information"
        )

        args = parser.parse_args()
        ArgumentValidator.valid_number_of_arguments(args, parser)
        return args

    def print_weather_report(self):
        arg = self.read_arguments()
        weather_files_path = arg.dir_path + "/"
        if arg.e:
            year = arg.e
            self.weather_reporter.print_yearly_weather_report(
                year,
                weather_files_path
            )
        if arg.a:
            year, month = self.get_year_month(arg.a)
            self.weather_reporter.print_monthly_average_report(
                year,
                month,
                weather_files_path
            )
        if arg.c:
            year, month = self.get_year_month(arg.c)
            self.weather_reporter.print_daily_report(
                year,
                month,
                weather_files_path
            )
            self.weather_reporter.print_daily_report_bonus(
                year,
                month,
                weather_files_path
            )


def main():
    WeathermanDriver().print_weather_report()


if __name__ == '__main__':
    main()
