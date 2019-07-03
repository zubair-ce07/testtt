import argparse

from datetime import datetime

from data_calculator import DataCalculator
from input_handler import FileParser
from report_generator import ReportGenerator


def arg_parser():

    parser = argparse.ArgumentParser()
    parser.add_argument('file_path',
                        help='The file path of weather files')
    parser.add_argument('-e', '-yearly',
                        type=lambda arg: datetime.strptime(
                            arg, '%Y'), nargs="*")
    parser.add_argument('-a', '-monthly',
                        type=lambda arg: datetime.strptime(
                            arg, '%Y/%m'), nargs="*")
    parser.add_argument('-b', '-bonus',
                        type=lambda arg: datetime.strptime(
                            arg, '%Y/%m'), nargs="*")
    parser.add_argument('-c', '-chart',
                        type=lambda arg: datetime.strptime(
                            arg, '%Y/%m'), nargs="*")
    parsed_data = parser.parse_args()
    return parsed_data


if __name__ == "__main__":
    input_arguments = arg_parser()
    path = input_arguments.file_path
    file_extraction = FileParser

    data_extracted = file_extraction.data_extractor(file_extraction, path)
    calculator = DataCalculator()
    report = ReportGenerator()

    if input_arguments.e:
        for arguments in input_arguments.e:
            result = (calculator.yearly_analysis(
                data_extracted, arguments.date()))
            report.generate_yearly_report(*iter(result))

    if input_arguments.a:
        for arguments in input_arguments.a:
            result = (calculator.monthly_analysis(
                data_extracted, arguments.date()))
            report.generate_monthly_report(*iter(result))

    if input_arguments.b:
        for arguments in input_arguments.b:
            report.generate_bonus_report(data_extracted, arguments.date())

    if input_arguments.c:
        for arguments in input_arguments.c:
            report.generate_chart_report(data_extracted, arguments.date())
