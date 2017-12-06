import glob
import os
import datetime
import calendar
import sys


class ForecastReport:
    max_temp = 0
    min_temp = 0
    max_hum = 0
    max_date = ""
    min_date = ""
    hum_date = ""
    max_mean = 0
    min_mean = 0
    avg_hum = 0
    file_path = "/home/dawood/Downloads/weatherfiles/" \
                "weatherfiles/Murree_weather_"

    def generate_report(self, year_month, report_type):
        lst_yearmon = year_month.split("/")
        if report_type == "-e":
            file_name = self.file_path+lst_yearmon[0]+"_*.txt"
            self.find_max_temp(file_name)
            self.print_max()
        elif report_type == "-a":
            mon = calendar.month_name[int(lst_yearmon[1])]
            mon = mon[0:3]
            file_name = self.file_path+lst_yearmon[0]+"_"+mon+".txt"
            self.report_mean(file_name)
            self.print_average()
        elif report_type == "-c":
            mon = calendar.month_name[int(lst_yearmon[1])]
            mon = mon[0:3]
            file_name = self.file_path + lst_yearmon[0] + "_" + mon + ".txt"
            self.report_barchart(file_name)
            self.report_bonus(file_name)

    def find_max_temp(self, file_name):
        for file in glob.glob(file_name):
            f = open(file, "r")
            file_data = f.readlines()
            for line in file_data:
                words = line.split(",")
                if words[1] != "" and words[1] != "Max TemperatureC":
                    max = int(words[1])
                    if max > self.max_temp:
                        self.max_temp = max
                        self.max_date = words[0]
                if words[3] != "" and words[3] != "Min TemperatureC":
                    min = int(words[3])
                    if min < self.min_temp:
                        self.min_temp = min
                        self.min_date = words[0]
                if words[7] != "" and words[7] != "Max Humidity":
                    hum = int(words[7])
                    if hum > self.max_hum:
                        self.max_hum = hum
                        self.hum_date = words[0]

    def report_mean(self, file_name):
        maxmean = 0
        minmean = 0
        avghum = 0
        total_element_max = 0
        total_element_min = 0
        total_element_hum = 0
        for file in glob.glob(file_name):
            f = open(file,"r")
            file_data = f.readlines()
            for line in file_data:
                words = line.split(",")
                if words[1] != "" and words[1] != "Max TemperatureC":
                    maxmean += int(words[1])
                    total_element_max += 1
                if words[3] != "" and words[3] != "Min TemperatureC":
                    minmean += int(words[3])
                    total_element_min += 1
                if words[8] != "" and words[8] != " Mean Humidity":
                    avghum += int(words[8])
                    total_element_hum += 1
        self.max_mean = int(maxmean/total_element_max)
        self.min_mean = int(minmean/total_element_min)
        self.avg_hum = int(avghum/total_element_hum)

    def report_barchart(self, file_name):
        black = '\033[30m'
        for file in glob.glob(file_name):
            f = open(file, "r")
            daynum = 0
            file_data = f.readlines()
            for line in file_data:
                words = line.split(",")
                if words[1] != "" and words[1] != "Max TemperatureC":
                    maxtemp = int(words[1])
                    i = 0
                    barchart = ""
                    while i< maxtemp:
                        barchart += "+"
                        i += 1
                    R = '\033[31m'
                    print(str(daynum)+" "+R+barchart+" "+black+str(maxtemp)+"C")
                if words[3] != "" and words[3] != "Min TemperatureC":
                    mintemp = int(words[3])
                    i = 0
                    barchart = ""
                    while i< mintemp:
                        barchart += "+"
                        i += 1
                    B = '\033[34m'
                    print(str(daynum)+" "+B+barchart+" "+black+str(mintemp)+"C")
                daynum += 1

    def report_bonus(self, file_name):
        black = '\033[30m'
        for file in glob.glob(file_name):
            f = open(file, "r")
            daynum = 0
            file_data = f.readlines()
            for line in file_data:
                words = line.split(",")
                barchartmin = ""
                barchartmax = ""
                maxtemp = 0
                mintemp = 0
                if words[1] != "" and words[1] != "Max TemperatureC":
                    maxtemp = int(words[1])
                    i = 0
                    while i < maxtemp:
                        barchartmax += "+"
                        i += 1
                    R = '\033[31m'
                    barchartmax = R+barchartmax
                if words[3] != "" and words[3] != "Min TemperatureC":
                    mintemp = int(words[3])
                    i = 0
                    while i< mintemp:
                        barchartmin += "+"
                        i += 1
                    B = '\033[34m'
                    barchartmin = B+barchartmin
                if daynum > 0 and words[3] != "" and words[1] != "":
                    print(black+str(daynum)+" "+barchartmin+barchartmax+" "+black+str(mintemp)+"C-"+str(maxtemp)+"C")
                daynum += 1

    def print_max(self):
        black = '\033[30m'
        mydatemax = datetime.datetime.strptime(self.max_date, '%Y-%m-%d')
        mydatemin = datetime.datetime.strptime(self.min_date, '%Y-%m-%d')
        mydatehum = datetime.datetime.strptime(self.hum_date, '%Y-%m-%d')
        print(black+"Higest:" + str(self.max_temp) + "C on " + mydatemax.strftime('%B %d'))
        print(black+"Lowest:" + str(self.min_temp) + "C on " + mydatemin.strftime('%B %d'))
        print(black+"Humidity:" + str(self.max_hum) + "% on " + mydatehum.strftime('%B %d'))

    def print_average(self):
        black = '\033[30m'
        print(black+"Highest Avergae:"+str(self.max_mean)+"C")
        print(black+"Lowest Avergae:" + str(self.min_mean) + "C")
        print(black+"Avergae Mean Humidity:" + str(self.avg_hum) + "%")

report = ForecastReport()
i = 0
for index in sys.argv:
    if i > 0:
        list = sys.argv[i].split()
        report.generate_report(list[1],list[0])
    i += 1
