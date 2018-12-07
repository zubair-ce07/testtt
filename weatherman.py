import argparse
import os
import analysis
import datareader


def check_arg(args=None):
    parser = argparse.ArgumentParser(description='Process command line arguments.')

    parser.add_argument('-path', type=dir_path)
    parser.add_argument('-e', help='yearly report', required=False, default='')
    parser.add_argument('-a', help='monthly report', required=False, default='')
    parser.add_argument('-c', help='bar chart report', required=False, default='')

    return parser.parse_args(args)


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(string))


def main():

    parsed_args = check_arg()
    files_data = datareader.data_parser(parsed_args.path + '/*.txt')
    for report_name in vars(parsed_args):
        report_args = getattr(parsed_args, report_name)
        if report_args:
            analysis.computation_analysis(files_data, report_name, report_args)


if __name__ == "__main__":
    main()
