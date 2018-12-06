import argparse
import sys
import analysis
import reportgenerator
import datareader


def check_arg(args=None):
    parser = argparse.ArgumentParser(description='Process command line arguments.')

    parser.add_argument('-e', '--yearly',
                        help='yearly report',
                        required=False,
                        default='')

    parser.add_argument('-a', '--monthly',
                        help='monthly report',
                        required=False,
                        default='')

    parser.add_argument('-c', '--bar_chart',
                        help='bar chart report',
                        required=False,
                        default='')

    return parser.parse_args(args)


def main():

    data_set = datareader.data_parser(sys.argv[1] + '/*.txt')
    if data_set:
        parsed_args = check_arg(sys.argv[2:])
        for report_name in vars(parsed_args):
            report_args = getattr(parsed_args, report_name)
            if report_args != '':
                result = analysis.computation_analysis(data_set, report_name, report_args)
                if result:
                    reportgenerator.report_generator(report_name, result)


if __name__ == "__main__":
    main()
