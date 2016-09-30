import sys

import os

# class to save record of whole year in object oriented way


class TempratureReport:
    date = ""
    maxTemprature = 0
    minTemprature = 0
    humidity = 0

    def __init__(self, date, max_temp, min_temp, humid):
        self.date = date
        self.maxTemperature = max_temp
        self.minTemperature = min_temp
        self.humidity = humid
# class temperature report ends here


class WeatherMan:
    @staticmethod
    def yearly_report(filelist):
        temprecord = []
        for file in filelist:
            if os.path.isfile(filePathArg + "/" + file):
                f = open(filePathArg + "/" + file, 'r')  # opening file
                line = f.readline()  # skiping 1st line containg empty space
                line = f.readline()  # skipping header line
                for line in f:
                    if line.startswith("<!"):  # skip last line
                        line = ""
                    else:
                        lineElement = line.split(',')  # split on ,
                        if lineElement[1] == '':  # in case reading not taken
                            lineElement[1] = 0
                        # if lineElement[3]=='': never use will change mintemp
                        #    lineElement[3]=0
                        if lineElement[7] == '':  # in case reading not taken
                            lineElement[7] = 0
                        # save 365 records in list
                        temprecord.append(
                            TempratureReport(lineElement[0],
                                             int(lineElement[1]),
                                             lineElement[3],
                                             int(lineElement[7]))
                        )

                hightemp = 0
                hightempdate = ""
                for temp in temprecord:  # iterating through each object
                    if (temp.maxTemperature >= hightemp):
                        hightemp = temp.maxTemperature
                        hightempdate = temp.date
                datetomonth = hightempdate.split('-')
                monthofHighest = int(datetomonth[1])
                dayofHighest = datetomonth[2]
        print("Highest: "+str(hightemp) +
              "C on " + year_month[monthofHighest-1] + " "+str(dayofHighest))

        lowtemp = 40            # random value just to compare mintemp
        lowtempdate = ""
        for temp in temprecord:
                if temp.minTemperature != '':
                    if (int(temp.minTemperature) <= int(lowtemp)):
                        lowtemp = temp.minTemperature
                        lowtempdate = temp.date
        datetomonth = lowtempdate.split('-')
        monthoflowest = int(datetomonth[1])
        dayoflowest = datetomonth[2]
        print("Lowest: " + str(lowtemp) + "C on " +
              year_month[monthoflowest - 1] + " " +
              str(dayoflowest))

        mosthumidity = 0
        mostHumidDay = ""
        for temp in temprecord:
                    if int(temp.humidity) >= int(mosthumidity):
                        mosthumidity = temp.humidity
                        mostHumidDay = temp.date
        datetomonth = mostHumidDay.split('-')
        monthofhumidity = int(datetomonth[1])
        dayofhumidity = datetomonth[2]
        print("Humidity: " + str(mosthumidity) +
              "% on " + year_month[monthofhumidity - 1] +
              " " + str(dayofhumidity))

    def monthly_report(self, filename):
        if (os.path.isfile(filePathArg + "/" + filename)):
            f = open(filePathArg + "/" + filename, 'r')
            highest_average_Array = []
            lowest_average_Array = []
            average_mean_humidity = []

            line = f.readline()
            line = f.readline()

            for line in f:
                if line.startswith("<!"):
                    line = ""
                else:
                    lineElement = line.split(',')
                    if lineElement[1] != '':
                        highest_average_Array.append(int(lineElement[1]))
                    if lineElement[3] != '':
                        lowest_average_Array.append(int(lineElement[3]))
                    if lineElement[8] != '':
                        average_mean_humidity.append(int(lineElement[8]))
            # calculating average
            highest_average = \
                int(sum(highest_average_Array) / len(highest_average_Array))
            lowest_average = \
                int(sum(lowest_average_Array) / len(lowest_average_Array))
            average_mean_humidity = \
                int(sum(average_mean_humidity) / len(average_mean_humidity))

            # printing
            print("Highest Average: " + str(highest_average) + "C")
            print("Lowest Average : " + str(lowest_average) + "C")
            print ("Average Mean Humidity: " +
                   str(average_mean_humidity) + "%")

    def chart_report(self, filename):
        if (os.path.isfile(filePathArg + "/" + filename)):
            f = open(filePathArg + "/" + filename, 'r')
            line = f.readline()
            line = f.readline()
            bluetext = ""
            redtext = ""
            day = 1
            for line in f:
                redtext = ""
                bluetext = ""
                if line.startswith("<!"):
                    line = ""
                else:
                    lineElement = line.split(',')  # reading not taken
                    if lineElement[1] != '':
                        highest_temp = lineElement[1]
                        for i in range(0, int(highest_temp)):
                            redtext += "+"
                        red_color_bar = "\033[1;31m" + redtext + "\033[1;m"
                        print(str(day) + red_color_bar + highest_temp)

                    if lineElement[3] != '':
                        lowest_temp = lineElement[3]
                        for i in range(0, int(lowest_temp)):
                            bluetext += "+"
                        blueColorBar = "\033[1;34m" + bluetext + "\033[1;m"
                        print(str(day) + blueColorBar + lowest_temp)
                    day += 1
            return

    def oneLine_chart_report(self, filename):
        if (os.path.isfile(filePathArg + "/" + filename)):
            f = open(filePathArg + "/" + filename, 'r')
            highest_temp = ""
            lowest_temp = ""
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
                    lineElement = line.split(',')  # reading not taken
                    if (lineElement[1] != ''):
                        highest_temp = lineElement[1]

                        for i in range(0, int(highest_temp)):
                            redtext += "+"
                        red_color_bar = "\033[1;31m" + redtext + "\033[1;m"
                    if (lineElement[3] != ''):
                        lowest_temp = lineElement[3]
                        for i in range(0, int(lowest_temp)):
                            bluetext += "+"
                        blueColorBar = "\033[1;34m" + bluetext + "\033[1;m"
                        print(str(day) + blueColorBar + red_color_bar +
                              lowest_temp + "-" + highest_temp)
                    day += 1

            return

