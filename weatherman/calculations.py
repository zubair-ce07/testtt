import datetime
import os
import sys
import copy
import statistics


def print_list(listt):
    for i in range(len(listt)):
        print(listt[i])
        print("\n")


def replacing_values(allfiles):
    for i in range (len(allfiles)):
                if allfiles[i][3] == '':
                        allfiles[i][3] = "200"
    for i in range(len(allfiles)):
                if allfiles[i][1] == '':
                        allfiles[i][1]="0"
    for i in range(len(allfiles)):
                if allfiles[i][7] == '':
                        allfiles[i][7] = "0"


def calculating_average(listt,index):
        local_average = 0
        new = [float(x[index]) for x in listt if x[index]!='']
        local_average = statistics.mean(new)
        return local_average
        

def draw_graph(day,max_temp,min_temp):
    print(day, end=' ')                      
    for i in range(int(min_temp)):
        print("\033[1;34;40m+", end='')     
    for i in range(int(max_temp)):
        print("\033[1;31;40m+", end='')
    print("\033[1;37;40m" + str(min_temp) + "C", end=' ')
    print("\033[1;37;40m" + str(max_temp) + "C")


def sorting_max_values(all_files):
    
    sorted_values=[]
    replacing_values(all_files)
    all_files.sort(key=lambda x: int(x[1])) 
    sorted_values.append(all_files[len(all_files)-1])
    all_files.sort(key=lambda x: int(x[3]))  
    sorted_values.append(all_files[0])
    all_files.sort(key=lambda x: int(x[7]))          
    sorted_values.append(all_files[len(all_files)-1])
    return sorted_values

