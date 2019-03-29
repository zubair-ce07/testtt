import datetime
import os
import sys
import copy


maxTemp_from_all_files = []
minTemp_from_all_files = []
maxHumd_from_all_files = []

def print_List(List):
    for i in range(len(List)):
        print(List[i])
        print("\n")


def date_splitter(dates_string):
    intList = []
    x = dates_string.split("-")
    intList = list(map(int, x))
    temp_date = datetime.datetime(intList[0], intList[1], intList[2])
    final_date = temp_date.strftime("%b %d")
    return final_date


def parsing_allfiles(basepath,
                     yearM,
                     tag):
    final_file_List = []    
    List_of_files = []
    final_file = ""
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            List_of_files.append(entry)
    if(tag == "-e"):

        for i in range(0, len(List_of_files)):
                if(List_of_files[i][15:19] == yearM):
                        final_file_List.append(basepath + List_of_files[i])
        return final_file_List
    if(tag == "-a" or tag == "-c"):
        for i in range(0, len(List_of_files)):
                if(List_of_files[i][15:23] == yearM):
                        final_file = basepath + List_of_files[i]
    
    return final_file


def formatting_filename(argfile):
        month_dict = {'1':'Jan' , '2':'Feb' , '3':'Mar' , '4':'Apr' , '5':'May',
                      '6':'Jun' , '7' :'Jul' , '8':'Aug' , '9':'Sep' , '10':'Oct' , '11':'Nov' , '12':'Dec'}
        temp_List = []
        x = argfile.split("/")
        temp_List.append(x)
        new_str = temp_List[0][0]+"_" + month_dict.get(temp_List[0][1])
        return new_str

def average_calculator(listt,
                       index):
        summ = 0
        countt = 0
        local_average = 0
        for i in range(len(listt)):
            if (listt[i][index] != ''):  
                summ = summ + float(listt[i][index])  
                countt += 1    
       
        local_average = float(summ/countt)
        return local_average


def draw_graph(day,
               maxTemp,
               minTemp):
    print(day, end=' ')                      
    for i in range(int(minTemp)):
        print("\033[1;34;40m+", end=' ')     
    for i in range(int(maxTemp)):
        print("\033[1;31;40m+", end=' ')
    print("\033[1;37;40m" + str(minTemp) + "C", end=' ')
    print("\033[1;37;40m" + str(maxTemp) + "C")

    
    
def extracting_date(datee):
        x = datee.split("-")
        day = x[2]
        return day


def replacing_values(allfiles):
        for i in range(len(allfiles)):
                if(allfiles[i][3] == ''):
                        allfiles[i][3] = "200"

        for i in range(len(allfiles)):
                if(allfiles[i][1] == ''):
                        allfiles[i][1] = "0"

        for i in range(len(allfiles)):
                if(allfiles[i][7] == ''):
                        allfiles[i][7] = "0"
        

def file_reader(filename,
                tag,
                megaList):
    allfiles = []
    temp_list = []
    my_dict = {}
    date_inlist = []
    
    with open(filename, "r") as f:
        header_line = next(f)  
        for line in f:
            result = [x.strip() for x in line.split(',')]
            allfiles.append(result)
    if(tag == "-e"):   
        replacing_values(allfiles)
        allfiles.sort(key=lambda x: x[1])  
        maxTemp_from_all_files.append(allfiles[len(allfiles)-1])
        allfiles.sort(key=lambda x: x[3])  
        minTemp_from_all_files.append(allfiles[0])
        allfiles.sort(key=lambda x: x[7])          
        maxHumd_from_all_files.append(allfiles[len(allfiles)-1])
     
    if(tag == "-a"):
        Averrage_highest = average_calculator(allfiles, 1)
        Averrage_Lowest = average_calculator(allfiles, 3)
        Averrage_Humidity = average_calculator(allfiles, 8)
        
        print("Average Highest: " + str(Averrage_highest) + " C")
        print("Average Lowst: " + str(Averrage_Lowest) + " C")
        print("Average Humidit: " + str(Averrage_Humidity) + " %")
    if(tag == "-c"):
        for i in range(len(allfiles)-1):
            if(allfiles[i][1] != ''or allfiles[i][3] != '' or allfiles[i][7] != ''):
                    draw_graph(extracting_date(allfiles[i][0]), allfiles[i][1], allfiles[i][3])
                    print("\n")   


def subtask1(basepath,
             year_month,
             tag):
    megaList=[]
    final_file_list = parsing_allfiles(basepath, year_month, tag)
    if (final_file_list.count != 0):
        if len(final_file_list) != 0:
                for i in range(len(final_file_list)):
                        file_reader(final_file_list[i], tag, megaList)
        maxTemp_from_all_files.sort(key=lambda y: int(y[1]))         
        minTemp_from_all_files.sort(key=lambda y: int(y[3]))         
        maxHumd_from_all_files.sort(key=lambda y: int(y[7]))             
        final_date = date_splitter(maxTemp_from_all_files[len(maxTemp_from_all_files)-1][0])
        print("Max Temprature: " + maxTemp_from_all_files[len(maxTemp_from_all_files)-1][7] + "%" + "  on " + final_date)
        final_date = date_splitter(minTemp_from_all_files[0][0])
        print("Min temprature: " + minTemp_from_all_files[0][3] + "C" + "  on " + final_date)
        final_date = date_splitter(maxHumd_from_all_files[len(maxHumd_from_all_files)-1][0])
        print("Max Humidity: " + maxHumd_from_all_files[len(maxHumd_from_all_files)-1][7] + "%" + "  on " + final_date)
        print("\n-----------------------")


def subtask2(basepath,
             year_month,
             tag):
    megaList = []
    modified_string = formatting_filename(year_month)
    filename = parsing_allfiles(basepath, modified_string, tag)
    file_reader(filename, tag, megaList)
    print("\n-----------------------")


def subtask3(basepath,
             year_month,
             tag):
    megaList = []
    modified_string = formatting_filename(year_month)
    filename = parsing_allfiles(basepath, modified_string, tag)
    file_reader(filename, tag, megaList)
    print("\n-----------------------")


def main():
    ArugementList = sys.argv
    basepath = ArugementList[1]           #weather files path
    for i in range(2, len(ArugementList)):
            if(ArugementList[i] == '-e'):
                    subtask1(basepath, ArugementList[i+1], ArugementList[i])
            if(ArugementList[i] == '-a'):
                    subtask2(basepath, ArugementList[i+1], ArugementList[i])
            if(ArugementList[i] == '-c'):
                    subtask3(basepath, ArugementList[i+1], ArugementList[i])
            
main()