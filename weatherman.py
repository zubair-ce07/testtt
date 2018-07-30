import os
import calendar
import argparse


class Starter:

    file_names = os.listdir("/home/rehan/Documents/task/the-lab/weatherfiles")
    data = []

    def __init__(self):
        for q in range(1, self.file_names.__len__()):

            tempo = open('/home/rehan/Documents/task/the-lab/weatherfiles/'
                         + str(self.file_names[q])).read().split("\n")
            self.data = tempo + self.data

        for q in range(self.data.__len__()):  # reads and splits using comma into list
            self.data[q] = self.data[q].split(',')


class Calculations:

    s = Starter()
    all_data = s.data

    def give_month_bar(self, year_month):
        print(calendar.month_name[int(year_month[-1:])] + " " + year_month[:4])
        for k in range(0, self.all_data.__len__() - 1):
            if year_month[0:4] == self.all_data[k][0][0:4] and year_month[-1:] == self.all_data[k][0][5:6]:
                if self.all_data[k][1] != '':
                    print(self.all_data[k][0][7:] + ' ' + '\033[91m' + '+' * int(self.all_data[k][1]) + '\033[0m' + " "
                          + self.all_data[k][1] + "C")
                if self.all_data[k][3] != '':
                    print(self.all_data[k][0][7:] + ' ' + '\033[94m' + '+' * int(self.all_data[k][3]) + '\033[0m' + " "
                          + self.all_data[k][3] + "C")

    def give_year_data(self, year):
        highest_temp = 0
        highest_temp_date = 0
        lowest_temp = 100
        lowest_temp_date = 0
        humidity = 0
        humidity_date = 0
        for p in range(0, self.all_data.__len__()):
            if year == self.all_data[p][0][0:4]:
                if self.all_data[p][1] != '':
                    if int(self.all_data[p][1]) > highest_temp:
                        highest_temp = int(self.all_data[p][1])
                        highest_temp_date = p
                if self.all_data[p][3] != '':
                    if int(self.all_data[p][3]) < lowest_temp:
                        lowest_temp = int(self.all_data[p][3])
                        lowest_temp_date = p
                if self.all_data[p][7] != '':
                    if int(self.all_data[p][7]) > humidity:
                        humidity = int(self.all_data[p][7])
                        humidity_date = p
        return str(highest_temp), calendar.month_name[int(self.all_data[highest_temp_date][0][5:6])], \
            self.all_data[highest_temp_date][0][7:], str(lowest_temp), \
            calendar.month_name[int(self.all_data[lowest_temp_date][0][5:6])], \
            self.all_data[lowest_temp_date][0][7:], str(humidity), \
            calendar.month_name[int(self.all_data[humidity_date][0][5:6])], self.all_data[humidity_date][0][7:]

    def give_month_data(self, year_month):
        highest_cumulative = 0
        highest_counter = 0
        lowest_cumulative = 0
        lowest_counter = 0
        humidity_cumulative = 0
        humidity_counter = 0
        for k in range(0, self.all_data.__len__()):
            if year_month[0:4] == self.all_data[k][0][0:4] and year_month[-1:] == self.all_data[k][0][5:6]:
                if self.all_data[k][1] != '':
                    highest_cumulative = highest_cumulative + int(self.all_data[k][1])
                    highest_counter = highest_counter + 1
                if self.all_data[k][3] != '':
                    lowest_cumulative = lowest_cumulative + int(self.all_data[k][3])
                    lowest_counter = lowest_counter + 1
                if self.all_data[k][8] != '':
                    humidity_cumulative = humidity_cumulative + int(self.all_data[k][8])
                    humidity_counter = humidity_counter + 1
        highest_average = int(highest_cumulative / highest_counter)
        lowest_average = int(lowest_cumulative / lowest_counter)
        humidity_average = int(humidity_cumulative / humidity_counter)
        return highest_average, lowest_average, humidity_average


class PrintReport:

    def print_task_2(self, highest_average, lowest_average, humidity_average):
        print("Highest Average: " + str(highest_average) + "C")
        print("Lowest Average: " + str(lowest_average) + "C")
        print("Average Mean Humidity: " + str(humidity_average) + "C")

    def print_task_1(self, s1, s2, s3, s4, s5, s6, s7, s8, s9):
        print("Highest: " + s1 + "C on " + s2 + " " + s3)
        print("Lowest: " + s4 + "C on " + s5 + " " + s6)
        print("Humidity: " + s7 + "% on " + s8 + " " + s9)

    def print_task_bonus(self, year_month, data_list):
        print(calendar.month_name[int(year_month[-1:])] + " " + year_month[:4])
        for k in range(0, data_list.__len__() - 1):
            if year_month[0:4] == data_list[k][0][0:4] and year_month[-1:] == data_list[k][0][5:6]:
                if data_list[k][1] != '':
                    print(data_list[k][0][7:] + ' ' + '\033[91m' + '+' * int(data_list[k][1]) +
                          '\033[94m' + '+' * int(data_list[k][3]) + '\033[0m' +
                          " " + data_list[k][1] + "C" + " " + data_list[k][3] + "C")

    def print_task_3(self, year_month, data_list):
        print(calendar.month_name[int(year_month[-1:])] + " " + year_month[:4])
        for k in range(0, data_list.__len__() - 1):
            if year_month[0:4] == data_list[k][0][0:4] and year_month[-1:] == data_list[k][0][5:6]:
                if data_list[k][1] != '':
                    print(data_list[k][0][7:] + ' ' + '\033[91m' + '+' * int(data_list[k][1]) + '\033[0m' + " "
                          + data_list[k][1] + "C")
                if data_list[k][3] != '':
                    print(data_list[k][0][7:] + ' ' + '\033[94m' + '+' * int(data_list[k][3]) + '\033[0m' + " "
                          + data_list[k][3] + "C")


def main():

    c = Calculations()

    p = PrintReport()

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--extreme', help='foo help')
    parser.add_argument('-a', '--average', help='foo help')
    parser.add_argument('-c', '--bar', help='foo help')
    parser.add_argument('-b', '--bonus', help='foo help')
    args = parser.parse_args()
    if args.extreme:
        s1, s2, s3, s4, s5, s6, s7, s8, s9 = c.give_year_data(args.extreme)
        p.print_task_1(s1, s2, s3, s4, s5, s6, s7, s8, s9)
    if args.average:
        highest_average, lowest_average, humdity_average = c.give_month_data(args.average)
        p.print_task_2(highest_average, lowest_average, humdity_average)
    if args.bar:
        p.print_task_3(args.bar, c.all_data)
    if args.bonus:
        p.print_task_bonus(args.bonus, c.all_data)


if '__main__' == __name__:
    main()