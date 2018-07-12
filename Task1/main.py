import argparse
import calendar
import datetime

from parsed_weather_reading import ParsedWeatherReading
from weather_result_computer import WeatherResultComputer
from weather_report_maker import WeatherReportMaker


def valid_year(year):
    if int(year) > datetime.date.today().year:
        raise argparse.ArgumentTypeError(f"Max year is {datetime.date.today().year}")
    return int(year)


def valid_year_month(weather_date):
    try:
        weather_date = datetime.datetime.strptime(weather_date, '%Y/%m')
    except ValueError:
        raise argparse.ArgumentTypeError(f"The Date is not valid")

    return valid_year(weather_date.year), weather_date.month


user_command_parser = argparse.ArgumentParser()

user_command_parser.add_argument("file_path", help="This arg stores the path to all weather data files", type=str)
user_command_parser.add_argument("-e", help="This command will give you the highest and "
                                 "lowest temperature and highest humidity with "
                                 "respective days for given year", type=valid_year)
user_command_parser.add_argument("-a", help="This command will give you the highest and "
                                 "lowest avg temperature and Mean avg Humidity"
                                 "for a given month", type=valid_year_month)
user_command_parser.add_argument("-c", help="For a given month this command will draw two "
                                 "horizontal bar charts on the console for the "
                                 "highest and lowest temperature on each day. "
                                 "Highest in red and lowest in blue.", type=valid_year_month)
user_command_parser.add_argument("-b", help="For a given month this command will draw one "
                                 "horizontal bar charts on the console for the "
                                 "highest and lowest temperature on each day. "
                                 "Highest in red and lowest in blue.", type=valid_year_month)

user_cli_args = user_command_parser.parse_args()


if __name__ == "__main__":
    file_path = user_cli_args.file_path

    if user_cli_args.e:
        weather_record_parser = ParsedWeatherReading()
        filtered_weather_records = weather_record_parser.get_weather_records(file_path, user_cli_args.e)
        weather_summary_result = WeatherResultComputer.get_result(filtered_weather_records)
        WeatherReportMaker.print_report_for_e(weather_summary_result)

    if user_cli_args.a:
        year, month = user_cli_args.a
        weather_record_parser = ParsedWeatherReading()
        filtered_weather_records = weather_record_parser.get_weather_records(file_path, year,
                                                                             calendar.month_abbr[month])
        weather_summary_result = WeatherResultComputer.get_result(filtered_weather_records)
        WeatherReportMaker.print_report_for_a(weather_summary_result)

    if user_cli_args.c:
        year, month = user_cli_args.c
        weather_record_parser = ParsedWeatherReading()
        filtered_weather_records = weather_record_parser.get_weather_records(file_path, year,
                                                                             calendar.month_abbr[month])
        weather_summary_result = WeatherResultComputer.get_result(filtered_weather_records)
        WeatherReportMaker.print_report_for_c(weather_summary_result)

    if user_cli_args.b:
        year, month = user_cli_args.b
        weather_record_parser = ParsedWeatherReading()
        filtered_weather_records = weather_record_parser.get_weather_records(file_path, year,
                                                                             calendar.month_abbr[month])
        weather_summary_result = WeatherResultComputer.get_result(filtered_weather_records)
        WeatherReportMaker.print_report_for_c_bonus(weather_summary_result)
