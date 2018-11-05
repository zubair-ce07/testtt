import re
import argparse
from os import path
from datetime import datetime
from glob import glob

from file_reader import read_weather_data
import report
from output import display_monthly_report
from output import display_monthly_graph
from output import display_yearly_report


def main():
    """Driver function for the weatherman program"""

    parser = argparse.ArgumentParser(
        description='WeatherMan: Display monthly or yearly weather reports')
    parser.add_argument('files_path', metavar='path',
                        type=str, help='Path to weather files')

    parser.add_argument('-a',
                        type=str,
                        help='Display the average highest temperature, average\
                            lowest temperature, average mean humidity.',
                        nargs='*'    
                        )
    parser.add_argument('-e',
                        type=str,
                        help='Display the highest temperature and day, lowest\
                            temperature and day, most humid day and humidity',
                        nargs='*'
                        )
    parser.add_argument('-c',
                        type=str,
                        help='Display two horizontal bar charts on the console for\
                            the highest and lowest temperature on each day.\
                            Highest in red and lowest in blue.',
                        nargs='*'
                        )
    args = parser.parse_args()
    files_directory = args.files_path
    files_directory = path.expanduser(files_directory)

    get_list = lambda l : l if l else []

    for specs in get_list(args.a):
        specs = parse_year_month(specs)
        year = specs.year
        month_name = specs.strftime('%b')
        files = find_files(files_directory, year, month_name)
        if files:
            create_monthly_reports(specs, files)

    for specs in get_list(args.c):
        specs = parse_year_month(specs)
        year = specs.year
        month_name = specs.strftime('%b')
        files = find_files(files_directory, year, month_name)
        if files:
            create_monthly_graphs(specs, files)
    
    for specs in get_list(args.e):
        specs = parse_year(specs)
        year = specs.year
        files = find_files(files_directory, year)
        if files:
            create_yearly_reports(specs, files)


def create_monthly_reports(report_specs, files):
    """manage the reports requested with -a tag"""
    monthly_record = read_weather_data(files)
    result = report.calculate_monthly_report(monthly_record)
    display_monthly_report(result, report_specs)


def create_monthly_graphs(report_specs, files):
    """manage the reports requested with -c tag"""
    monthly_record = read_weather_data(files)
    result = report.calculate_monthly_graph(monthly_record)
    display_monthly_graph(result, report_specs)


def create_yearly_reports(report_specs, files):
    """manage the reports requested with -e tag"""
    yearly_record = read_weather_data(files)
    result = report.calculate_yearly_report(yearly_record)
    display_yearly_report(result, report_specs)


def parse_year_month(report_specs):
    try:
        return datetime.strptime(report_specs, '%Y/%m')
    except ValueError:
        print("\nIncorrect data format, should be YYYY/MM\n")
        raise


def parse_year(report_specs):
    try:
        return datetime.strptime(report_specs, '%Y')
    except:
        print("\nIncorrect data format, should be YYYY\n")
        raise


def find_files(files_dir, year, month='*'):
    file_path = f'{files_dir}/*{year}_{month}.txt'
    found_files = glob(file_path)
    if found_files:
        return [file_name for file_name in found_files if path.isfile(file_name)]
    else:
        print('Error: File not found.')


if __name__ == '__main__':
    main()
