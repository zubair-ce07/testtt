import argparse
from reportone import ReportOne
from reporttwo import ReportTwo
from filereader import FileReader
from reportthree import ReportThree
from argumentvalidator import ArgumentValidator


def average(sequence, key=None):
    if key:
        sequence = map(key, sequence)
    return sum(sequence) / len(sequence)


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
    files_dict = file_reader.read_files()

    if args.arg_report1:
        year = args.arg_report1
        report_one = ReportOne(files_dict, year)
        report_one.generate_report()
        report_one.print_report()

    if args.arg_report2:
        year, month = args.arg_report2.split('/')
        report_two = ReportTwo(files_dict, year, month)
        report_two.generate_report()
        report_two.print_report()

    if args.arg_report3:
        year, month = args.arg_report3.split('/')
        report_three = ReportThree(files_dict, year, month)
        report_three.print_report()


if __name__ == "__main__":
    main()
