import os
from reportlab.pdfgen import canvas

month_lst = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
              'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def Report(fpath,month):
    print("\n    Report 2")
    month = int(month)
    my_file = fpath + "_" + month_lst[month] + ".txt"
    temprature_list = []
    humidity_list = []
    if os.path.isfile(my_file): 
        with open(my_file) as file:
            next(file)          #skip first line of the file
            # Values of temprature and humidity inserted into perticular list
            for line in file:
                file = line.split(',')
                temprature_list.append(file[3])
                humidity_list.append(file[9])
    
        while '' in temprature_list:
            temprature_list.remove('')
        while '' in humidity_list:
            humidity_list.remove('')    
            
        temprature_list = list(map(int, temprature_list)) 
        humidity_list = list(map(int, humidity_list))

        if len(temprature_list) != 0:
            print("Highest Average: " + str(max(temprature_list)) + "C")
            print("Lowest Average: " + str(min(temprature_list))+ "C")
            print("Average Mean Humidity: " + str(sum(humidity_list)/len(humidity_list)) + "%")    

            # Genarates report
            c = canvas.Canvas("Report2.pdf")
            c.drawString(150, 700, "Highest Average: " + str(max(temprature_list)) + "C")
            c.drawString(150, 685, "Lowest Average: " + str(min(temprature_list))+ "C")
            c.drawString(150, 670, "Average Mean Humidity: " + str(sum(humidity_list)/len(humidity_list)) + "%")
            c.save()    
     