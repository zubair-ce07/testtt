import argparse
import calendar

from wheatherman.datareader import DataReader
from wheatherman.presentation import Presentation
from wheatherman.reports import Reports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to files")
    parser.add_argument('-e', metavar='N')
    parser.add_argument('-a', metavar='N')
    parser.add_argument('-c', metavar='N')

    list_parameters = parser.parse_args()
    path = list_parameters.path + "Murree_weather_"
    report = Reports()
    reader = DataReader()
    print_report = Presentation()

    if list_parameters.e:
        year = list_parameters.e
        file_name = path + year + "_*.txt"
        wheather_data = reader.extract_year(file_name)
        report.maximum_temperature_report(wheather_data)
        print_report.maximum_temperature(report)

    if list_parameters.a:
        year_month = list_parameters.a.split('/')
        year = year_month[0]
        month = year_month[1]
        month = calendar.month_name[int(month)]
        month = month[0:3]
        file_name = path + year + "_" + month + ".txt"
        wheather_data = reader.extract_monthly(file_name)
        report.average_temperature_report(wheather_data)
        print_report.average_report(report)

    if list_parameters.c:
        year_month = list_parameters.c.split('/')
        year = year_month[0]
        month = year_month[1]
        month = calendar.month_name[int(month)]
        month = month[0:3]
        file_name = path + year + "_" + month + ".txt"
        wheather_data = reader.extract_monthly(file_name)
        report.barchart_report(wheather_data)
        print_report.barchart(report)
        #     report.print_barchart()
        #     report.report_bonus(file_name)


if __name__ == '__main__':
    main()
