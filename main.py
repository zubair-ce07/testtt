import argparse
import calendar
import datetime
import parsed_weather_reading
import weather_result_computer as ws
import weather_report_maker as report_maker


user_command_parser = argparse.ArgumentParser()

user_command_parser.add_argument("file_path", help="This arg stores the path to all weather data files", type=str)

user_command_parser.add_argument("-e", help="This command will give you the highest and "
                               "lowest temperature and highest humidity with "
                               "respective days for given year", type=int, choices=range(2004, 2017))

user_command_parser.add_argument("-a", help="This command will give you the highest and "
                               "lowest avg temperature and Mean avg Humidity"
                               "for a given month", type=str)

user_command_parser.add_argument("-c", help="For a given month this command will draw two "
                               "horizontal bar charts on the console for the "
                               "highest and lowest temperature on each day. "
                               "Highest in red and lowest in blue.", type=str)

user_command_parser.add_argument("-b", help="For a given month this command will draw one "
                               "horizontal bar charts on the console for the "
                               "highest and lowest temperature on each day. "
                               "Highest in red and lowest in blue.", type=str)

user_cli_args = user_command_parser.parse_args()


def get_year_month(weather_date):
    date_year_month = weather_date.split("/")

    if len(date_year_month) == 2:
        year = date_year_month[0]
        month = date_year_month[1]

        if year.isdigit() and month.isdigit() \
                and int(year) in range(datetime.MINYEAR, datetime.MAXYEAR+1) and int(month) in range(1, 13):
            return int(year), int(month)

    print("The date given is not valid!")


if __name__ == "__main__":
    file_path = user_cli_args.file_path

    if user_cli_args.e:
        data_parser = parsed_weather_reading.ParsedWeatherReading()
        filtered_data = data_parser.get_weather_records(file_path, user_cli_args.e)
        result = ws.WeatherResultComputer.get_result_for_e(filtered_data)
        report = report_maker.WeatherReportMaker.print_report_for_e(result)

    if user_cli_args.a:
        year_month = get_year_month(user_cli_args.a)

        if year_month:
            data_parser = parsed_weather_reading.ParsedWeatherReading()
            filtered_data = data_parser.get_weather_records(file_path, year_month[0],
                                                            calendar.month_abbr[year_month[1]])
            result = ws.WeatherResultComputer.get_result_for_a(filtered_data)
            report_maker.WeatherReportMaker.print_report_for_a(result)

    if user_cli_args.c:
        year_month = get_year_month(user_cli_args.c)

        if year_month:
            data_parser = parsed_weather_reading.ParsedWeatherReading()
            filtered_data = data_parser.get_weather_records(file_path, year_month[0],
                                                            calendar.month_abbr[year_month[1]])
            result = ws.WeatherResultComputer.get_result_for_c(filtered_data)
            report_maker.WeatherReportMaker.print_report_for_c(result)

    if user_cli_args.b:
        year_month = get_year_month(user_cli_args.c)

        if year_month:
            data_parser = parsed_weather_reading.ParsedWeatherReading()
            filtered_data = data_parser.get_weather_records(file_path, year_month[0],
                                                            calendar.month_abbr[year_month[1]])
            result = ws.WeatherResultComputer.get_result_for_c(filtered_data)
            report_maker.WeatherReportMaker.print_report_for_c_bonus(result)