if len(sys.argv) < 4:
    print ("Arguments are not valid")

    # more detail of error
    if len(sys.argv) == 3:
        print ("filename may be missing")
        sys.exit()
    else:
        if len(sys.argv) == 2:
            print ("date and filename missing")
            sys.exit()
        else:
            if len(sys.argv) == 1:
                print ("report type,date and filename missing")
                sys.exit()
report_type = ""
year = ""
month = ""
day = ""
year_month = ["Jan", "Feb", "Mar", "Apr",
              "May", "Jun", "Jul", "Aug",
              "Sep", "Oct", "Nov", "Dec"
              ]
filePathArg = str(sys.argv[3])
if len(sys.argv) == 1:  # in case user run program from ide
    report_type = raw_input("Please enter flag value: ")  # manual input
else:
    report_type = str(sys.argv[1])  # value commoing from cmd

if report_type == "-e":
    year = str(sys.argv[2])                          # calculating year
    if len(sys.argv[2].split('/')) > 1:
        print ("invalid arguments")
        sys.exit()
    if int(year) > 2011:
        print("record not found for this year")
        sys.exit()
    if int(year) < 1996:
        print("record not found for this year")
        sys.exit()
    filelist = []  # if year is givencalclate from (12 files)list
    for month in year_month:
        fileprfix = "lahore_weather_" + year +\
                    "_"+month+".txt"  # creating file name
        filelist.append(fileprfix)
    WeatherMan().yearly_report(filelist)    # passing list of files to function

else:
    if report_type == "-a":                      # monthly report
        yearPlusMonth = str(sys.argv[2]).split('/')
        if len(yearPlusMonth) < 2:
            print("invalid month")
            sys.exit()
        year = yearPlusMonth[0]
        month = int(yearPlusMonth[1])
        if month > 12:
            print("invalid month")
            sys.exit()
        if month < 1:
            print("invalid month")
            sys.exit()
        filename = "lahore_weather_" + year + "_" + \
                   str(year_month[(month-1)]) + ".txt"
        WeatherMan().monthly_report(filename)

    else:
        if report_type == "-c":
            yearPlusMonth = str(sys.argv[2]).split('/')
            if len(yearPlusMonth) < 2:
                print("invalid month")
                sys.exit()
            year = yearPlusMonth[0]
            month = int(yearPlusMonth[1])
            if month > 12:
                print("invalid month")
                sys.exit()
            if month < 1:
                print("invalid month")
                sys.exit()
            filename = "lahore_weather_" +\
                       year + "_" + \
                       str(year_month[(month - 1)]) + \
                       ".txt"
            print(str(year_month[(month - 1)]) + " "+year)
            WeatherMan().chart_report(filename)
        else:
            if report_type == "-c4":
                yearPlusMonth = str(sys.argv[2]).split('/')
                if len(yearPlusMonth) < 2:
                    print("invalid month")
                    sys.exit()
                year = yearPlusMonth[0]
                month = int(yearPlusMonth[1])
                if month > 12:
                    print("invalid month")
                    sys.exit()
                if month < 1:
                    print("invalid month")
                    sys.exit()
                filename = "lahore_weather_" + \
                           year + "_" + \
                           str(year_month[(month - 1)]) + \
                           ".txt"
                print(str(year_month[(month - 1)]) + " " + year)
                WeatherMan().oneLine_chart_report(filename)
            else:
                print ("invalid arguments")
                sys.exit()
