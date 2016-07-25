import csv
import argparse
import os
import glob

_stats = dict()

def display(number):
    "Displays the output of the report"
    if (number==1):
        print'{0} {1}'.format("This is report number: ",number)
        print("Year         MAX Temp         MIN Temp         MAX Humidity         MIN Humidity")
        print("--------------------------------------------------------------------------------")
        for key in _stats.keys():
            print'{0: <5}        {1: <5}               {2: <5}               {3: <5}                   {4: <5}'.format\
                (key,(_stats[key])["maxtemp"],(_stats[key])["mintemp"],(_stats[key])["maxhumid"],(_stats[key])["minhumid"])
    elif (number==2):
            print'{0} {1}'.format("This is report number: ", number)
            print("Year          Date                 Temp")
            print("---------------------------------------")
            for key in _stats.keys():
                print'{0: <5}        {1: <10}              {2: <5}'.format(key,(_stats[key])["date"],(_stats[key])["maxtemp"])

def min_max_key(list_of_dicts,key,type):

    seq = [x[key] for x in list_of_dicts if x[key] != '']
    if (type=='min'):
        if seq:
            return min(seq)
        else:
            return '200'
    elif (type=='max'):
        if seq:
            return max(seq)
        else:
            return '-200'

def calculate_statistics(files,reportnumber):
    "function to calculates all the statistics from the given files"
    for file_ in files:
        year = (int(filter(str.isdigit, file_)))
        date = ''
        if (reportnumber == 1):
            with open(file_) as f:
                data = csv.DictReader(f)
                list_of_dicts = list(data)
                min_temp = min_max_key(list_of_dicts, 'Min TemperatureC', 'min')
                max_temp = min_max_key(list_of_dicts, 'Max TemperatureC', 'max')
                min_humid = min_max_key(list_of_dicts, ' Min Humidity', 'min')
                max_humid = min_max_key(list_of_dicts, 'Max Humidity', 'max')
            if year in _stats:
                data = _stats[year]
                if (max_temp > data['maxtemp']):
                    (_stats[year])['maxtemp'] = max_temp
                if (min_temp < data['mintemp']):
                    (_stats[year])['mintemp'] = min_temp
                if (max_humid > data['maxhumid']):
                    (_stats[year])['maxhumid'] = max_humid
                if (min_humid < data['minhumid']):
                    (_stats[year])['minhumid'] = min_humid

            else:
                temp = dict()
                temp['maxtemp'] = max_temp
                temp['mintemp'] = min_temp
                temp['maxhumid'] = max_humid
                temp['minhumid'] = min_humid
                temp['date'] = date
                _stats[year] = temp
        elif (reportnumber == 2):
            with open(file_) as f:
                data = csv.DictReader(f)
                dicts = list(data)
                dict_ = max(dicts, key=lambda x: x.get('Max TemperatureC'))
                max_temp = dict_['Max TemperatureC']
                date = dict_.get('PKT')
                if year in _stats:
                    data = _stats[year]
                    if (max_temp > data['maxtemp']):
                        (_stats[year])['maxtemp'] = max_temp
                else:
                    temp = dict()
                    temp['maxtemp'] = max_temp
                    temp['date'] = date
                    _stats[year] = temp
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
    reportnum = int(args.R)
    calculate_statistics(files_found,reportnum)
    display(reportnum)


if __name__ == "__main__":
    main()


