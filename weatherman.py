import os
from os import walk
import csv
for dirpath, dirnames, filenames in walk("/root/PycharmProjects/text project/weatherdata"):
    continue
Max_temp_value = []
Max_temp_date = []
Min_temp_value = []
Min_temp_date = []
Max_humid_value = []
Max_humid_date = []
Red = "\033[91m {}\033[00m"
Blue = "\033[34m {}\033[00m"


class MyWeather:
    def maximum_year_temp(self, file_list):         # Function To Calculate the Maximum Value
        input_file = csv.reader(open(file_list), delimiter=',')
        max_month = []
        max_days = []
        for row in input_file:
            if len(row) < 16:
                continue
            elif row[1] == "" or row[0] == "PKT":
                continue
            elif row[0] == "PKT" or row[1] == "Max TemperatureC":
                    continue
            else:
                max_days.append(row[0])
                max_month.append(int(row[1]))
        var_index = max(max_month)
        Max_temp_value.append(var_index)
        index1 = max_month.index(var_index)
        Max_temp_date.append(max_days[index1])

    def minimum_year_temp(self, file_list):         # Function To Calculate the Minimum Value
        input_file = csv.reader(open(file_list), delimiter=',')
        min_month = []
        min_days = []
        for row in input_file:
            if len(row) < 16:
                continue
            elif row[3] == "":
                continue
            elif row[0] == "PKT" or row[3] == "Min TemperatureC":
                continue
            else:
                min_days.append(row[0])
                min_month.append(int(row[3]))
        var_index = min(min_month)
        Min_temp_value.append(var_index)
        index1 = min_month.index(var_index)
        Min_temp_date.append(min_days[index1])

    def maximum_year_humidity(self, file_list):     # Function To Calculate the Maximum Humidity
        input_file = csv.reader(open(file_list), delimiter=',')
        humidity_month = []
        humidity_days = []
        for row in input_file:
            if len(row) < 16:
                continue
            elif row[7] == "":
                continue
            elif row[0] == "PKT" or row[7] == "Max Humidity":
                    continue
            else:
                humidity_days.append(row[0])
                humidity_month.append(int(row[7]))
        var_index = max(humidity_month)
        Max_humid_value.append(var_index)
        index1 = humidity_month.index(var_index)
        Max_humid_date.append(humidity_days[index1])

    def monthly_avg(self, file_list):               # Function To Calculate the Monthly Average
        input_file = csv.reader(open(file_list), delimiter=',')
        max_temp = []
        min_temp = []
        hum_avg = []
        for row in input_file:
            if len(row) < 16:
                continue
            elif row[1] == "" or row[3] == "" or row[7] == "":
                continue
            elif row[1] == "Max TemperatureC" or row[3] == "Min TemperatureC" \
                    or row[7] == "Max Humidity":
                continue
            else:
                max_temp.append(int(row[1]))
                min_temp.append(int(row[3]))
                hum_avg.append(int(row[7]))
        var_max = sum(max_temp) / len(max_temp)
        var_min = sum(min_temp) / len(min_temp)
        var_hum = sum(hum_avg) / len(hum_avg)
        print("Highest Average: ", "{0:.0f}C".format(var_max * 1))
        print("Lowest Average: ", "{0:.0f}C".format(var_min * 1))
        print("Average Humidity: ", "{0:.0f}%".format(var_hum * 1))

    def bar_chart1(self, file_list):               # Function To Draw the temperature on Chart
        input_file = csv.reader(open(file_list), delimiter=',')
        max_temp = []
        min_temp = []
        counter = 0
        star = "+"
        for row in input_file:
            if len(row) < 16:
                continue
            elif row[1] == "" or row[3] == "":
                continue
            elif row[1] == "Max TemperatureC" or row[3] == "Min TemperatureC":
                continue
            else:
                max_temp.append(int(row[1]))
                min_temp.append(int(row[3]))
                counter += 1
                maximum1 = star * int(row[1])
                minimum1 = star * int(row[3])
                print(counter, Red.format(maximum1), "{0:.0f}C".format(int(row[1]) * 1))
                print(counter, Blue.format(minimum1), "{0:.0f}C".format(int(row[3]) * 1))

    def bar_chart2(self, file_list):                  # Function To Combine the Bar Chart
        input_file = csv.reader(open(file_list), delimiter=',')
        max_temp = []
        min_temp = []
        counter = 0
        var1 = "+"
        for row in input_file:
            if len(row) < 16:
                continue
            elif row[1] == "" or row[3] == "":
                continue
            elif row[1] == "Max TemperatureC" or row[3] == "Min TemperatureC":
                continue
            else:
                max_temp.append(int(row[1]))
                min_temp.append(int(row[3]))
                counter += 1
                minimum2 = var1 * int(row[3])
                maximum2 = var1 * int(row[1])
                print(counter, Blue.format(minimum2) + Red.format(maximum2),
                      "{0:.0f}C".format(int(row[3]) * 1), "-", "{0:.0f}C".format(int(row[1]) * 1))

    def display_max_temp(self):                 # Function To Display the Maximum Temperature
        maximum = [int(i) for i in Max_temp_value]
        var_index = (max(maximum))
        max_index = maximum.index(var_index)
        print("Highest "+"{0:.0f}C".format(var_index * 1) + " on " + Max_temp_date[max_index])

    def display1_min_temp(self):                 # Function To Display the Minimum Temperature
        minimum = [int(i) for i in Min_temp_value]
        var_index = (min(minimum))
        min_index = minimum.index(var_index)
        print("Lowest " + "{0:.0f}C".format(var_index * 1) + " on " + Min_temp_date[min_index])

    def display_max_hum(self):                   # Function To Display the Highest Humidity
        humidity = [int(i) for i in Max_humid_value]
        var_index = (max(humidity))
        max_index = humidity.index(var_index)
        print("Humid " + "{0:.0f}C".format(var_index * 1) + " on " + Max_humid_date[max_index])

