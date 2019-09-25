import pandas as pd
import os
import sys
import re
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

def common_entries(*dcts):
        for i in set(dcts[0]).intersection(*dcts[1:]):
            yield (i,) + tuple(d[i] for d in dcts)

class Bonus:
    def __init__(self,year,month):
        self.year = year
        self.month = month
        self.formated_month = datetime(int(self.year), int(self.month), 1)
        self.selected_month = self.formated_month.strftime("%b")
        self.filname = 'Murree_weather_' + str(self.year) + '_' + self.selected_month + '.txt'
        self.read_max_average_temperature = []
        self.max_average_temperature = 0
        self.read_min_average_temperature = []
        self.pkt = []
    
    def graph(self):
        print("Hello")
        df = pd.read_csv(self.filname)
        print(df)
        self.read_max_temperature = df['Max TemperatureC'].fillna(df['Max TemperatureC'].mean())
        self.read_min_temperature = df['Min TemperatureC'].fillna(df['Min TemperatureC'].mean())
        self.pkt = df['PKT']
        length = np.arange(len(self.pkt))
        plt.barh(length,self.read_max_temperature , color = 'r')
        plt.barh(length,self.read_min_temperature, color = 'b')
        plt.yticks(length,self.pkt)
        plt.title('Horizontal bar charts')
        plt.xlabel('Temperature')
        plt.ylabel('Date')
        plt.show()
        

class Month_Year:
    def __init__(self,year,month):
        self.year = year
        self.month = month
        self.formated_month = datetime(int(self.year), int(self.month), 1)
        self.selected_month = self.formated_month.strftime("%b")
        self.filname = 'Murree_weather_' + str(self.year) + '_' + self.selected_month + '.txt'
        self.read_max_average_temperature = []
        self.max_average_temperature = 0
        self.read_min_average_temperature = []
        self.read_mean_average_temperature = []
        self.mean_average_temperature = 0
    def Maximum_Average(self):
        filename1 = open(self.filname)
        read = pd.read_csv(filename1)
        self.read_max_average_temperature = read['Max TemperatureC'].fillna(read['Max TemperatureC'].mean())
        self.max_average_temperature = (self.read_max_average_temperature.sum())/ 31
        print("MAx Average of Temperature: ",self.max_average_temperature)
    def Minimum_Average(self):
        filename1 = open(self.filname)
        read = pd.read_csv(filename1)
        self.read_min_average_temperature = read['Min TemperatureC'].fillna(read['Min TemperatureC'].mean())
        self.min_average_temperature = (self.read_min_average_temperature.sum())/ 31
        print("Min Average OF Temperature: ",self.min_average_temperature)
    def Mean_Humidity(self):
        filename1 = open(self.filname)
        read = pd.read_csv(filename1)
        self.read_mean_average_temperature = read[' Mean Humidity'].fillna(read[' Mean Humidity'].mean())
        self.mean_average_temperature = (self.read_mean_average_temperature.sum())/ 31
        print("Mean Average: ",self.mean_average_temperature)

class Monthly_Report:
    def __init__(self,year1,month1):
        self.year = year1
        self.month = month1
        self.formated_month = datetime(int(self.year), int(self.month), 1)
        self.selected_month = self.formated_month.strftime("%b")
        self.filname = 'Murree_weather_' + str(self.year) + '_' + self.selected_month + '.txt'
        self.max_temperature = []
        self.min_temperature = []
        self.pkt = []

    def monthly_graph(self):
        df = pd.read_csv(self.filname)
        self.max_temperature = df['Max TemperatureC']
        self.min_temperature = df['Min TemperatureC']
        self.pkt = df['PKT']
        self.formated_month = datetime(int(self.year), int(self.month), 1)
        length = np.arange(len(self.pkt))
        plt.barh(length,self.max_temperature , color = 'r')
        plt.yticks(length,self.pkt)
        plt.title(self.selected_month + " " + str(self.year))
        plt.xlabel('Temperature')
        plt.ylabel('Date')
        plt.show()

        length2 = np.arange(len(self.pkt))
        plt.barh(length2,self.min_temperature , color = 'b')
        plt.yticks(length2,self.pkt)
        plt.title(self.selected_month + " " + str(self.year))
        plt.xlabel('Temperature')
        plt.ylabel('Date')
        plt.show()

