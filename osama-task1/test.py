#!~/Documents/myenv/bin/python3
import csv
import sys
from datetime import datetime
import calendar
import os
from termcolor import colored


def main():

    path = sys.argv[1]
    dirs = os.listdir(path)

    for i in range(2, len(sys.argv), 2):
        year = sys.argv[i + 1][0:4]
        if sys.argv[i] == '-e':
            year_list = []
            for file in dirs:
                if year in file:
                    year_list.append(file)

            max_T = [(-273, 0000 - 00 - 00)]
            min_T = [(1000, 0000 - 00 - 00)]
            max_H = [(0, 0000 - 00 - 00)]

            for file in year_list:
                with open(path + '/' + file) as csvfile:
                    filereader = csv.DictReader(csvfile)
                    for row in filereader:
                        if row['Max TemperatureC'] != '':
                            max_T.append(
                                (int(row['Max TemperatureC']), row['PKT']))
                        if row['Min TemperatureC'] != '':
                            min_T.append(
                                (int(row['Min TemperatureC']), row['PKT']))
                        if row['Max Humidity'] != '':
                            max_H.append(
                                (int(row['Max Humidity']), row['PKT']))

            b = max(max_T)
            m = min(min_T)
            h = max(max_H)
            d = datetime.strptime(b[1], '%Y-%m-%d')
            d2 = datetime.strptime(m[1], '%Y-%m-%d')
            d3 = datetime.strptime(h[1], '%Y-%m-%d')

            print('Highest: ' + str(b[0]).zfill(2) + 'C on ' +
                  calendar.month_name[d.month] + ' ' + str(d.day).zfill(2))
            print('Lowest: ' + str(m[0]).zfill(2) + 'C on ' +
                  calendar.month_name[d2.month] + ' ' + str(d2.day).zfill(2))
            print('Humidity: ' + str(h[0]).zfill(2) + '% on ' +
                  calendar.month_name[d3.month] + ' ' + str(d3.day).zfill(2))
            print()
        elif sys.argv[i] == '-a' or 'c':
            if int(sys.argv[i + 1][5]) == 0:
                month = int(sys.argv[i + 1][6])
            else:
                month = int(sys.argv[i + 1][5:])
            month = calendar.month_abbr[month]

            for file in dirs:
                if year in file:
                    if month in file:
                        req_file = file

            lists_highT = []
            lists_lowT = []
            lists_meanH = []

            with open(path + '/' + req_file) as csvfile:
                filereader = csv.DictReader(csvfile)
                for row in filereader:
                    if row['Max TemperatureC'] != '':
                        lists_highT.append(int(row['Max TemperatureC']))
                    else:
                        lists_highT.append('-')
                    if row['Min TemperatureC'] != '':
                        lists_lowT.append(int(row['Min TemperatureC']))
                    else:
                        lists_lowT.append('-')
                    if row[' Mean Humidity'] != '':
                        lists_meanH.append(int(row[' Mean Humidity']))
                    else:
                        lists_meanH.append('-')

            if sys.argv[i] == '-a':
                avg_high = 0
                avg_low = 0
                avg_hum = 0
                for i in lists_highT:
                    if i != '-':
                        avg_high += i
                avg_high = avg_high // len(
                    [n for n in lists_highT if str(n).isdigit()])

                for i in lists_lowT:
                    if i != '-':
                        avg_low += i
                avg_low = avg_low // len(
                    [n for n in lists_lowT if str(n).isdigit()])

                for i in lists_meanH:
                    if i != '-':
                        avg_hum += i
                avg_hum = avg_hum // len(
                    [n for n in lists_meanH if str(n).isdigit()])

                print('Highest Average: ' + str(avg_high) + 'C')
                print('Lowest Average: ' + str(avg_low) + 'C')
                print('Average Mean Humidity: ' + str(avg_hum) + '%')
                print()
            elif sys.argv[i] == '-c':
                text = ''
                print(month, year)
                for x in range(0, len(lists_highT)):
                    if lists_highT[x] == '-':
                        continue
                    print(str(x + 1).zfill(2), end=' ')
                    for i in range(0, lists_highT[x]):
                        text += colored('+', 'red')
                    print(text + ' ' + str(lists_highT[x]) + 'C')
                    text = ''
                    print(str(x + 1).zfill(2), end=' ')
                    for i in range(0, lists_lowT[x]):
                        text += colored('+', 'blue')
                    print(text + ' ' + str(lists_lowT[x]) + 'C')
                    text = ''
                print()
                print(month, year)
                for x in range(0, len(lists_highT)):
                    if lists_highT[x] == '-':
                        continue
                    print(str(x + 1).zfill(2), end=' ')
                    for i in range(0, lists_lowT[x]):
                        text += colored('+', 'blue')
                    #print(text, end='')
                    #text = ''

                    for i in range(0, lists_highT[x]):
                        text += colored('+', 'red')
                    print(text + ' ' + str(lists_lowT[x]) +
                          'C - ' + str(lists_highT[x]) + 'C')
                    text = ''
                print()


if __name__ == "__main__":
    main()
