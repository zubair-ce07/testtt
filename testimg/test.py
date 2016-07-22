import csv
import argparse
import os
import glob

_stats = dict()

def display(reportnumber):
    "Displays the output of the report"
    number = int(reportnumber)
    if (number==1):
        print'{0} {1}'.format("This is report number: ",reportnumber)
        print("Year         MAX Temp         MIN Temp         MAX Humidity         MIN Humidity")
        print("--------------------------------------------------------------------------------")
        for key in _stats.keys():
            print'{0: <5}        {1: <5}               {2: <5}               {3: <5}                   {4: <5}'.format\
                (key,(_stats[key])["maxtemp"],(_stats[key])["mintemp"],(_stats[key])["maxhumid"],(_stats[key])["minhumid"])
    elif (number==2):
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
    except OSError:
        print("The directory path is not valid")

    for file_ in files:
            year = (int(filter(str.isdigit, file_)))
            date = ''
            with open(file_) as f:
                next(f)  # discard first row from file -- see notes
                max_row = max(csv.reader(f), key=lambda row: row[1])
                date = max_row[0]
                maxtemp = max_row[1]
                f.seek(0)
                next(f)
                maxhumid = max(row[7] for row in csv.reader(f))
                f.seek(0)
                next(f)
                values_temp = []
                for row in csv.reader(f):
                    if row[3]:
                        values_temp.append(row[3])
                if values_temp:
                    mintemp = min(values_temp)
                else:
                    mintemp = 'No data'
                f.seek(0)
                next(f)
                values_humid = []
                for row in csv.reader(f):
                    if row[3]:
                        values_humid.append(row[3])
                if values_humid:
                    minhumid = min(values_humid)
                else:
                    minhumid = 'No data'
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


if __name__ == "__main__":
    main()


