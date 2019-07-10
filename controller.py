import argparse

from datetime import datetime
from os.path import exists

from data_calculator import DataCalculator
from input_handler import FileParser
from report_generator import ReportGenerator


def is_valid_directory(directory):
    if exists(directory) is False:
        exit("Path is not valid")
    return directory


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=is_valid_directory, help='The local file path of weather files')
    parser.add_argument('-e', '-yearly', type=lambda arg: datetime.strptime(arg, '%Y'), nargs="*")
    parser.add_argument('-a', '-monthly', type=lambda arg: datetime.strptime(arg, '%Y/%m'), nargs="*")
    parser.add_argument('-b', '-bonus', type=lambda arg: datetime.strptime(arg, '%Y/%m'), nargs="*")
    parser.add_argument('-c', '-chart', type=lambda arg: datetime.strptime(arg, '%Y/%m'), nargs="*")
    return parser.parse_args()


if __name__ == "__main__":
    input_arguments = arg_parser()
    files_path = input_arguments.file_path
    weather_records = FileParser.data_extractor(FileParser, files_path)
    calculator = DataCalculator()
    report_gen = ReportGenerator()

    if input_arguments.e:
        for arguments in input_arguments.e:
            results = calculator.yearly_analysis(weather_records, arguments.date().year)
            report_gen.generate_yearly_report(results)

    if input_arguments.a:
        for arguments in input_arguments.a:
            results = calculator.monthly_analysis(weather_records, arguments.date())
            report_gen.generate_monthly_report(results)

    if input_arguments.b:
        for arguments in input_arguments.b:
            records = calculator.monthly_records(weather_records, arguments.date())
            report_gen.generate_chart_report(records, 'bonus')

    if input_arguments.c:
        for arguments in input_arguments.c:
            records = calculator.monthly_records(weather_records, arguments.date())
            report_gen.generate_chart_report(records)
