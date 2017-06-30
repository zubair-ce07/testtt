import argparse
from YearlyWeatherExtremesReport import YearlyWeatherExtremesReport
from MonthlyTemperatureReports import MonthlyTemperatureReports
from filereader import FileReader
from TemperatureGraph import TemperatureGraph
from argumentvalidator import ArgumentValidator


def main():
    arg_validator = ArgumentValidator()

    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path", help="the path of directory where files are allocated",
                        default=1, nargs='?')
    parser.add_argument("-e", "--arg_report1", type=arg_validator.validate_arguments_year,
                        help="specify year for required information")
    parser.add_argument("-c", "--arg_report2", type=arg_validator.validate_arguments_month_year,
                        help="specify month for required information")
    parser.add_argument("-a", "--arg_report3", type=arg_validator.validate_arguments_month_year,
                        help="specify month for required information")

    args = parser.parse_args()
    arg_validator.check_number_arguments(args, parser)

    file_reader = FileReader(args)
    report_records = file_reader.read_files()

    if args.arg_report1:
        year = args.arg_report1
        report1_records = report_records['report1']
        if report1_records:
            report_one = YearlyWeatherExtremesReport(report1_records)
            report_one.generate_report()
            report_one.print_report()
        else:
            print("Report1: Record for the year %s doesn't exists \n" % (year))

    if args.arg_report2:
        year, month = args.arg_report2.split('/')
        report2_records = report_records['report2']
        if report2_records:
            report_two = MonthlyTemperatureReports(report_records['report2'])
            report_two.generate_report()
            report_two.print_report()
        else:
            print("Report2: Record for the %s/%s doesn't exists \n" % (year, month))

    if args.arg_report3:
        year, month = args.arg_report3.split('/')
        report3_records = report_records['report3']
        if report3_records:
            report_three = TemperatureGraph(report_records['report3'])
            report_three.print_report()
        else:
            print("Report3: Record for the %s/%s doesn't exists \n" % (year, month))


if __name__ == "__main__":
    main()
