import datetime
import os
import sys
import copy
import statistics


def print_list(input):
    for i in range(len(input)):
        print(input[i])
        print("\n")

def get_files(basepath):
    final_file_List = []    
    files = []
    final_file = ""

    for file in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, file)):
            if file!=".DS_Store":
                files.append(file)
    
    for i in range(0, len(files)):
        final_file_List.append(basepath + files[i])
    
    return final_file_List


def read_files(files,input,start_index,end_index):
    
    all_files = []
    for i in range(len(files)):
        with open(str(files[i]), "r") as f:
            header_line = next(f)  
            for line in f:
                if line[start_index:end_index] == input:       
                    all_files.append(str(line).strip().split(","))
    return all_files
