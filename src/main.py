import argparse
from datetime import datetime

from calculations import WeatherCalculations
from report_generator import ReportGenerator


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("dir_path", type=str)
    parser.add_argument('-e', type=lambda date: datetime.strptime(date, '%Y'), nargs='*')
    parser.add_argument('-a', type=lambda date: datetime.strptime(date, '%Y/%m'), nargs='*')
    parser.add_argument('-c', type=lambda date: datetime.strptime(date, '%Y/%m'), nargs='*')

    return parser.parse_args()


def main():
    args = parse_arguments()

    weather_calculations = WeatherCalculations()
    weather_records = weather_calculations.read_weather_records(args.dir_path)

    report_generator = ReportGenerator()

    if args.e:
        for date in args.e:
            year_report = weather_calculations.year_report(weather_records, date)
            report_generator.generate_year_report(year_report)
    if args.a:
        for date in args.a:
            month_report = weather_calculations.average_report(weather_records, date)
            report_generator.generate_month_report(month_report)
    if args.c:
        for date in args.c:
            month_report = weather_calculations.month_records(weather_records, date)
            report_generator.generate_month_chart_report(month_report, single_line=True)


if __name__ == '__main__':
    main()
