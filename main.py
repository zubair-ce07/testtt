import calendar
import os
import sys
from ReportGenerator import ReportGenerator
from Parser import Parser
import logging


def main():
    if len(sys.argv) < 4:
        logging.error(f"Error: few Arg{str(sys.argv)}\n"
                      f"Proper format is /path [-e] year [-a] year/month [-c] year/month")
        exit(0)
    if not os.path.exists(sys.argv[1]):
        logging.error('File path does not exists')
        exit(0)
    else:
        index = 2  # skipping First 2 arg as they are file name and path
        while index < len(sys.argv):
            # get flag_indexes[] of the total indexes encounter for -a flag in the command line argument
            flag_indexes = [i for i, x in enumerate(sys.argv) if x == '-a']
            flag_iter = 0  # Variable to iterate over flag_indexes
            while flag_iter < len(flag_indexes):
                tokenize_date = sys.argv[flag_indexes[flag_iter] + 1].split('/')
                if int(tokenize_date[0]) not in range(2004, 2017):
                    logging.error('Year must between 2004 - 2016')
                    exit(0)
                if int(tokenize_date[1]) not in range(1, 13):
                    logging.error('Month must between 1 - 12')
                    exit(0)
                path =\
                    sys.argv[1] + '/weatherfiles/Murree_weather_' + tokenize_date[0] +\
                    '_' + calendar.month_abbr[int(tokenize_date[1])] + '.txt'  # append calender.month_abbr to path
                index += 2
                flag_iter += 1
                print(ReportGenerator.calculate_monthly_report(Parser.read_file(path)))
                print()
            # get flag_indexes[] of the total indexes encounter for -e flag in the command line argument
            flag_indexes = [i for i, x in enumerate(sys.argv) if x == '-e']
            flag_iter = 0
            while flag_iter < len(flag_indexes):
                if int(sys.argv[flag_indexes[flag_iter] + 1]) not in range(2004, 2017):
                    logging.error('Year must between 2004 - 2016')
                    exit(0)
                reading_list = list()
                month = 1
                while month <= 12:
                    path = \
                        sys.argv[1] + '/weatherfiles/Murree_weather_' + sys.argv[flag_indexes[flag_iter] + 1] + \
                        '_' + calendar.month_abbr[month] + '.txt'
                    reading_list = reading_list + Parser.read_file(path)
                    month += 1
                print(ReportGenerator.calculate_yearly_report(reading_list))
                index += 2
                flag_iter += 1
            # get flag_indexes[] of the total indexes encounter for -c flag in the command line argument
            flag_indexes = [i for i, x in enumerate(sys.argv) if x == '-c']
            flag_iter = 0
            while flag_iter < len(flag_indexes):
                tokenize_date = sys.argv[flag_indexes[flag_iter] + 1].split('/')
                if int(tokenize_date[0]) not in range(2004, 2017):
                    logging.error('Year must between 2004 - 2016')
                    exit(0)
                if int(tokenize_date[1]) not in range(1, 13):
                    logging.error('Month must between 1 - 12')
                    exit(0)
                path =\
                    sys.argv[1] + '/weatherfiles/Murree_weather_' + tokenize_date[0] +\
                    '_' + calendar.month_abbr[int(tokenize_date[1])] + '.txt'
                index += 2
                flag_iter += 1
                print(ReportGenerator.calculate_chart_report(Parser.read_file(path)))
                print()


main()
