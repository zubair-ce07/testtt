import argparse
from filereader import FileReader
from TemperatureGraph import TemperatureGraph
from argumentvalidator import ArgumentValidator
from YearlyWeatherExtremesReport import YearlyWeatherExtremesReport
from MonthlyTemperatureReports import MonthlyTemperatureReports


def main():
    arg_validator = ArgumentValidator()

    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path", help="the path of directory where files are allocated",
                        default=1, nargs='?')
    parser.add_argument("-e", "--yearly_report", type=arg_validator.validate_arguments_year,
                        help="specify year for required information")
    parser.add_argument("-c", "--monthly_report",
                        type=arg_validator.validate_arguments_month_year,
                        help="specify month for required information")
    parser.add_argument("-a", "--temp_graph", type=arg_validator.validate_arguments_month_year,
                        help="specify month for required information")

    args = parser.parse_args()
    arg_validator.check_number_arguments(args, parser)

    file_reader = FileReader(args)
    report_records = file_reader.read_files()

    if args.yearly_report:
        year = args.yearly_report
        records = report_records.get('yearly_report')
        if records:
            report = YearlyWeatherExtremesReport(records)
            report.generate_report()
            report.print_report()
        else:
            print("Record for the given year %s doesn't exists \n" % year)

    if args.monthly_report:
        year, month = args.monthly_report.split('/')
        records = report_records.get('monthly_report')
        if records:
            report = MonthlyTemperatureReports(report_records.get('monthly_report'))
            report.generate_report()
            report.print_report()
        else:
            print("Record for the given %s/%s doesn't exists \n" % (year, month))

    if args.temp_graph:
        year, month = args.temp_graph.split('/')
        records = report_records.get('temp_graph')
        if records:
            report = TemperatureGraph(report_records.get('temp_graph'))
            report.print_report()
        else:
            print("Record for the given %s/%s doesn't exists \n" % (year, month))


if __name__ == "__main__":
    main()
