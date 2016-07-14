import os.path
import sys
import csv
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("R",help="input the report number")
parser.add_argument("filepath",help="input the path that contains data files")
args = parser.parse_args()


def NotEmpty(stri):
    "This checks if the character is empty"
    if (stri==''):
        return 0;
    else:
        return 1;


def main():
    "Main function of this program"
    Stats= []
    HottestDays = []
    print("This is report number: "+args.R)
    for year in range(1996,2011):
        reportNumber=1
        date = '1993-8-2'
        maxTemp = -100
        minTemp = 100
        maxHumid = 0
        minHumid = 100
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        for month in months:
            if os.path.isfile(args.filepath+"lahore_weather_"+str(year)+"_"+month+".txt"):
                with open(args.filepath+"lahore_weather_"+str(year)+"_"+month+".txt") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if (NotEmpty(row['Max TemperatureC'])):
                            if (int(row['Max TemperatureC']) > maxTemp):
                                date = row['PKT']
                                maxTemp = int(row['Max TemperatureC'])
                        if (NotEmpty(row['Min TemperatureC'])):
                            if (int(row['Min TemperatureC']) < minTemp):
                                minTemp = int(row['Min TemperatureC'])
                        if (NotEmpty(row['Max Humidity'])):
                            if (int(row['Max Humidity']) > maxHumid):
                                maxHumid = int(row['Max Humidity'])
                        if (NotEmpty(row['Min Humidity'])):
                            if (int(row['Min Humidity']) < minHumid):
                                minHumid = int(row['Min Humidity'])
        Stats.append(str(year)+"        "+str(maxTemp)+"              "+str(minTemp)+"               "+str(maxHumid)+"                  "+str(minHumid))
        HottestDays.append(str(year)+"        "+date+"     "+str(maxTemp))
    print("Year        MAX Temp        MIN Temp        MAX Humidity        MIN Humidity")
    print("--------------------------------------------------------------------------")
    for stat in Stats:
        print(stat)
    print("Year        Date          Temp")
    print("------------------------------")
    for hottestday in HottestDays:
        print(hottestday)
    return 0;


main()



