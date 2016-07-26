import csv
import argparse
import os
import glob
import sys

_stats = dict()

def display(report_number):
    "Displays the output of the report"
    if (report_number==1):
        print'{0} {1}'.format("This is report number: ", report_number)
        print("Year         MAX Temp         MIN Temp         MAX Humidity         MIN Humidity")
        print("--------------------------------------------------------------------------------")
        for key in _stats.keys():
            print'{0: <5}        {1: <5}               {2: <5}               {3: <5}                   {4: <5}'.format\
                (key,(_stats[key])["Max TemperatureC"],(_stats[key])["Min TemperatureC"],(_stats[key])["Max Humidity"],(_stats[key])[" Min Humidity"])
    elif (report_number==2):
            print'{0} {1}'.format("This is report number: ", report_number)
            print("Year          Date                 Temp")
            print("---------------------------------------")
            for key in _stats.keys():
                print'{0: <5}        {1: <10}              {2: <5}'.format(key,(_stats[key])["date"],(_stats[key])["maxtemp"])
    return


def min_or_max_key_value(list_of_dicts, key, min_or_max):
    "Function that returns the max value of a key from a list of dictionaries"
    seq = [x[key] for x in list_of_dicts if x[key] != '']
    if (min_or_max== 'min'):
        return min(seq) if seq else '200'
    elif (min_or_max== 'max'):
        return max(seq) if seq else '-200'


def Generate_report_one(files):
    "function to calculate all the statistics from the given files and generate report number one"
    for file_ in files:
        year = (int(filter(str.isdigit, file_)))
        with open(file_) as f:
            iteratable_dicts = csv.DictReader(f)
            list_of_dictionaries = list(iteratable_dicts)
            if year in _stats:
                list_of_dictionaries.append(_stats[year])
            min_temp = min_or_max_key_value(list_of_dictionaries, 'Min TemperatureC', 'min')
            max_temp = min_or_max_key_value(list_of_dictionaries, 'Max TemperatureC', 'max')
            min_humid = min_or_max_key_value(list_of_dictionaries, ' Min Humidity', 'min')
            max_humid = min_or_max_key_value(list_of_dictionaries, 'Max Humidity', 'max')
        temp_dict = {}
        temp_dict['Max TemperatureC'] = max_temp
        temp_dict['Min TemperatureC'] = min_temp
        temp_dict['Max Humidity'] = max_humid
        temp_dict[' Min Humidity'] = min_humid
        _stats[year] = temp_dict
    return


def Generate_report_two(files):
    "function to calculate all the statistics from the given files and generate report number two"
    for file_ in files:
        year = (int(filter(str.isdigit, file_)))
        date = ''
        with open(file_) as f:
            iteratable_dictionaries = csv.DictReader(f)
            list_of_dictionaries = list(iteratable_dictionaries)
            if year in _stats:
                list_of_dictionaries.append(_stats[year])
            row_of_max_temp = max(list_of_dictionaries, key=lambda x: x.get('Max TemperatureC'))
            max_temp = row_of_max_temp['Max TemperatureC']
            date = row_of_max_temp.get('PKT') or row_of_max_temp.get('PKST')
            temp_dict = {}
            temp_dict['maxtemp'] = max_temp
            temp_dict['date'] = date
            _stats[year] = temp_dict
    return


def main():
    "Main function of this program"
    parser = argparse.ArgumentParser()
    parser.add_argument("R", help="input the report number")
    parser.add_argument("filepath", help="input the path that contains data files")
    args = parser.parse_args()
    try:
        os.chdir(args.filepath)
        files_found = glob.glob("*.txt")
    except OSError:
        print("The directory path is not valid")
        sys.exit(1)
    report_num = int(args.R)
    if (report_num == 1):
        Generate_report_one(files_found)
    elif (report_num == 2):
        Generate_report_two(files_found)
    display(report_num)


if __name__ == "__main__":
    main()


