import os.path
import sys
import csv
import argparse

__date__ = '1993-8-2'
__maxTemp__ = -100
__minTemp__ = 100
__maxHumid__ = 0
__minHumid__ = 100
__stats__ = []
__hottestdays__ = []
parser = argparse.ArgumentParser()
parser.add_argument("R",help="input the report number")
parser.add_argument("filepath",help="input the path that contains data files")
args = parser.parse_args()

def display():
    "Displays the output of the report"
    print'{0} {1}'.format("This is report number: ",args.R)
    print("Year        MAX Temp        MIN Temp        MAX Humidity        MIN Humidity")
    print("--------------------------------------------------------------------------")
    for stat in __stats__:
        print(stat)
    print("Year        Date          Temp")
    print("------------------------------")
    for hottestday in __hottestdays__:
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
                        if not row['Max TemperatureC']:
                            if (int(row['Max TemperatureC']) > maxTemp):
                                date = row['PKT']
                                maxTemp = int(row['Max TemperatureC'])
                        if not row['Min TemperatureC']:
                            if (int(row['Min TemperatureC']) < minTemp):
                                minTemp = int(row['Min TemperatureC'])
                        if not row['Max Humidity']:
                            if (int(row['Max Humidity']) > maxHumid):
                                maxHumid = int(row['Max Humidity'])
                        if not row['Min Humidity']:
                            if (int(row['Min Humidity']) < minHumid):
                                minHumid = int(row['Min Humidity'])
        __stats__.append(str(year) + "        " + str(maxTemp) + "              " + str(minTemp) + "               " + str(maxHumid) + "                  " + str(minHumid))
        __hottestdays__.append(str(year) + "        " + date + "     " + str(maxTemp))


if __name__ == "__main__": main()



