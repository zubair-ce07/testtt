import argparse
import os
import datareader
import reports
import reportgenerator


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process command line arguments.')
    parser.add_argument('-path', type=dir_path)
    parser.add_argument('-e', help='yearly report', required=False, default='')
    parser.add_argument('-a', help='monthly report', required=False, default='')
    parser.add_argument('-c', help='bar chart report', required=False, default='')

    return parser.parse_args()


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{string} is not a valid path")


def main():

    parsed_args = parse_arguments()
    files_data = datareader.data_parser(parsed_args.path)

    if 'e' in parsed_args and parsed_args.e:
        result = reports.yearly_report(files_data, parsed_args.e)
        reportgenerator.generate_yearly_report(result)

    if 'a' in parsed_args and parsed_args.a:
        result = reports.monthly_report(files_data, parsed_args.a)
        reportgenerator.generate_monthly_report(result)

    if 'c' in parsed_args and parsed_args.c:
        result = reports.bar_chart_report(files_data, parsed_args.c)
        reportgenerator.generate_bonus_bar_chart(result)


if __name__ == "__main__":
    main()
