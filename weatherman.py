import os
import calendar
import csv
from year_report import *
from month_report import *
from chart_report import *
from chart_report_bonus import *


def check_bound(lenght, count):
    if count >= lenght:
        return False
    else:
        return True


def extract_file_namaes(argv, argv_pointer, file_names):
    if argv[argv_pointer] == '-e':
        for month_idx in range(1, 13):
            temp = ("Murree_weather_{year}_{month}.txt".format(
                year=argv[argv_pointer+1], month=calendar.month_name[month_idx][:3]))
            try:
                with open(temp, "r") as csvFile:
                    reader = csv.reader(csvFile)
                csvFile.close()
                file_names.append(temp)
            except IOError:
                print("", end="")

    if argv[argv_pointer] == '-a' or argv[argv_pointer] == '-c' or argv[argv_pointer] == '-d':
        year, month_index = argv[argv_pointer + 1].split('/')
        file_names.append("Murree_weather_{year}_{month}.txt".format(
            year=year, month=calendar.month_name[int(month_index)][:3]))


def main(argv):
    file_names = []
    lenght = len(argv)
    count = 0
    while check_bound(lenght, count):
        file_names.clear()
        if argv[count] == '-e':
            print("Task1 :")
            extract_file_namaes(sys.argv[1:], count, file_names)
            obj = year_report()
            count = count + 1
            obj.generate_year_report(file_names)
            count = count + 1
            if not(check_bound(lenght, count)):
                break

        if argv[count] == '-a':
            print("Task2 :")
            obj = month_report()
            extract_file_namaes(sys.argv[1:], count, file_names)
            count = count + 1
            obj.generate_month_report(file_names)
            count = count + 1
            if not(check_bound(lenght, count)):
                break

        if argv[count] == '-c':
            print("Task3 :")
            obj = chart_report()
            extract_file_namaes(sys.argv[1:], count, file_names)
            count = count + 1
            obj.generate_chart_report(file_names)
            count = count + 1
            if not(check_bound(lenght, count)):
                break

        if argv[count] == '-d':
            print("Task5 :")
            extract_file_namaes(sys.argv[1:], count, file_names)
            count = count + 1
            obj = chart_report_bonus()
            obj.generate_chart_report_bonus(file_names)
            count = count + 1
            if not(check_bound(lenght, count)):
                break


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    main(sys.argv[1:])

