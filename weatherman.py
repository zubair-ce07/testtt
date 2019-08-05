import copy
import csv
import sys
import os
from task1 import *
from task2 import *
from task3 import *
from task5 import *


def check_bound(lenght, count):
    if count >= lenght:
        return False
    else:
        return True


def main(argv):
    lenght = len(argv)
    count = 0
    while check_bound(lenght, count):
        if argv[count] == '-e':
            print("Task1 :")
            obj = task1()
            count = count + 1
            obj.task(argv[count])
            count = count + 1
            if not(check_bound(lenght, count)):
                break

        if argv[count] == '-a':
            print("Task2 :")
            obj = task2()
            count = count + 1
            year, month = argv[count].split('/')
            month = int(month) - 1
            obj.task(int(month), year)
            count = count + 1
            if not(check_bound(lenght, count)):
                break

        if argv[count] == '-c':
            print("Task3 :")
            obj = task3()
            count = count + 1
            year, mont = argv[count].split('/')
            month = int(month) - 1
            obj.task(int(month), year)
            count = count + 1
            if not(check_bound(lenght, count)):
                break

        if argv[count] == '-d':
            print("Task5 :")
            count = count + 1
            obj = task5()
            year, month = argv[count].split('/')
            month = int(month) - 1
            obj.task(int(month), year)
            count = count + 1
            if not(check_bound(lenght, count)):
                break


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    main(sys.argv[1:])
