import glob
import os
import datetime
import csv
import argparse


class WeatherReport:
    def __init__(self):
        pass

    def get_file(self, path, filename_string):
        self.filename_string = filename_string
        self.path = path
        list_file = []
        os.chdir(path)
        sammy_string = "{}"+filename_string+"{}"
        filename = sammy_string.format("*", "*")
        for f in glob.glob(filename):
            list_file.append(f)
        return list_file

    def average_of(self, list_temp, stra, strb):
        addition = 0
        for i in range(len(list_temp)):
            if list_temp[i] != '':
                addition = addition + list_temp[i]
        avg = addition / len(list_temp)
        print(stra, avg, strb)

    def graph_chart(self, high_temlist, low_templist, listdate):
        self.high_temlist = high_temlist
        self.listm = low_templist
        self.listdate = listdate
        for i in range(len(high_temlist)):
            print(listdate[i], " ", end='')
            if high_temlist[i] != '':
                for j in range(high_temlist[i]):
                    print("\033[31m+", end='')
                print(" \033[37m", high_temlist[i], 'C')
            else:
                print(0, "C")
            print(listdate[i], " ", end='')
            if low_templist[i] != '':
                for k in range(low_templist[i]):
                    print("\033[34m+", end='')
                print("\033[37m", low_templist[i], 'C')
            else:
                print(0, "C")

    def graph_chart1(self, high_temlist, low_templist, listdate):
        self.listn = high_temlist
        self.listm = low_templist
        self.listdate = listdate
        for i in range(len(high_temlist)):
            print(listdate[i], " ", end='')
            if low_templist[i] != '':
                for j in range(low_templist[i]):
                    print("\033[34m+", end='')
                print("\033[37m", end='')
            else:
                print(end='')
            if high_temlist[i] != '':
                for k in range(high_temlist[i]):
                    print("\033[31m+", end='')
                print(" \033[37m", low_templist[i], "-", high_temlist[i], 'C')
            else:
                print(low_templist[i], "-", high_temlist[i], "C")

    def making_list(self, list_data):
        self.list = list
        for i in range(len(list_data)):
            if list_data[i] != '':
                list_data[i] = int(list_data[i])
        return list_data

    def find_report_year(self, path, filename_string):
        self.filename_string = filename_string
        self.path = path
        list_date = []
        maxtamp_year = []
        mintamp_year = []
        maxhumi_year = []
        list_file = self.get_file(path, filename_string)
        for i in range(len(list_file)):
            with open(list_file[i], 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                high_temp_month = []
                low_temp_month = []
                high_humidity_month = []
                date_list = []
                for row in reader:
                    date_list.append(row['PKT'])
                    high_temp_month.append(row['Max TemperatureC'])
                    low_temp_month.append(row['Min TemperatureC'])
                    high_humidity_month.append(row['Max Humidity'])
                self.making_list(high_temp_month)
                self.making_list(low_temp_month)
                self.making_list(high_humidity_month)
                list_tamp1 = []
                list_date_tamp1 = []
                for i in range(len(high_temp_month)):
                    if high_temp_month[i] != '':
                        list_tamp1.append(high_temp_month[i])
                        list_date_tamp1.append(date_list[i])
                list_tamp2 = []
                list_date_tamp2 = []
                for i in range(len(low_temp_month)):
                    if low_temp_month[i] != '':
                        list_tamp2.append(low_temp_month[i])
                        list_date_tamp2.append(date_list[i])
                list_humi = []
                list_date_humi = []
                for i in range(len(high_humidity_month)):
                    if high_humidity_month[i] != '':
                        list_humi.append(high_humidity_month[i])
                        list_date_humi.append(date_list[i])
                list_date.append(list_date_tamp1[(list_tamp1.index
                                                  (max(list_tamp1)))])
                maxtamp_year.append(max(list_tamp1))
                list_date.append(list_date_tamp2[(list_tamp2.index
                                                  (max(list_tamp2)))])
                mintamp_year.append(min(list_tamp2))
                list_date.append(list_date_humi[(list_humi.index
                                                 (max(list_humi)))])
                maxhumi_year.append(max(list_humi))
        print("Highest:", max(maxtamp_year), "C", " on",
              list_date[maxtamp_year.index(max(maxtamp_year))])
        print("Lowest:", min(mintamp_year), "C", "  on",
              list_date[mintamp_year.index(min(mintamp_year))])
        print("Highest:", max(maxhumi_year), "%", "on",
              list_date[maxhumi_year.index(min(maxhumi_year))])

    def find_report_month(self, path, filename_string):
        self.path = path
        self.filename_string = filename_string
        high_temp_month = []
        low_temp_month = []
        high_humidity_month = []
        date_list = []
        list_file = self.get_file(path, filename_string)
        with open(list_file[0], 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                date_list.append(row['PKT'])
                high_temp_month.append(row['Max TemperatureC'])
                low_temp_month.append(row['Min TemperatureC'])
                high_humidity_month.append(row['Max Humidity'])
            self.making_list(high_temp_month)
            self.making_list(low_temp_month)
            self.making_list(high_humidity_month)
        self.average_of(high_temp_month, "Avg Highest Temprature ", "C")
        self.average_of(low_temp_month, "Avg Lowest Temprature  ", "C")
        self.average_of(high_humidity_month, "Average Mean Humidity ", "%")

    def findreport_month_graph(self, path, filename_string):
        self.path = path
        self.filename_string = filename_string
        high_temp_month = []
        low_temp_month = []
        date_list = []
        list_file = self.get_file(path, filename_string)
        with open(list_file[0], 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                date_list.append(row['PKT'])
                high_temp_month.append(row['Max TemperatureC'])
                low_temp_month.append(row['Min TemperatureC'])
            self.making_list(high_temp_month)
            self.making_list(low_temp_month)
        self.graph_chart(high_temp_month, low_temp_month, date_list)

    def findreport_month_graph1(self, path, filename_string):
        self.path = path
        self.filename_string = filename_string
        high_temp_month = []
        low_temp_month = []
        date_list = []
        list_file = self.get_file(path, filename_string)
        with open(list_file[0], 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                date_list.append(row['PKT'])
                high_temp_month.append(row['Max TemperatureC'])
                low_temp_month.append(row['Min TemperatureC'])
            self.making_list(high_temp_month)
            self.making_list(low_temp_month)
        self.graph_chart1(high_temp_month, low_temp_month, date_list)

    def find_filename(self, name):
        month1 = name.split("/")
        month_integer = int(month1[1])
        month = datetime.date(1900, month_integer, 6).strftime('%B')
        splits = [month[x:x + 3] for x in range(0, len(month), 3)]
        year = month1[0]
        filename = year + '_' + splits[0]
        return filename
if __name__ == '__main__':
    class_obj = WeatherReport()
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    parser.add_argument("-e", type=str)
    parser.add_argument("-a", type=str)
    parser.add_argument("-c", type=str)
    parser.add_argument("-d", type=str)
    args = parser.parse_args()
    if(args.e and args.a and args.c and args.d):
        print("\nReport of complete year\n")
        class_obj.find_report_year(args.path, args.e)
        print("\nReport of complete month\n\n")
        filename = class_obj.find_filename(args.a)
        class_obj.find_report_month(args.path, filename)
        print("\nReport of complete month in Graph\n\n")
        filename = class_obj.find_filename(args.c)
        class_obj.findreport_month_graph(args.path, filename)
        print("\nReport of month in Graph by Low and High Temprature\n\n")
        filename = class_obj.find_filename(args.d)
        class_obj.findreport_month_graph1(args.path, filename)
    else:
        if args.e:
            class_obj.find_report_year(args.path, args.e)
        elif args.a:
            filename = class_obj.find_filename(args.a)
            class_obj.find_report_month(args.path, filename)
        elif args.c:
            filename = class_obj.find_filename(args.c)
            class_obj.findreport_month_graph(args.path, filename)
        elif args.d:
            filename = class_obj.find_filename(args.d)
            class_obj.findreport_month_graph1(args.path, filename)
        else:
            print("Plz Valid arguments")