class Yearly_report:
    def __init__(self,year):
        self.year = year
        self.filename = "Murree_weather_"
        self.index_max_temperature = []
        self.index_min_temperature = []
        self.index_humidity = []
        self.read_max_temperature = []
        self.read_min_temperature = []
        self.read_humidity = []
        self.max_temperature = []
        self.min_temperature = []
        self.pkt =[]
        self.date = []
        self.date1 = []
        self.date2 =[]
        self.store_values = dict()
        self.store_values1 = dict()
        self.key = 0
        self.new_key = 0

    def yearly_graph_for_maximum(self):
        basepath1 = r"/home/ahmed/Downloads/weatherfiles/weatherfiles"
        for entry1 in os.listdir(basepath1):
            if os.path.isfile(os.path.join(basepath1,entry1)):
                if(entry1.startswith(self.filename + self.year)):
                    #print(entry1)
                    filename1 = open(entry1)
                    read = pd.read_csv(filename1)
                    self.read_max_temperature = read['Max TemperatureC'].fillna(read['Max TemperatureC'].mean())
                    self.max_temperature = max(self.read_max_temperature)
                    self.index_max_temperature = read['Max TemperatureC'].fillna(read['Max TemperatureC'].mean()).idxmax()
                    self.date = read['PKST'][self.index_max_temperature]
                    #print("Self Read Max Temperature: ",self.read_max_temperature)
            
                    self.new_key = self.key
                    self.store_values[self.new_key] = self.max_temperature
                    self.store_values1[self.new_key] = self.date
                    self.key += 1

        #print("Max Temperature: ",self.max_temperature)
        #print("Date: ",self.)
        length = np.arange(len(self.store_values1))
        plt.barh(length,self.store_values , color = 'r')
        plt.yticks(length,self.store_values1)
        plt.title("Yearly Graph")
        plt.xlabel('Temperature')
        plt.ylabel('Date')
        plt.show()

    def yearly_graph_for_minimum(self):
        basepath1 = r"/home/ahmed/Downloads/weatherfiles/weatherfiles"
        for entry1 in os.listdir(basepath1):
            if os.path.isfile(os.path.join(basepath1,entry1)):
                if(entry1.startswith(self.filename + self.year)):
                    #print(entry1)
                    filename1 = open(entry1)
                    read = pd.read_csv(filename1)
                    self.read_min_temperature = read['Min TemperatureC'].fillna(read['Min TemperatureC'].mean())
                    self.min_temperature = min(self.read_min_temperature)
                    self.index_min_temperature = read['Max TemperatureC'].fillna(read['Max TemperatureC'].mean()).idxmin()
                    self.date = read['PKT'][self.index_min_temperature]
                    #print("Self Read Max Temperature: ",self.read_max_temperature)
            
                    self.new_key = self.key
                    self.store_values[self.new_key] = self.max_temperature
                    self.store_values1[self.new_key] = self.date
                    self.key += 1

       
        length = np.arange(len(self.store_values1))
        plt.barh(length,self.store_values , color = 'b')
        plt.yticks(length,self.store_values1)
        plt.title("Yearly Graph")
        plt.xlabel('Temperature')
        plt.ylabel('Date')
        plt.show()
        



