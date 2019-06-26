from datetime import datetime
import argparse
import WeatherDataExtractor, CalculationsResults, ReportGenerator, ResultStorage, WeatherReading


def extract_month_year(year_month):
    year_month = year_month.split("/")
    try:
        date_time_obj = datetime(int(year_month[0]), int(year_month[1]), 1)
        month = date_time_obj.strftime("%b")
        return month, year_month[0]
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
        weather_data_obj = WeatherDataExtractor.WeatherDataExtractor()
        weather_data = weather_data_obj.read_all_files(args.e, None)
        report = ReportGenerator.ReportGenerator()
        report.year_report(weather_data)
    if args.a:
        month, year = extract_month_year(args.a)
        weather_data_obj = WeatherDataExtractor.WeatherDataExtractor()
        weather_data = weather_data_obj.read_all_files(year, month)
        report = ReportGenerator.ReportGenerator()
        report.month_report(weather_data)
    if args.c:
        month, year = extract_month_year(args.c)
        print(month+" "+year)
        weather_data_obj = WeatherDataExtractor.WeatherDataExtractor()
        weather_data = weather_data_obj.read_all_files(year, month)
        report = ReportGenerator.ReportGenerator()
        report.draw_bar_charts(weather_data)
        report.draw_single_chart(weather_data)
