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
        filename = ('*%s*' % filename_string)
        for f in glob.glob(filename):
            list_file.append(f)
        return list_file

    def get_average_of(self, list_temp, str_a, str_b):
        addition = 0
        for i in range(len(list_temp)):
            if list_temp[i]:
                addition = addition + list_temp[i]
        avg = addition / len(list_temp)
        print(str_a, avg, str_b)

    def graph_chart(self, high_tem_list, low_temp_list, list_date):
        self.high_tem_list = high_tem_list
        self.low_temp_list = low_temp_list
        self.list_date = list_date
        for i in high_tem_list:
            print(list_date[i], " ", end='')
            if high_tem_list[i]:
                for j in range((high_tem_list[i])):
                    print("\033[31m+", end='')
                print(" \033[37m", high_tem_list[i], 'C')
            else:
                print(0, "C")
            print(list_date[i], " ", end='')
            if low_temp_list[i]:
                for k in range((low_temp_list[i])):
                    print("\033[34m+", end='')
                print("\033[37m", low_temp_list[i], 'C')
            else:
                print(0, "C")

    def graph_chart1(self, high_tem_list, low_temp_list, list_date):
        self.high_tem_list = high_tem_list
        self.low_temp_list = low_temp_list
        self.list_date = list_date
        for i in high_tem_list:
            print(list_date[i], " ", end='')
            if low_temp_list[i]:
                for j in range(low_temp_list[i]):
                    print("\033[34m+", end='')
                print("\033[37m", end='')
            else:
                print(end='')
            if high_tem_list[i]:
                for k in range(high_tem_list[i]):
                    print("\033[31m+", end='')
                print(" \033[37m", low_temp_list[i], "-", high_tem_list[i], 'C')
            else:
                print(low_temp_list[i], "-", high_tem_list[i], "C")

    def make_list(self, list_data):
        self.list_data = list_data
        for i in range(len(list_data)):
            if list_data[i]:
                list_data[i] = int(list_data[i])
        return list_data

    def find_year_report(self, path, filename_string):
        self.filename_string = filename_string
        self.path = path
        list_date = []
        max_tamp_year = []
        min_tamp_year = []
        max_humi_year = []
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
                self.make_list(high_temp_month)
                self.make_list(low_temp_month)
                self.make_list(high_humidity_month)
                list_tamp1 = []
                list_date_tamp1 = []
                for i in range(len(high_temp_month)):
                    if high_temp_month[i]:
                        list_tamp1.append(high_temp_month[i])
                        list_date_tamp1.append(date_list[i])
                list_tamp2 = []
                list_date_tamp2 = []
                for i in range(len(low_temp_month)):
                    if low_temp_month[i]:
                        list_tamp2.append(low_temp_month[i])
                        list_date_tamp2.append(date_list[i])
                list_humi = []
                list_date_humi = []
                for i in range(len(high_humidity_month)):
                    if high_humidity_month[i]:
                        list_humi.append(high_humidity_month[i])
                        list_date_humi.append(date_list[i])
                list_date.append(list_date_tamp1[(list_tamp1.index
                                                  (max(list_tamp1)))])
                max_tamp_year.append(max(list_tamp1))
                list_date.append(list_date_tamp2[(list_tamp2.index
                                                  (max(list_tamp2)))])
                min_tamp_year.append(min(list_tamp2))
                list_date.append(list_date_humi[(list_humi.index
                                                 (max(list_humi)))])
                max_humi_year.append(max(list_humi))
        print("Highest:", max(max_tamp_year), "C", " on",
              list_date[max_tamp_year.index(max(max_tamp_year))])
        print("Lowest:", min(min_tamp_year), "C", "  on",
              list_date[min_tamp_year.index(min(min_tamp_year))])
        print("Highest:", max(max_humi_year), "%", "on",
              list_date[max_humi_year.index(min(max_humi_year))])

    def find_month_report(self, path, filename_string):
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
            self.make_list(high_temp_month)
            self.make_list(low_temp_month)
            self.make_list(high_humidity_month)
        self.get_average_of(high_temp_month, "Avg Highest Temprature ", "C")
        self.get_average_of(low_temp_month, "Avg Lowest Temprature  ", "C")
        self.get_average_of(high_humidity_month, "Average Mean Humidity ", "%")

    def find_month_report_graph(self, path, filename_string):
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
            self.make_list(high_temp_month)
            self.make_list(low_temp_month)
        self.graph_chart(high_temp_month, low_temp_month, date_list)

    def find_month_report_graph1(self, path, filename_string):
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
            self.make_list(high_temp_month)
            self.make_list(low_temp_month)
        self.graph_chart1(high_temp_month, low_temp_month, date_list)

    def get_file_name(self, name):
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
        class_obj.find_year_report(args.path, args.e)
        print("\nReport of complete month\n\n")
        filename = class_obj.get_file_name(args.a)
        class_obj.find_month_report(args.path, filename)
        print("\nReport of complete month in Graph\n\n")
        filename = class_obj.get_file_name(args.c)
        class_obj.find_month_report_graph(args.path, filename)
        print("\nReport of month in Graph by Low and High Temprature\n\n")
        filename = class_obj.get_file_name(args.d)
        class_obj.find_month_report_graph1(args.path, filename)
    else:
        if args.e:
            class_obj.find_year_report(args.path, args.e)
        elif args.a:
            filename = class_obj.get_file_name(args.a)
            class_obj.find_month_report(args.path, filename)
        elif args.c:
            filename = class_obj.get_file_name(args.c)
            class_obj.find_month_report_graph(args.path, filename)
        elif args.d:
            filename = class_obj.get_file_name(args.d)
            class_obj.find_month_report_graph1(args.path, filename)
        else:
            print("Plz Valid arguments")

