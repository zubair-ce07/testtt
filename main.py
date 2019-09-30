import weatherman as weatherman
import argparse
import datetime
import re
import os


def validate_month_and_year(date):
    month_format = re.compile(r"\d{4}/\d{1,2}$")
    if not month_format.match(date):
        raise argparse.ArgumentTypeError
    return date


def validate_year(year):
    if re.match("\\d{4}$", year):
        return year
    else:
        raise argparse.ArgumentTypeError(f"Invalid format: {year}")


def validate_path(argument):
    if os.path.exists(argument):
        return argument
    else:
        raise argparse.ArgumentTypeError(f"Invalid Path: {argument}")


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=validate_path)
    parser.add_argument("-a", help="Format should be like yyyy/m",
                        type=validate_month_and_year)
    parser.add_argument("-c", help="Format should be like yyyy/m",
                        type=validate_month_and_year)
    parser.add_argument("-e", help="Format should be like yyyy",
                        type=validate_year)
    args = parser.parse_args()
    if not (args.a or args.c or args.e):
        parser.error('No arguments provided!')
    return args


def generate_reports(args):

    report = weatherman.WeatherAnalysis()
    if args.a:
        file_names = report.get_files(args.path)
        if file_names:
            date = args.a.replace("/", "-")
            file_records = report.reading_file(file_names, date)
            report.display_monthly_report(file_records)
        else:
            print("File may not be available against -a argument!")
    if args.c:
        file_names = report.get_files(args.path)
        if file_names:
            date = args.c.replace('/', '-')
            file_records = report.reading_file(file_names, date)
            report.display_month_chart_report(file_records)
            report.display_month_bar_chart(file_records)
        else:
            print("File may not be available against -c argument!")
    if args.e:
        file_names = report.get_files(args.path)
        if file_names:
            file_records = report.reading_file(file_names, args.e)
            report.display_yearly_report(file_records)
        else:
            print("File may not be available against -e argument!")


def main():
    arguments = get_arguments()
    generate_reports(arguments)
if __name__ == "__main__":
    main()