class Year:
    def __init__(self,year):
        #print("Year: ",year)
        self.year = year
        self.filename = "Murree_weather_"
        self.index_max_temperature = []
        self.index_min_temperature = []
        self.index_humidity = []
        self.read_max_temperature = []
        self.read_min_temperature = []
        self.read_humidity = []
        self.max_temperature = []
        self.min_temperature = []
        self.humidity =[]
        self.date = []
        self.date1 = []
        self.date2 =[]
        self.store_values = dict()
        self.store_values1 = dict()
        self.store_values2 = dict()
        self.store_values3 = dict()
        self.store_values4 = dict()
        self.store_values5 = dict()
        self.key = 0
        self.new_key = 0
        self.key1 = 0
        self.new_key1 = 0
        self.key2 = 0
        self.new_key2 = 0



    


    def Maximum_Temperature(self):
        #filename = "Murree_weather_"
        #print("Self year: ",self.year)
        basepath1 = r"/home/ahmed/Downloads/weatherfiles/weatherfiles"
        for entry1 in os.listdir(basepath1):
            if os.path.isfile(os.path.join(basepath1,entry1)):
                if(entry1.startswith(self.filename + self.year)):
                    #print(entry1)
                    filename1 = open(entry1)
                    read = pd.read_csv(filename1)
                    self.read_max_temperature = read['Max TemperatureC'].fillna(read['Max TemperatureC'].mean())
                    self.max_temperature = max(self.read_max_temperature)
                    self.index_max_temperature = read['Max TemperatureC'].fillna(read['Max TemperatureC'].mean()).idxmax()
                    self.date = read['PKT'][self.index_max_temperature]
                    #print("Self Read Max Temperature: ",self.read_max_temperature)
            
                    self.new_key = self.key
                    self.store_values[self.new_key] = self.max_temperature
                    self.store_values1[self.new_key] = self.date
                    self.key += 1          
                    #print("Max Temperature: ",self.max_temperature)
                    #print("Index of Max Temperature is: ",self.index_max_temperature)
                    #print("Index date: ",self.date)
                    #print("Store Values: ",self.store_values)
            
                    #print(self.read_max_temperature , self.read_min_temperature,self.read_humidity)
                    #print(read)

        #print("Temperature Values: ",self.store_values.values())
        #print("Date Values: ",self.store_values1.values())
        store_values2 = []
        store_values2 = list(max(common_entries(self.store_values, self.store_values1),key=lambda item:item[1]))
        print("Maximum Temperature: ",store_values2)


    def Minimum_Temperature(self):
        #filename = "Murree_weather_"
        #print("Self year: ",self.year)
        basepath1 = r"/home/ahmed/Downloads/weatherfiles/weatherfiles"
        for entry1 in os.listdir(basepath1):
            if os.path.isfile(os.path.join(basepath1,entry1)):
                if(entry1.startswith(self.filename + self.year)):
                    #print(entry1)
                    filename1 = open(entry1)
                    read = pd.read_csv(filename1)
                    self.read_min_temperature = read['Min TemperatureC']
                    self.min_temperature = min(self.read_min_temperature)
                    self.index_min_temperature = read['Max TemperatureC'].fillna(read['Max TemperatureC'].mean()).idxmin()
                    self.date1 = read['PKT'][self.index_min_temperature]
                    #print("Self Read Max Temperature: ",self.read_max_temperature)
            
                    self.new_key1 = self.key1
                    self.store_values2[self.new_key1] = self.min_temperature
                    self.store_values3[self.new_key1] = self.date1
                    self.key1 += 1          
                    #print("Max Temperature: ",self.max_temperature)
                    #print("Index of Max Temperature is: ",self.index_max_temperature)
                    #print("Index date: ",self.date)
                    #print("Store Values: ",self.store_values)
            
                    #print(self.read_max_temperature , self.read_min_temperature,self.read_humidity)
                    #print(read)

        #print("Temperature Values: ",self.store_values.values())
        #print("Date Values: ",self.store_values1.values())
        store_values3 = []
        store_values3 = list(min(common_entries(self.store_values2, self.store_values3),key=lambda item:item[1]))
        print("Minimum Temperature: ",store_values3)
    def Humidity(self):
        #filename = "Murree_weather_"
        #print("Self year: ",self.year)
        basepath1 = r"/home/ahmed/Downloads/weatherfiles/weatherfiles"
        for entry1 in os.listdir(basepath1):
            if os.path.isfile(os.path.join(basepath1,entry1)):
                if(entry1.startswith(self.filename + self.year)):
                    #print(entry1)
                    filename1 = open(entry1)
                    read = pd.read_csv(filename1)
                    self.read_humidity = read['Max Humidity']
                    self.humidity = max(self.read_humidity)
                    self.index_humidity = read['Max Humidity'].fillna(read['Max Humidity'].mean()).idxmax()
                    self.date2 = read['PKT'][self.index_humidity]
                    #print("Self Read Max Temperature: ",self.read_max_temperature)
            
                    self.new_key2 = self.key2
                    self.store_values4[self.new_key2] = self.humidity
                    self.store_values5[self.new_key2] = self.date2
                    self.key2 += 1          
                    
        store_values4 = []
        store_values4 = list(min(common_entries(self.store_values4, self.store_values5),key=lambda item:item[1]))
        print("Minimum Temperature: ",store_values4)

    




def main():
    print("1 For Monthly and Yearly Calculations of Temperature and Humidity: ")
    print("2 for Monthly and Multiple Reports  show by Graph")
    print("3 Bonus task")
    option = input("Enter operation that you want to do: ")
    print("option Slected: ",option)
    #length_of_arguments = len(sys.argv) - 1
    string_argv =sys.argv
    if option == '1':
        print("option 1")
        for i in string_argv:
            if(not(i.endswith("py"))):
                #print("Arg: ", i)
                values = i.split("/")
                #print("Length of list: " , len(values))
                if(len(values) > 1):
                    # Month and Year
                    year = values[0]
                    month = values[1]
                    #print("Year: " + year + " Month: " + month)
                    months = Month_Year(year,month)
                    months.Maximum_Average()
                    months.Minimum_Average()
                    months.Mean_Humidity()

                else:
                    # Year
                    years = values[0]
                    #print("Year: " + years)
                    obj = Year (years)
                    obj.Maximum_Temperature()
                    obj.Minimum_Temperature()
                    obj.Humidity()

    elif option == '2':
        print("option 2")
        for i in string_argv:
            if(not(i.endswith("py"))):
                #print("Arg: ", i)
                values = i.split("/")
                #print("Length of list: " , len(values))
                if(len(values) > 1):
                    # Month and Year
                    year = values[0]
                    month = values[1]
                    #print("Year: " + year + " Month: " + month)
                    monthly = Monthly_Report (year,month)
                    monthly.monthly_graph() 
                    

                else:
                    # Year
                    years = values[0]
                    yearly_report = Yearly_report (years)
                    yearly_report.yearly_graph_for_maximum()
                    yearly_report.yearly_graph_for_minimum()
                    #print("Year: " + years)

    elif option == '3':
        for i in string_argv:
            if(not(i.endswith("py"))):
                values = i.split("/")
                if(len(values) > 1):
                    # Month and Year
                    year = values[0]
                    month = values[1]

                    bonus = Bonus (year,month)
                    bonus.graph()



    else:
        print("Enter Valid Inputs")



if __name__ == '__main__':
    main()