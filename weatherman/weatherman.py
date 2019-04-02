import datetime
import os
import sys
import copy
import statistics
import file_reader as fr
import report_generation as gr
import calculations as cl
import argparse


def print_List(input):
    for i in range(len(input)):
        print(input[i])
        print("\n")


def find_max_values(basepath,year_month):
   files = fr.get_files(basepath)
   if files.count == 0:
        return 
   days=fr.read_files(files,year_month,0,4)
   sorted_values=cl.sorting_max_values(days)
   gr.print_max(sorted_values)

def find_avge_values(basepath, year_month):
    year_month = str(year_month).replace("/","-")   
    year_month = f"{year_month}-"
    files = fr.get_files(basepath)
    days=fr.read_files(files,year_month,0,8)
    gr.print_averges(days)
    print("\n-----------------------")

   
def design_graph(basepath,year_month):
    year_month = str(year_month).replace("/","-")
    year_month = f"{year_month}-"
    print(year_month)
    files = fr.get_files(basepath)
    days=fr.read_files(files,year_month,0,8)
    gr.print_graph(days)                    
    print("\n-----------------------")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("basepath", help="directory path",
                        type=str)
    parser.add_argument("-e", "--max_temp",help="display a square of a given number",
                        type=str)
    parser.add_argument("-a", "--avg_temp",help="display a square of a given number",
                        type=str)
    parser.add_argument("-c","--graph" ,help="display a square of a given number",
                        type=str)

    args = parser.parse_args()    
    if args.max_temp:
            find_max_values(args.basepath,args.max_temp)
    if args.avg_temp:
            find_avge_values(args.basepath,args.avg_temp)
    if args.graph:
            design_graph(args.basepath,args.graph)

    print(args.basepath)

main()
