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



def main():
    "Main function of this program"
    parser = argparse.ArgumentParser()
    parser.add_argument("R", help="input the report number")
    parser.add_argument("filepath", help="input the path that contains data files")
    args = parser.parse_args()
    try:
        os.chdir(args.filepath)
        files = glob.glob("*.txt")
    except OSError:
        print("The directory path is not valid")
    reportnumber = int(args.R)
    for file_ in files:
            year = (int(filter(str.isdigit, file_)))
            date = ''
            if (reportnumber==1):
                with open(file_) as f:
                    data = csv.DictReader(f)
                    max_temp_data = []
                    min_temp_data = []
                    max_humid_data = []
                    min_humid_data = []
                    for row in data:
                        if row.get('Max TemperatureC'):
                            max_temp_data.append(row.get('Max TemperatureC'))
                        if row.get('Min TemperatureC'):
                            min_temp_data.append(row.get('Min TemperatureC'))
                        if row.get('Max Humidity'):
                            max_humid_data.append(row.get('Max Humidity'))
                        if row.get('Max Humidity'):
                            min_humid_data.append(row.get(' Min Humidity'))
                    if max_temp_data:
                        maxtemp = max(max_temp_data)
                    else:
                        maxtemp="N/A"
                    if min_temp_data:
                        mintemp = min(min_temp_data)
                    else:
                        mintemp = "N/A"
                    if max_humid_data:
                        maxhumid = max(max_humid_data)
                    else:
                        maxhumid = "N/A"
                    if min_humid_data:
                        minhumid = min(min_humid_data)
                    else:
                        minhumid = "N/A"
                if year in _stats:
                    data = _stats[year]
                    if (maxtemp > data['maxtemp']):
                        (_stats[year])['maxtemp'] = maxtemp
                    if (mintemp < data['mintemp']):
                        (_stats[year])['mintemp'] = mintemp
                    if (maxhumid > data['maxhumid']):
                        (_stats[year])['maxhumid'] = maxhumid
                    if (minhumid < data['minhumid']):
                        (_stats[year])['minhumid'] = minhumid

                else:
                    temp = dict()
                    temp['maxtemp'] = maxtemp
                    temp['mintemp'] = mintemp
                    temp['maxhumid'] = maxhumid
                    temp['minhumid'] = minhumid
                    temp['date'] = date
                    _stats[year] = temp
            elif(reportnumber==2):
                with open(file_) as f:
                    data = csv.DictReader(f)
                    maxtemp = -100
                    date = ''
                    for row in data:
                        temp_value = row.get('Max TemperatureC')
                        if temp_value:
                            if (temp_value > maxtemp):
                                maxtemp = temp_value
                                date = row.get('PKT')
                    if year in _stats:
                        data = _stats[year]
                        if (maxtemp > data['maxtemp']):
                            (_stats[year])['maxtemp'] = maxtemp
                    else:
                        temp = dict()
                        temp['maxtemp'] = maxtemp
                        temp['date'] = date
                        _stats[year] = temp


    display(reportnumber)


if __name__ == "__main__":
    main()


