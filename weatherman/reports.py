""" Controller file """
import sys
from reports import display_year_report, display_month_report


if len(sys.argv) > 3 and (((len(sys.argv)-2) % 2) == 0):
    for i in range(2, len(sys.argv), 2):
        try:
            if sys.argv[i] == "-e":
                display_year_report(sys.argv[1], sys.argv[i+1])
            elif sys.argv[i] == "-a":
                display_month_report(sys.argv[1], sys.argv[i+1], False)
            elif sys.argv[i] == "-c":
                display_month_report(sys.argv[1], sys.argv[i+1], True)
            else:
                print("\n<< Invalid option "+sys.argv[i])
                break
        except IndexError:
            print("\n<< Invalid arguments\n")
else:
    print("\n<< Invalid argument list\n")
