import sys

import os

#class to save record of whole year in object oriented way
class tempratureReport:
    date = ""
    maxTemprature = 0
    minTemprature = 0
    humidity = 0

    def __init__(self, date, maxTemp, minTemp, humid): #constructor to iitialize values when object will be created
        self.date = date
        self.maxTemperature = maxTemp
        self.minTemperature = minTemp
        self.humidity = humid
#class temprature report ends here
class weatherMan:
    def yearly_report(self,ilelist):
        # print(numberOfFiles) #uncomment to view all files name that will be used in report process
        temprecord=[]
        for file in filelist:
          if(os.path.isfile(filePathArg+"/"+file)):
            f=open(filePathArg+"/"+file, 'r')#opening file for processing
            line = f.readline() #skiping 1st line containg empty space
            line = f.readline() #skipping header line
            for line in f:
                if (line.startswith("<!")):#skip last line
                    line = ""
                else:
                    lineElement = line.split(',') #split on base of , to get values seperatly
                    if lineElement[1]=='':        #in case reading were not taken on that day
                       lineElement[1]=0
                    # if lineElement[3]=='':      3never use this this will change our mintemp
                    #    lineElement[3]=0
                    if lineElement[7] == '':      #in case reading were not taken on that day
                        lineElement[7] = 0
                    # save 365 records in list
                    temprecord.append(
                        tempratureReport(lineElement[0],int(lineElement[1]),
                                         lineElement[3],int(lineElement[7]))
                                        )

            hightemp=0
            hightempdate=""
            for temp in temprecord:     #iterating through each object to get max temp and the day it was calculated
                if(temp.maxTemperature>=hightemp):
                    hightemp=temp.maxTemperature
                    hightempdate=temp.date
            dateTomonth=hightempdate.split('-')
            monthofHighest=int(dateTomonth[1])
            dayofHighest=dateTomonth[2]
        print("Highest: "+str(hightemp)+"C on "+year_month[monthofHighest-1]+" "+str(dayofHighest))

        lowtemp = 40                            #random value just to compare mintemp
        lowtempdate = ""
        for temp in temprecord:
                if(temp.minTemperature != ''):
                    if (int(temp.minTemperature) <= int(lowtemp)):
                        lowtemp = temp.minTemperature
                        lowtempdate = temp.date
        dateTomonth = lowtempdate.split('-')
        monthoflowest = int(dateTomonth[1])
        dayoflowest = dateTomonth[2]
        print("Lowest: " + str(lowtemp) + "C on " + year_month[monthoflowest - 1] + " " + str(dayoflowest))

        mosthumidity = 0
        mostHumidDay = ""
        for temp in temprecord:
                    if (int(temp.humidity) >= int(mosthumidity)):
                        mosthumidity = temp.humidity
                        mostHumidDay = temp.date
        dateTomonth = mostHumidDay.split('-')
        monthofhumidity = int(dateTomonth[1])
        dayofhumidity = dateTomonth[2]
        print("Humidity: " + str(mosthumidity) + "% on " + year_month[monthofhumidity - 1] + " " + str(dayofhumidity))

    #yearly calculation ends here
    def monthly_report(self,filename):
       if (os.path.isfile(filePathArg + "/" + filename)):
        f = open(filePathArg+"/"+filename, 'r')
        Highest_Average=""
        Lowest_Average=""
        Average_Mean_Humidity=""
        highest_Average_Array=[]
        lowest_Average_Array =[]
        average_mean_humidity=[]

        line = f.readline()
        line=f.readline()

        for line in f:
                    if(line.startswith("<!")):
                        line=""
                    else:
                            lineElement = line.split(',')
                            if(lineElement[1]!=''):
                                highest_Average_Array.append(int(lineElement[1]))
                            if (lineElement[3] != ''):
                                lowest_Average_Array.append(int(lineElement[3]))
                            if (lineElement[8] != ''):
                                average_mean_humidity.append(int(lineElement[8]))
        #calculating average
        Highest_Average =int(sum(highest_Average_Array)/len(highest_Average_Array))
        Lowest_Average = int(sum(lowest_Average_Array) / len(lowest_Average_Array))
        Average_Mean_Humidity = int(sum(average_mean_humidity) / len(average_mean_humidity))

        #printing
        print("Highest Average: "+str(Highest_Average)+"C")
        print("Lowest Average : "+str(Lowest_Average)+"C")
        print ("Average Mean Humidity: "+str(Average_Mean_Humidity)+"%")

        return;



    def chart_report(self,filename):
      if (os.path.isfile(filePathArg + "/" + filename)):
        f = open(filePathArg + "/" + filename, 'r')
        Highest_Temp= ""
        Lowest_Temp = ""
        line = f.readline()
        line = f.readline()
        bluetext=""
        redtext=""
        day=1
        for line in f:
                    redtext=""
                    bluetext = ""
                    if(line.startswith("<!")):
                        line=""
                    else:
                            lineElement = line.split(',') #in case reading were not taken
                            if(lineElement[1]!=''):
                                Highest_Temp=lineElement[1]
                                for i in range(0,int(Highest_Temp)):
                                  redtext+="+"
                                redColorBar = "\033[1;31m" + redtext + "\033[1;m"
                                print(str(day)+redColorBar+Highest_Temp)

                            if(lineElement[3]!=''):
                                Lowest_Temp = lineElement[3]
                                for i in range(0,int(Lowest_Temp)):
                                    bluetext+="+"
                                blueColorBar ="\033[1;34m"+bluetext+"\033[1;m"
                                print(str(day)+blueColorBar+Lowest_Temp)
                            day+=1
        return;

    def OneLine_chart_report(self,filename):
     if (os.path.isfile(filePathArg + "/" + filename)):
        f = open(filePathArg + "/" + filename, 'r')
        Highest_Temp = ""
        Lowest_Temp = ""
        line = f.readline()
        line = f.readline()
        bluetext = ""
        redtext = ""
        day = 1
        for line in f:
            redtext = ""
            bluetext = ""
            if (line.startswith("<!")):
                line = ""
            else:
                lineElement = line.split(',')  # in case reading were not taken
                if (lineElement[1] != ''):
                    Highest_Temp = lineElement[1]

                    for i in range(0, int(Highest_Temp)):
                        redtext += "+"
                    redColorBar = "\033[1;31m" + redtext + "\033[1;m"
                if (lineElement[3] != ''):
                    Lowest_Temp = lineElement[3]
                    for i in range(0, int(Lowest_Temp)):
                        bluetext += "+"
                    blueColorBar = "\033[1;34m" + bluetext + "\033[1;m"
                    print(str(day) +blueColorBar+ redColorBar + Lowest_Temp+"-"+Highest_Temp)
                day += 1

        return ;

