
import calendar
import argparse

from DataParser import DataParser
from Computer import Analyzer


def main(cmdArg):
    """
    main method for program weatherman handles all the functionality of program
    and use DataParser and Analyzer classes to fill data and perform actions on it and Display the reports
    :param cmdArg: command line arguments after parsing into path and lists e, a and c.
    :return:
    """
    data = {
        'features': [],
        'values': []
    }

    # Collecting data
    data = DataParser.parsefile(cmdArg.path, data)

    if not data['values']:
        print('No file found on given path!')
    else:

        for year in cmdArg.e:
            result = Analyzer.yearly_report(data, year)
            if result:
                print(
                    'Highest: ' + result['Highest'] + '\n' +
                    'Lowest: ' + result['Lowest'] + '\n' +
                    'Humidity: ' + result['Humidity'] + '\n'
                )
            else:
                print('No data Found Against ' + year)

        for date in cmdArg.a:
            date = date.replace('/0', '/')
            result = Analyzer.monthly_report(data, date)
            if result:
                print(
                    'Highest Average: ' + result['Highest Average'] + '\n' +
                    'Lowest Average: ' + result['Lowest Average'] + '\n' +
                    'Average Mean Humidity: ' + result['Average Mean Humidity'] + '\n'
                )
            else:
                print('No data Found Against ' + date)

        for date in cmdArg.c:
            date = date.replace('/0', '/')
            result = Analyzer.monthly_chart(data, date)
            year, month = date.split('/')

            print(calendar.month_name[int(month)] + ' ' + year)
            if result:
                for key, value in sorted(result.items()):
                    if value:
                        sign, temp = value[0].split(' ')
                        print(key + ' \033[1;31m' + sign + '\033[m ' + temp)

                        sign, temp = value[1].split(' ')
                        print(key + ' \033[1;34m' + sign + '\033[m ' + temp)
                    else:
                        print('{} No Data!'.format(key))

                print('Bonus:')

                for key, value in sorted(result.items()):
                    if value:
                        sign_for_high, temp_high = value[0].split(' ')
                        sign_for_low, temp_low = value[1].split(' ')
                        output_string = '{} \033[1;34m{}\033[1;31m{}\033[m {} - {}'

                        print(output_string.format(key, sign_for_low, sign_for_high, temp_low, temp_high))
                    else:
                        print('{} No Data!'.format(key))
            else:
                print('No data Found Against ' + date)


if __name__ == "__main__":
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

    main(cmd_Arguments)
