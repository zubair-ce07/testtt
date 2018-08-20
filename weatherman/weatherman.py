"""weaatherman.py script.
used for manipulating files having daily weather information of a city.
"""
import sys
from cmdline_utils import display_usage_help, parse_input, validate_input
from filehandler import WeatherFileHandler
from reportgenerator import ReportGenerator
from weathercontroller import WeatherController
import constants


def main():
    """Driver function for the script."""
    if validate_input(sys.argv) is not True:
        display_usage_help()
        return
    parsed_args = parse_input(sys.argv)
    file_handler = WeatherFileHandler(parsed_args["path_to_files"], "Murree")
    controller = WeatherController()
    report_generator = ReportGenerator()
    current_report_no = 1
    for report in parsed_args["report_operations"]:

        print("\nReport #{} :-\n".format(current_report_no))
        current_report_no += 1
        if not report["report_date"]:
            print("Invalid Date is provided!")
            continue
        result = None
        if report["report_type"] == constants.YEARLY_TEMPERATURE:
            readings = file_handler.read_year_files(report["report_date"].year)
            if readings:
                result = controller.find_yearly_extremes(readings)
        elif report["report_type"] == constants.AVERAGE_TEMPERATURE:
            readings = file_handler.read_month_file(report["report_date"].year,
                                                    report["report_date"].month)
            if readings:
                result = controller.find_month_average(readings)
        elif report["report_type"] in (constants.ONE_LINE_CHART,
                                       constants.TWO_LINE_CHART):
            readings = file_handler.read_month_file(report["report_date"].year,
                                                    report["report_date"].month)
            if readings:
                result = readings
        report_generator.display_report(result, report["report_type"])


if __name__ == "__main__":
    main()
