from datetime import datetime
import argparse
from weather_data_extractor import WeatherDataExtractor
from report_generator import ReportGenerator


def extract_month_year(year_month):
    year_month = year_month.split("/")
    try:
        date_time_obj = datetime(
            int(year_month[0]), int(year_month[1]), 1)
        return date_time_obj.strftime("%b"), year_month[0]
    except ValueError:
        print("Invalid month or year")
        return None, None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a')
    parser.add_argument('-e')
    parser.add_argument('-c')
    args = parser.parse_args()

    if args.e:
        weather_data = WeatherDataExtractor(year=args.e)
        report = ReportGenerator(weather_data)
        report.year_report()
    if args.a:
        month, year = extract_month_year(args.a)
        weather_data = WeatherDataExtractor(year=year, month=month)
        report = ReportGenerator(weather_data)
        report.month_report()
    if args.c:
        month, year = extract_month_year(args.c)
        weather_data = WeatherDataExtractor(year=year, month=month)
        report = ReportGenerator(weather_data)
        report.draw_bar_charts()
        report.draw_single_chart()
