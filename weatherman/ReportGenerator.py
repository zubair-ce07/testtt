import os.path


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

        self._report_generator()

    def _report_generator(self):
        print("\n    Report 1")
        
        
        for current_month in month_lst:
            my_file = self.file_path + "_" + current_month + ".txt"
            temprature_list = []
            humidity_list = []
            
            if os.path.isfile(my_file):
                with open(my_file) as file:
                    next(file)             #skip first line of the file
                    for each_line in file:
                        file = each_line.split(',')
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
                    self.max_temp_month = current_month
                    
                if len(temprature_list) != 0 and self.min_temp > min(temprature_list):    
                    self.min_temp = min(temprature_list)
                    self.min_temp_month = current_month

                if len(humidity_list) != 0 and self.max_temp < max(humidity_list):
                    self.max_humid = max(humidity_list)
                    self.max_humid_month = current_month    

            
        print(f"Highest: {self.max_temp} C on  {self.max_temp_month}")
        print(f"Lowest: {self.min_temp} C on  {self.min_temp_month}")
        print(f"Humidity: {self.max_humid} C on  {self.max_humid_month}")

     
class MonthlyReport:
    def __init__(self, file_path, month):
        self.file_path = file_path
        self.month = month
        self._report_generator()

    def _report_generator(self):
        print("\n    Report 2")
        month = int(self.month)
        my_file = self.file_path + "_" + month_lst[month] + ".txt"
        temprature_list = []
        humidity_list = []
        if os.path.isfile(my_file): 
            with open(my_file) as file:
                next(file)          #skip first line of the file
                for line in file:
                    file = line.split(',')
                    temprature_list.append(file[3])
                    humidity_list.append(file[9])
        
            while '' in temprature_list:
                temprature_list.remove('')
            while '' in humidity_list:
                humidity_list.remove('')    
            #converts string elementes of the list into int for calculations    
            temprature_list = list(map(int, temprature_list)) 
            humidity_list = list(map(int, humidity_list))

            if len(temprature_list) != 0:
                print(f"Highest Average: {max(temprature_list)}C")
                print(f"Lowest Average: {min(temprature_list)}C")
                print(f"Average Mean Humidity: {sum(humidity_list)/len(humidity_list)}%C")  

                
class HorizontalBarReport:
    def __init__(self, file_path, month):
        self.file_path = file_path
        self.month = month
        self._report_generator()

    def _report_generator(self):
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

            for i in range(len(max_temprature_list)):
                if i < 9:
                    print("\n0" + str(i+1), end=" ")
                else:
                    print("\n" + str(i+1), end=" ")


                for j in range(min_temprature_list[i]):
                    print(f'\033[1;34m' '+' '\033[1;m', end=" ")              
                
                for j in range(max_temprature_list[i]):
                    print(f'\033[31m' '+' '\033[0m', end=" ")
                print(f'{min_temprature_list[i]}C - {max_temprature_list[i]}C')    
                