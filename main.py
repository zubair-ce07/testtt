import argparse
import calendar
import parsed_weather_data
import weather_summary as ws
import weather_report_generator


parser = argparse.ArgumentParser()

parser.add_argument("file_path", help="This arg stores the path to all weather data files", type=str)

parser.add_argument("-e", help="This command will give you the highest and "
                               "lowest temperature and highest humidity with "
                               "respective days for given year", type=int, choices=range(2004, 2017))

parser.add_argument("-a", help="This command will give you the highest and "
                               "lowest avg temperature and Mean avg Humidity"
                               "for a given month", type=str)

parser.add_argument("-c", help="For a given month this command will draw two "
                               "horizontal bar charts on the console for the "
                               "highest and lowest temperature on each day. "
                               "Highest in red and lowest in blue.", type=str)

parser.add_argument("-b", help="For a given month this command will draw one "
                               "horizontal bar charts on the console for the "
                               "highest and lowest temperature on each day. "
                               "Highest in red and lowest in blue.", type=str)

args = parser.parse_args()


def get_year_month(date):
    year_month = date.split("/")

    if len(year_month) == 2:
        year = year_month[0]
        month = year_month[1]

        if year.isdigit() and month.isdigit() \
                and int(year) in range(2004, 2017) and int(month) in range(1, 13):
            return int(year), int(month)

    print("The date given is not valid!")


if __name__ == "__main__":
    file_path = args.file_path
    report = weather_report_generator.WeatherReportGenerator()
    reports = ""

    if args.e:
        data_parser = parsed_weather_data.ParsedWeatherData()
        filtered_data = data_parser.get_filtered_data(file_path, args.e)
        result = ws.WeatherSummary.get_result_for_e(filtered_data)
        report.set_report_for_e(result)
        reports += report.report+"\n\n"

    if args.a:
        year_month = get_year_month(args.a)

        if year_month:
            data_parser = parsed_weather_data.ParsedWeatherData()
            filtered_data = data_parser.get_filtered_data(file_path, year_month[0],
                                                          calendar.month_abbr[year_month[1]])
            result = ws.WeatherSummary.get_result_for_a(filtered_data)
            report.set_report_for_a(result)
            reports += report.report+"\n\n"

    if args.c:
        year_month = get_year_month(args.c)

        if year_month:
            data_parser = parsed_weather_data.ParsedWeatherData()
            filtered_data = data_parser.get_filtered_data(file_path, year_month[0],
                                                          calendar.month_abbr[year_month[1]])
            result = ws.WeatherSummary.get_result_for_c(filtered_data)
            report.set_report_for_c(result)
            reports += report.report + "\n\n"

    if args.b:
        year_month = get_year_month(args.c)

        if year_month:
            data_parser = parsed_weather_data.ParsedWeatherData()
            filtered_data = data_parser.get_filtered_data(file_path, year_month[0],
                                                          calendar.month_abbr[year_month[1]])
            result = ws.WeatherSummary.get_result_for_c(filtered_data)
            report.set_report_for_c_bonus(result)
            reports += report.report + "\n\n"

    print(reports)
