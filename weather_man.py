import argparse

from validators import validate_path
from validators import validate_year
from validators import validate_year_and_month
from validators import verify_year_month_weather_readings_exist_and_read_file_paths

from general_helper import change_month_to_month_name

from weather_man_helper import ReportType
from weather_man_helper import WeatherManFileParser
from weather_man_helper import WeatherManResultCalculator
from weather_man_helper import WeatherManReportGenerator


def weather_man_report(path,year_month,report_type):
    """
    :param path:
    :param year_month:
    :param report_type:
    :return:
    """
    if type(year_month) is int:  # it is year
        reading_files = verify_year_month_weather_readings_exist_and_read_file_paths(path,year_month)
    else:  # it is year month
        year = year_month.split('/')[0]
        month = year_month.split('/')[1]
        month = change_month_to_month_name(int(month))
        reading_files = verify_year_month_weather_readings_exist_and_read_file_paths(path, year,month)

    if reading_files.__len__()>0:
        file_parser = WeatherManFileParser()
        weather_readings = file_parser.populate_weather_man_readings(reading_files)

        weather_readings_calculator=WeatherManResultCalculator()
        weather_results = weather_readings_calculator.compute_result(weather_readings, report_type)

        weather_readings_report_generator = WeatherManReportGenerator()
        if report_type == ReportType.TwoBarCharts:
            weather_readings_report_generator.generate_report(weather_results, report_type, year, month)
        else:
            weather_readings_report_generator.generate_report(weather_results, report_type)

    else:
        print("Weather readings for " + year_month + " not exist")


parser = argparse.ArgumentParser(description='Weatherman data analysis')

parser.add_argument('path', type=validate_path, help='Enter weather files directory path')

parser.add_argument('-c', type=validate_year_and_month, default=None,
                    help='(usage: -c yyyy/mm) To see two horizontal bar charts on the console'
                         ' for the highest and lowest temperature on each day. Highest in red and lowest in blue.')
parser.add_argument('-e', type=validate_year, default=None,
                    help='(usage: -e yyyy) To see highest temperature and day,'
                         ' lowest temperature and day, most humid day and humidity')
parser.add_argument('-a', type=validate_year_and_month, default=None,
                    help='(usage: -a yyyy/m) To see average highest temperature,'
                         ' average lowest temperature, average mean humidity.')

input_ = parser.parse_args()


if input_.path:

    # it means no parameter provided so display appropriate message to user
    if input_.e is None and input_.a is None and input_.c is None:
        print("Please provide paramter(s) to view report(s)")

    # here one of the parameters might None which is not dependent for displaying message to user
    else:
        if input_.e is not None and input_.e is not False:
            weather_man_report(input_.path, input_.e, ReportType.Year)
        else:
            if input_.a is None and input_.c is None:
                print("Invalid year")
        if input_.a is not None and input_.a is not False:
            weather_man_report(input_.path, input_.a, ReportType.YearMonth)
        else:
            if input_.e is None and input_.c is None:
                print("Invalid year/month")
        if input_.c is not None and input_.c is not False:
            weather_man_report(input_.path, input_.c, ReportType.TwoBarCharts)
        else:
            if input_.a is None and input_.e is None:
                print("Invalid year/month")
else:
    print("Path not Found")
