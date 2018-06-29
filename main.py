import dataparser
import weather_summary as ws
import report_generator
import argparse


parser = argparse.ArgumentParser()


parser.add_argument("file_path", help="This arg stores the path to all "
                                      "weather data files", type=str)

parser.add_argument("-e", help="This command will give you the highest and "
                               "lowest temperature and highest humidity with "
                               "respective days for given year", type=int)

parser.add_argument("-a", help="This command will give you the highest and "
                               "lowest avg temperature and Mean avg Humidity"
                               "for a given month"
                               , type=str)

parser.add_argument("-c", help="For a given month this command will draw two "
                               "horizontal bar charts on the console for the "
                               "highest and lowest temperature on each day. "
                               "Highest in red and lowest in blue."
                               , type=str)

parser.add_argument("-b", help="For a given month this command will draw one "
                               "horizontal bar charts on the console for the "
                               "highest and lowest temperature on each day. "
                               "Highest in red and lowest in blue."
                               , type=str)

args = parser.parse_args()


def get_year_month(date):
    year_month = date.split("/")
    year = None
    month = None

    if len(year_month) == 2:
        year = year_month[0]
        month = year_month[1]

        if year.isdigit() and month.isdigit():
            return year, month

    print("The date given is not valid!")
    return None


if __name__ == "__main__":
    # The user provided params starts from index 1
    file_path = args.file_path
    data_parser = dataparser.DataParser()
    data = data_parser.get_data(file_path)
    report = report_generator.ReportGenerator()
    reports = ""

    if args.e:
        result = ws.WeatherSummary.get_result_for_e(args.e, data)
        report.set_report_for_e(result)
        reports += report.report+"\n\n"

    if args.a:
        year_month = get_year_month(args.a)

        if year_month is not None:
            result = ws.WeatherSummary.get_result_for_a(int(year_month[0]),
                                                      int(year_month[1]),
                                                      data)
            report.set_report_for_a(result)
            reports += report.report+"\n\n"

    if args.c:
        year_month = get_year_month(args.c)

        if year_month is not None:
            result = ws.WeatherSummary.get_result_for_c(int(year_month[0]),
                                                      int(year_month[1]),
                                                      data)
            report.set_report_for_c(result)
            reports += report.report + "\n\n"

    if args.b:
        year_month = get_year_month(args.c)

        if year_month is not None:
            result = ws.WeatherSummary.get_result_for_c(int(year_month[0]),
                                                       int(year_month[1]),
                                                       data)
            report.set_report_for_c_bonus(result)
            reports += report.report + "\n\n"

    print(reports)



