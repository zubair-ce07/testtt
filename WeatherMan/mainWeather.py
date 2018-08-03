import argparse
import calendar
import csv
import os

from calculaterecords import CalculateRecords
from printrecords import PrintRecords
from record import Record


def check_error(temp_str):
    if str(temp_str).strip() == '':
        return None
    return temp_str


def fill_data_structure(reader_dict, data):
    for row in reader_dict:
        if tuple(map(str.strip, [row.get('Max TemperatureC'), row.get('Min TemperatureC'),
                                 row.get('Max Humidity'), row.get(' Mean Humidity')])) == ('', '', '', ''):
            continue
        data.append(Record(row.get('PKT', row.get('PKST')),
                           check_error(row.get('Max TemperatureC')),
                           check_error(row.get('Min TemperatureC')),
                           check_error(row.get('Max Humidity')),
                           check_error(row.get(' Mean Humidity'))))


def compute_reader(directory, year, month=None):
    data = []
    files_path = os.getcwd() + directory
    files = [file for file in os.listdir(files_path) if year in file]
    if month:
        files = [file for file in files if calendar.month_abbr[int(month)] in file]
    for file in files:
        with open(files_path + file) as infile:
            reader = csv.DictReader(infile)
            fill_data_structure(reader, data)
    return data


def print_records(print_func, data, arg, cal_func=None):
    if not data:
        print('Invalid Year/Month, No record Found')
        return
    print_func(*cal_func(data), *arg.split('/')) if cal_func else print_func(data, *arg.split('/'))


def main():
    weather_man = argparse.ArgumentParser()
    weather_man.add_argument('dir', help='Provide the Folder name for weather files i.e. "/weatherfiles/"')
    weather_man.add_argument('-e', help='Yearly Results', nargs='*')
    weather_man.add_argument('-a', help='Monthly Average Results 2015/6', nargs='*')
    weather_man.add_argument('-c', help='Monthly Average Results 2015/6', nargs='*')
    args = weather_man.parse_args()
    for arg in args.e or []:
        record_data = compute_reader(args.dir, arg)
        print_records(PrintRecords.print_yearly_record, record_data, arg, cal_func=CalculateRecords.cal_yearly_report)
    for arg in args.a or []:
        record_data = compute_reader(args.dir, *arg.split('/'))
        print_records(PrintRecords.avg_monthly_record, record_data, arg, CalculateRecords.cal_monthly_report)
    for arg in args.c or []:
        record_data = compute_reader(args.dir, *arg.split('/'))
        print_records(PrintRecords.comparative_daily_record, record_data, arg)


if __name__ == "__main__":
    main()