obj = MyWeather()                               # Class Object which i use to call the Function
loop_control = 0
while loop_control == 0:
    hold_control = raw_input("\nPress 1 for Yearly Result: \nPress 2 for Monthly Result: "
                         "\nPress 3 for Bar Chart: \nPress 4 for combine Bar Chart: \n"
                          "Press 5 to Exit the Program: ")
    try:
        if hold_control == "1":                    # First If which will call the Function for Yearly Result
            yearly = raw_input("Enter Year Between 1996 to 2011: ")
            for files in filenames:
                if yearly in files:
                    obj.maximum_year_temp(files)
                    obj.minimum_year_temp(files)
                    obj.maximum_year_humidity(files)
            obj.display_max_temp()
            obj.display1_min_temp()
            obj.display_max_hum()
        if hold_control == "2":                   # Second If which will call the Function for Monthly Result
            yearly1 = raw_input("Enter Year Between 1996 to 2011: ")
            monthly = raw_input("Enter Month with first Capital letter: ")
            for name in filenames:
                if yearly1 in name:
                    if monthly[0:3] in name:
                        obj.monthly_avg(name)
        if hold_control == "3":                  # Third If which will call the Function for Bar Chart
            yearly3 = raw_input("Enter Year Between 1996 to 2011: ")
            monthly3 = raw_input("Enter Month with first Capital letter: ")
            for name in filenames:
                if yearly3 in name:
                    if monthly3[0:3] in name:
                        obj.bar_chart1(name)

        if hold_control == "4":                 # Forth If which will call the Function for 2nd Bar Chart
            yearly4 = raw_input("Enter Year Between 1996 to 2011: ")
            monthly4 = raw_input("Enter Month with first Capital letter: ")
            for name in filenames:
                if yearly4 in name:
                    if monthly4[0:3] in name:
                        obj.bar_chart2(name)
        if hold_control == "5":
            exit()

    except Exception:
        print(Red.format("Error occurred:- Please Enter a valid input with given format"))
