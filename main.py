import calendar
import sys
from Handler import *


def main():
    if not validate_arg(sys.argv):
        print(f"Error: few Arg{str(sys.argv)}\nProper format is /path [-e] year [-a] year/month [-c] year/month")
        exit(0)
    else:
        i = 2  # skipping First 2 arg as they are file name and path
        while i < len(sys.argv):
            # get ind[] of the total indexes encounter for -a flag in the command line argument
            ind = [i for i, x in enumerate(sys.argv) if x == '-a']
            j = 0  # Variable to iterate over ind
            while j < len(ind):
                token = sys.argv[ind[j] + 1].split('/')
                path =\
                    sys.argv[1] + '/weatherfiles/Murree_weather_' + token[0] +\
                    '_' + calendar.month_abbr[int(token[1])] + '.txt'  # append calender.month_abbr to path
                i = i + 2
                j = j + 1
                print(calculate_monthly_report(read_file(path)))
                print()
            # get ind[] of the total indexes encounter for -e flag in the command line argument
            ind = [i for i, x in enumerate(sys.argv) if x == '-e']
            j = 0
            while j < len(ind):
                lst = list()
                month = 1
                while month <= 12:
                    path = \
                        sys.argv[1] + '/weatherfiles/Murree_weather_' + sys.argv[ind[j] + 1] + \
                        '_' + calendar.month_abbr[month] + '.txt'
                    lst = lst + read_file(path)
                    month = month + 1
                print(calculate_yearly_report(lst))
                i = i + 2
                j = j + 1
            # get ind[] of the total indexes encounter for -c flag in the command line argument
            ind = [i for i, x in enumerate(sys.argv) if x == '-c']
            j = 0
            while j < len(ind):
                token = sys.argv[ind[j] + 1].split('/')
                path =\
                    sys.argv[1] + '/weatherfiles/Murree_weather_' + token[0] +\
                    '_' + calendar.month_abbr[int(token[1])] + '.txt'
                i = i + 2
                j = j + 1
                print(calculate_chart_report(read_file(path)))

                print()


main()
