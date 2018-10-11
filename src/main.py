import argparse
from datetime import datetime

from calculations import WeatherCalculations
from report_generator import ReportGenerator


def month_date(date):
    return datetime.strptime(date, '%Y/%m')


def year_date(date):
    return datetime.strptime(date, '%Y')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path", type=str)
    parser.add_argument('-e', type=year_date, nargs='*')
    parser.add_argument('-a', type=month_date, nargs='*')
    parser.add_argument('-c', type=month_date, nargs='*')
    args = parser.parse_args()

    weather_calculations = WeatherCalculations()
    weather_records = weather_calculations.all_weather_record(args.dir_path)

    report_generator = ReportGenerator()

    if args.e:
        for date in args.e:
            report_generator.generate_year_report(weather_calculations.year_report(weather_records, date))
    if args.a:
        for date in args.a:
            report_generator.generate_average_month_report(weather_calculations.average_report(weather_records, date))
    if args.c:
        for date in args.c:
            report_generator.generate_temp_chart(weather_calculations.month_records(weather_records, date),
                                                 single_line=True)


if __name__ == '__main__':
    main()
