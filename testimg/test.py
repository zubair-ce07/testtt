import csv
import argparse
import os
import glob

_stats = dict()

def display(reportnumber):
    "Displays the output of the report"
    print'{0} {1}'.format("This is report number: ",reportnumber)
    print("Year        MAX Temp        MIN Temp        MAX Humidity        MIN Humidity")
    print("--------------------------------------------------------------------------")
    for key in _stats.keys():
        print'{0}        {1}               {2}               {3}                   {4}'.format\
            (key,(_stats[key])["maxtemp"],(_stats[key])["mintemp"],(_stats[key])["maxhumid"],(_stats[key])["minhumid"])
    print("Year        Date          Temp")
    print("------------------------------")
    for key in _stats.keys():
        print'{0}        {1}              {2}'.format(key,(_stats[key])["date"],(_stats[key])["maxtemp"])


def main():
    "Main function of this program"
    parser = argparse.ArgumentParser()
    parser.add_argument("R", help="input the report number")
    parser.add_argument("filepath", help="input the path that contains data files")
    args = parser.parse_args()
    os.chdir(args.filepath)
    files = glob.glob("*.txt")

    for file in files:
            year = (int(filter(str.isdigit, file)))
            with open(file) as csvfile:
                reader = csv.DictReader(csvfile)
                date =''
                maxtemp = -100
                mintemp = 100
                maxhumid = 0
                minhumid = 100
                for row in reader:
                    if row.get('Max TemperatureC'):
                        if (int(row['Max TemperatureC']) > maxtemp):
                            date = row.get('PKT')
                            maxtemp = int(row['Max TemperatureC'])
                    if row.get('Min TemperatureC'):
                        if (int(row['Min TemperatureC']) < mintemp):
                            mintemp = int(row['Min TemperatureC'])
                    if row.get('Max Humidity'):
                        if (int(row['Max Humidity']) > maxhumid):
                            maxhumid = int(row['Max Humidity'])
                    if row.get('Min Humidity'):
                        if (int(row['Min Humidity']) < minhumid):
                            minhumid = int(row['Min Humidity'])
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


