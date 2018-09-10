import argparse

from DataReader import DataReader
from Analyzer import Analyzer
from DisplayReports import DisplayReports


def get_cmdline_arguments():
    """
    This method takes arguments from command line and parse them into a namespace
    :return: a Namespace<> object containing command line arguments parsed and set up
    """
    cmdline_parser = argparse.ArgumentParser(description='Program Argument')

    cmdline_parser.add_argument(
        'path',
        metavar='P',
        type=str,
        help='Path to directory containing data files'
    )

    cmdline_parser.add_argument(
        '-e',
        dest='e',
        default=[],
        action='append',
        help='highest temperature and day, lowest temperature and day, most humidity and day of year use: -e 2011',
    )

    cmdline_parser.add_argument(
        '-a',
        dest='a',
        default=[],
        action='append',
        help='average highest and lowest temperature and mean humidity of month use: -a 2010/1'
    )

    cmdline_parser.add_argument(
        '-c',
        dest='c',
        default=[],
        action='append',
        help='bar chart for temperature for each day of month use: -c 2010/5'
    )

    cmd_Arguments = cmdline_parser.parse_args()

    return cmd_Arguments


def main():
    """
    main method for program weatherman handles all the functionality of program
    and use DataParser and Analyzer classes to fill data and perform actions on it and Display the reports
    :param
    :return:
    """

    # Get Command line arguments
    cmdArg = get_cmdline_arguments()

    # Collecting data
    data = DataReader.parsefile(cmdArg.path)

    if not data:
        print('No file found on given path!')
        return 0

    for year in cmdArg.e:
        result = Analyzer.yearly_report(data, year)

        if result:
            DisplayReports.print_year_report(result)
        else:
            print('No data Found Against ' + year)

    for date in cmdArg.a:
        date = date.replace('/0', '/')
        result = Analyzer.monthly_report(data, date)

        if result:
            DisplayReports.print_monthly_report(result)
        else:
            print('No data Found Against ' + date)

    for date in cmdArg.c:
        date = date.replace('/0', '/')
        result = Analyzer.monthly_chart(data, date)

        if result:
            DisplayReports.print_monthly_charts(result, date)
        else:
            print('No data Found Against ' + date)


if __name__ == "__main__":
    main()