if(len(sys.argv)<4):
    print ("Argements are not valid")

    #more detail of error
    if(len(sys.argv)==3):
        print ("filename may be missing")
        sys.exit()
    else:
        if(len(sys.argv)==2):
            print ("date and filename missing")
            sys.exit()
        else:
            if(len(sys.argv)==1):
                print ("report type,date and filename missing")
                sys.exit()
report_type = ""
year=""
month=""
day=""
year_month=["Jan","Feb","Mar","Apr",
            "May","Jun","Jul","Aug",
            "Sep","Oct","Nov","Dec"
            ]
filePathArg =str(sys.argv[3])
#"/home/ayyaz/Desktop/weatherdata"
if (len(sys.argv) == 1): #in case user run program from ide
    report_type = raw_input("Please enter flag value: ")  # manually taking input
else:
    report_type = str(sys.argv[1])  # value commoing from cmd

if (report_type == "-e"):
    year=str(sys.argv[2])                          #calculating year
    if(len(sys.argv[2].split('/'))>1):
        print ("invalid arguments")
        sys.exit()
    if(int(year)>2011):
        print("record not found for this year")
        sys.exit()
    if (int(year) <1996):
        print("record not found for this year")
        sys.exit()
    filelist=[]                                    #if year is given system will calclate from (12 files)list
    for month in year_month:
        fileprfix="lahore_weather_"+year+"_"+month+".txt" #creating file name with user entered arguments
        filelist.append(fileprfix)
    weatherMan().yearly_report(filelist)                     #passing list of files to function

else:
    if (report_type == "-a"):                      #monthly report
        yearPlusMonth=str(sys.argv[2]).split('/')
        if ((len(yearPlusMonth) < 2)):
            print("invalid month")
            sys.exit()
        year=yearPlusMonth[0]
        month=int(yearPlusMonth[1])
        if(month>12):
            print("invalid month")
            sys.exit()
        if (month < 1):
            print("invalid month")
            sys.exit()
        filename = "lahore_weather_" + year+ "_"+ str(year_month[(month-1)])+ ".txt"
        weatherMan().monthly_report(filename)

    else:
        if (report_type == "-c"):
            yearPlusMonth = str(sys.argv[2]).split('/')
            if((len(yearPlusMonth)<2)):
                print("invalid month")
                sys.exit()
            year = yearPlusMonth[0]
            month = int(yearPlusMonth[1])
            if (month > 12):
                print("invalid month")
                sys.exit()
            if (month < 1):
                print("invalid month")
                sys.exit()
            filename = "lahore_weather_" + year + "_" + str(year_month[(month - 1)]) + ".txt"
            print(str(year_month[(month - 1)])+" "+year)
            weatherMan().chart_report(filename)
        else:
            if (report_type == "-c4"):
                yearPlusMonth = str(sys.argv[2]).split('/')
                if ((len(yearPlusMonth) < 2)):
                    print("invalid month")
                    sys.exit()
                year = yearPlusMonth[0]
                month = int(yearPlusMonth[1])
                if (month > 12):
                    print("invalid month")
                    sys.exit()
                if (month < 1):
                    print("invalid month")
                    sys.exit()
                filename = "lahore_weather_" + year + "_" + str(year_month[(month - 1)]) + ".txt"
                print(str(year_month[(month - 1)]) + " " + year)
                weatherMan().OneLine_chart_report(filename)
            else:
                print ("invalid arguments")
                sys.exit()
