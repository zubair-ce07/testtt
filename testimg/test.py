import csv
import argparse
import os
import glob

_stats = dict()

def display(reportnumber):
    "Displays the output of the report"
    if (int(reportnumber)==1):
        print'{0} {1}'.format("This is report number: ",reportnumber)
        print("Year         MAX Temp         MIN Temp         MAX Humidity         MIN Humidity")
        print("--------------------------------------------------------------------------------")
        for key in _stats.keys():
            print'{0: <5}        {1: <5}               {2: <5}               {3: <5}                   {4: <5}'.format\
                (key,(_stats[key])["maxtemp"],(_stats[key])["mintemp"],(_stats[key])["maxhumid"],(_stats[key])["minhumid"])
    else:
        if (int(reportnumber)==2):
            print'{0} {1}'.format("This is report number: ", reportnumber)
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

        for file_ in files:
                year = (int(filter(str.isdigit, file_)))
                date = ''
                with open(file_) as f:
                    next(f)  # discard first row from file -- see notes
                    max_row = max(csv.reader(f), key=lambda row: row[1])
                    date = max_row[0]
                    maxtemp = max_row[1]
                with open(file_) as csvfile:
                    next(csvfile)
                    values = []
                    for row in csv.reader(csvfile):
                        if row[3]:
                            values.append(row[3])
                    if values:
                        mintemp = min(values)
                    else:
                        mintemp = 'No data'
                with open(file_) as csvfile:
                    next(csvfile)
                    values = []
                    for row in csv.reader(csvfile):
                        if row[3]:
                            values.append(row[3])
                    if values:
                        minhumid = min(values)
                    else:
                        minhumid = 'No data'
                with open(file_) as csvfile:
                    next(csvfile)
                    maxhumid = max(row[7] for row in csv.reader(csvfile))
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
        display(args.R)
    except OSError:
        print("The directory path is not valid")


if __name__ == "__main__":
    main()


