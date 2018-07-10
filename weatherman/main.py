"""Main function

main function for assembling the weatherman code and running the program.
"""
import sys

from calculate import Calculate
from parse_file import ParseFile
from report import Report


path = sys.argv[1] + "/"
parser = ParseFile()
generate_report = Report()

if __name__ == '__main__':
    for operation, report in zip(sys.argv[2::2], sys.argv[3::2]):  # Read multiple reports
        readings = parser.parse(operation, report.split("/"), path)
        if not readings:
            print("Sorry data for " + report + " does not exist")
        else:
            calculation = Calculate(readings)
            if operation == '-e':
                max_temp, min_temp, max_humidity = calculation.year_calculation()
                generate_report.year_report(max_temp, min_temp, max_humidity)
            elif operation == '-a':
                avg_highest_temp, avg_lowest_temp, avg_mean_humidity = calculation.month_calculation()
                generate_report.month_report(avg_highest_temp, avg_lowest_temp, avg_mean_humidity)
            else:
                max_temp, min_temp = calculation.day_calculation()
                generate_report.day_report(max_temp, min_temp)
