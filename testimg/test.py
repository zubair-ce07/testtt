import os.path
import sys
Report = sys.argv[1]
path = sys.argv[2]
def NotEmpty(stri):
    "This checks if the character is empty"
    if (stri==''):
        return 0;
    else:
        return 1;
Stats= []
HottestDays = []
print("This is report number: "+Report)
years = ["1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011"]
for year in years:
    reportNumber=1
    date = '1993-8-2'
    maxTemp = -100
    minTemp = 100
    maxHumid = 0
    minHumid = 100
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    for month in months:
        if os.path.isfile(path+"lahore_weather_"+year+"_"+month+".txt"):
            data =  open(path+"lahore_weather_"+year+"_"+month+".txt")
            string = data.read()
            splitted= string.split("\n") 
            del splitted[1]
            del splitted[0]
            del splitted[len(splitted)-1]
            del splitted[len(splitted)-1]
            for day in splitted:
                daydata = day.split(",")
                if (NotEmpty(daydata[1])):
                    if (int(daydata[1])>maxTemp):
                        date=daydata[0]
                        maxTemp=int(daydata[1])
                if (NotEmpty(daydata[3])):
                    if (int(daydata[3]) < minTemp):
                        minTemp = int(daydata[3])
                if (NotEmpty(daydata[7])):
                    if (int(daydata[7]) > maxHumid):
                        maxHumid = int(daydata[7])
                if (NotEmpty(daydata[9])):
                    if (int(daydata[9]) < minHumid):
                        minHumid = int(daydata[9])
    Stats.append(year+"        "+str(maxTemp)+"              "+str(minTemp)+"               "+str(maxHumid)+"                  "+str(minHumid))
    HottestDays.append(year+"        "+date+"     "+str(maxTemp))
print("Year        MAX Temp        MIN Temp        MAX Humidity        MIN Humidity")
print("--------------------------------------------------------------------------")
for stat in Stats:
    print(stat)
print("Year        Date          Temp")
print("------------------------------")
for hottestday in HottestDays:
    print(hottestday)



