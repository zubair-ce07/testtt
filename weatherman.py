import argparse

from datetime import datetime

from calculations import DataCalculator
from weather_data import FileParser
from reporter import ReportGenerator


def check_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='The local file path of weather files')
    parser.add_argument('-e', nargs="*", type=lambda arg: datetime.strptime(arg, '%Y'), )
    parser.add_argument('-a', nargs="*", type=lambda arg: datetime.strptime(arg, '%Y/%m'))
    parser.add_argument('-c', nargs="*", type=lambda arg: datetime.strptime(arg, '%Y/%m'))
    parser.add_argument('-b', nargs="*", type=lambda arg: datetime.strptime(arg, '%Y/%m'))

    return parser.parse_args()


if __name__ == "__main__":
    args = check_args()
    if args.e:
        for arguments in args.e:
            outcome = DataCalculator().month_average(FileParser.file_reader(FileParser, args.file_path),arguments.date().year)
            ReportGenerator().print_max_min(outcome)

    if args.a:
        for arguments in args.a:
            outcome = DataCalculator().get_max_min(FileParser.file_reader(FileParser, args.file_path),arguments.date())
            ReportGenerator().monthly_average(outcome)

    if args.c:
        for arguments in args.c:
            outcome = DataCalculator().monthly_records(FileParser.file_reader(FileParser, args.file_path),arguments.date())
            ReportGenerator().print_chart(outcome)

    if args.b:
        for arguments in args.b:
            outcome = DataCalculator().monthly_records(FileParser.file_reader(FileParser, args.file_path),arguments.date())
            ReportGenerator().bonus_chart(outcome)


