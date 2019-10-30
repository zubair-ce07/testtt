import os.path
from reportlab.pdfgen import canvas


month_lst = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
              'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

class YearlyReport:
    def __init__(self, file_path):
        self.file_path = file_path
        
        self.max_temp = 0
        self.max_temp_month = 0

        self.min_temp = 200
        self.min_temp_month = 0

        self.max_humid = 0
        self.max_humid_month = 0

        self.ReportGenerator()

    def ReportGenerator(self):
        print("\n    Report 1")
        
        
        for month in range(12):
            
            my_file = self.file_path + "_" + month_lst[month] + ".txt"
            temprature_list = []
            humidity_list = []

            if os.path.isfile(my_file): 
                with open(my_file) as file:
                    next(file)             #skip first line of the file
                    # Values of temprature and humidity inserted into perticular list
                    for line in file:
                        file = line.split(',')
                        temprature_list.append(file[2])
                        humidity_list.append(file[8])
        
                while '' in temprature_list:
                    temprature_list.remove('')
                while '' in humidity_list:
                    humidity_list.remove('')    
                
                temprature_list = list(map(int, temprature_list)) 
                humidity_list = list(map(int, humidity_list))

                if len(temprature_list) != 0 and self.max_temp < max(temprature_list):
                    self.max_temp = max(temprature_list)
                    self.max_temp_month = month
                    
                if len(temprature_list) != 0 and self.min_temp > min(temprature_list):    
                    self.min_temp = min(temprature_list)
                    self.min_temp_month = month

                if len(humidity_list) != 0 and self.max_temp < max(humidity_list):
                    self.max_humid = max(humidity_list)
                    self.max_humid_month = month    

            
        print("Highest: " + str(self.max_temp) + "C on " + month_lst[self.max_temp_month])   
        print("Lowest: " + str(self.min_temp) + "C on " + month_lst[self.min_temp_month])
        print("Humidity: " + str(self.max_humid) + "% on " + month_lst[self.max_humid_month])


        # Genarates report
        c = canvas.Canvas("Report1.pdf")
        c.drawString(150, 700, "Highest: " + str(self.max_temp) + "C on " + month_lst[self.max_temp_month])
        c.drawString(150, 685, "Lowest: " + str(self.min_temp) + "C on " + month_lst[self.min_temp_month])
        c.drawString(150, 670, "Humidity: " + str(self.max_humid) + "% on " + month_lst[self.max_humid_month])
        c.save()
    
class MonthlyReport:
    def __init__(self, file_path, month):
        self.file_path = file_path
        self.month = month
        self.ReportGenerator()

    def ReportGenerator(self):
        print("\n    Report 2")
        month = int(self.month)
        my_file = self.file_path + "_" + month_lst[month] + ".txt"
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

class HorizontalBarReport:
    def __init__(self, file_path, month):
        self.file_path = file_path
        self.month = month
        self.ReportGenerator()

    def ReportGenerator(self):
        print("\n    Report 3")
        month = int(self.month)
        my_file = self.file_path + "_" + month_lst[self.month] + ".txt"
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
