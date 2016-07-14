import os.path
import sys
import csv
import argparse

_date = '1993-8-2'
_maxTemp = -100
_minTemp = 100
_maxHumid = 0
_minHumid = 100
_stats = []
_hottestdays = []
parser = argparse.ArgumentParser()
parser.add_argument("R",help="input the report number")
parser.add_argument("filepath",help="input the path that contains data files")
args = parser.parse_args()

def display():
    "Displays the output of the report"
    print'{0} {1}'.format("This is report number: ",args.R)
    print("Year        MAX Temp        MIN Temp        MAX Humidity        MIN Humidity")
    print("--------------------------------------------------------------------------")
    for stat in _stats:
        print(stat)
    print("Year        Date          Temp")
    print("------------------------------")
    for hottestday in _hottestdays:
        print(hottestday)


def main():
    "Main function of this program"
    for year in range(1996,2011):
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        for month in months:
            if os.path.isfile(args.filepath+"lahore_weather_"+str(year)+"_"+month+".txt"):
                with open(args.filepath+"lahore_weather_"+str(year)+"_"+month+".txt") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if row['Max TemperatureC']:
                            if (int(row['Max TemperatureC']) > maxTemp):
                                date = row['PKT']
                                maxTemp = int(row['Max TemperatureC'])
                        if row['Min TemperatureC']:
                            if (int(row['Min TemperatureC']) < minTemp):
                                minTemp = int(row['Min TemperatureC'])
                        if row['Max Humidity']:
                            if (int(row['Max Humidity']) > maxHumid):
                                maxHumid = int(row['Max Humidity'])
                        if row['Min Humidity']:
                            if (int(row['Min Humidity']) < minHumid):
                                minHumid = int(row['Min Humidity'])
        _stats.append(str(year) + "        " + str(maxTemp) + "              " + str(minTemp) + "               " + str(maxHumid) + "                  " + str(minHumid))
        _hottestdays.append(str(year) + "        " + date + "     " + str(maxTemp))


if __name__ == "__main__": main()



