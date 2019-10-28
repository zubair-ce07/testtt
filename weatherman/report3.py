import os
from reportlab.pdfgen import canvas

month_lst = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
              'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def Report(fpath,month):
    print("\n    Report 3")
    month = int(month)
    my_file = fpath + "_" + month_lst[month] + ".txt"
    date_list = []
    max_temprature_list = []
    min_temprature_list = []
    if os.path.isfile(my_file): 
        with open(my_file) as file:
            next(file)             #skip first line of the file
            # Values of temprature and humidity inserted into perticular list
            for line in file:
                file = line.split(',')
                date_list.append(file[0])
                max_temprature_list.append(file[2])
                min_temprature_list.append(file[4])
    
        while '' in max_temprature_list:
            max_temprature_list.remove('')
        while '' in min_temprature_list:
            min_temprature_list.remove('')    
            
        max_temprature_list = list(map(int, max_temprature_list)) 
        min_temprature_list = list(map(int, min_temprature_list))

        c = canvas.Canvas("Report3.pdf")
        for i in range(len(max_temprature_list)):
            if i < 9:
                print("\n0" + str(i+1) + " "),
            else:
                print("\n" + str(i+1) + " "),


            for j in range(min_temprature_list[i]):
               print('\033[1;34m' + '+' + '\033[1;m'),              
            
            for j in range(max_temprature_list[i]):
               print('\033[31m' + '+' + '\033[0m'),
            print(str(min_temprature_list[i]) + "C" + " - " + str(max_temprature_list[i]) + "C")
              

   