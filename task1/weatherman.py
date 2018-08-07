import os
import time
from datetime import datetime
from dateutil.parser import parse
import sys
import csv

class MonthData:
    # highest_temp = []
    # lowest_temp = []
    # humidity = []
    # day = []

    def __init__(self):
        self.highest_temp = []
        self.lowest_temp = []
        self.humidity = []
        self.day = []

    def add_month_value(self, h_tmp, l_tmp, hum, dat):
        self.highest_temp.append(h_tmp)
        self.lowest_temp.append(l_tmp)
        self.humidity.append(hum)
        self.day.append(dat)

    def view_month_value(self):
        # print("date ")
        # print(self.day)
        # print("highest temp ")
        # print(self.highest_temp)
        # print("lowest temp ")
        # print(self.lowest_temp)
        # print("humidity")
        # print(self.lowest_temp)
        return 0

    def view_month_temp(self):
        # print("date ")
        # print(self.day)
        # print("highest temp ")
        # print(self.highest_temp)
        return self.highest_temp,self.lowest_temp, self.humidity , self.day


class CalculateAverages:
    
    average_highest_temp = 0
    average_lowest_temp = 0
    average_mean_humidity = 0


    def __init__(self):
        self.highest_temp = []
        self.lowest_temp = []
        self.meanhumidity = []
        
    def populate_month_data(self, max_temp, min_temp, mean_humidity):
        self.highest_temp.append(max_temp)
        self.lowest_temp.append(min_temp)
        self.meanhumidity.append(mean_humidity)

    def insert_avrg_calculations(self,average_highest_temp, average_lowest_temp, average_mean_humidity):
        self.average_highest_temp = average_highest_temp
        self.average_lowest_temp = average_lowest_temp
        self.average_mean_humidity = average_mean_humidity    

    def view_month_data(self):
        # print(self.highest_temp)    
        # print(self.lowest_temp)   
        # print(self.meanhumidity)    
        return self.highest_temp,self.lowest_temp, self.meanhumidity
    
    def view_avrg_calculations(self):
        print('Highest Average: ', self.average_highest_temp, 'C')    
        print('Lowest Average: ', self.average_lowest_temp, 'C')   
        print('Average Mean Humidity: ', self.average_mean_humidity, '%')

class CreateReports:

        def __init__(self):
            self.highest_temp = []
            self.lowest_temp = []
        
        def populate_month_data(self, max_temp, min_temp):
            self.highest_temp.append(max_temp)
            self.lowest_temp.append(min_temp)

        def view_month_value(self):
            # print("highest temp ")
            # print(self.highest_temp)
            # print("lowest temp ")
            # print(self.lowest_temp)
            return self.highest_temp, self.lowest_temp

def year_report(year_input, path_to_dir):
    file_name_list = []
    # file_data_list = []
    month_highest_temp = []
    date_highest_temp = []
    month_lowest_temp = []
    date_lowest_temp = []
    month_mosthumid_val = []
    date_most_humid = []
    date_verify = year_input.find('/')>0 
    count = 0
    if date_verify == True or int(year_input) < 2004 or int(year_input) >= 2017:
        print('Data not found')

    else:    
        year_converted = year_input

        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month_count = 0

        for total_years in range(1):
            for total_months in range(11):
                file_name = "Murree_weather_" + year_converted + "_" + months[total_months] + ".txt"
                # print(file_name)
                path1 = path_to_dir + file_name
                # print(path1)

                if os.path.isfile(path_to_dir + file_name):
                    month_count = month_count + 1
                    # print('file found')
                    file_date = open(path1, "r")
                    currentdata = file_date.read()
                    # print(file_date.read())
                    # print(currentdata)
                    # print(file_name + '\n')
                    file_name_list.append(file_name)


        # print(file_name_list)
        # print(month_count)

        month_data_objects = []

        month_data_objects = [None]*month_count
        for i in range(month_count):
            month_data_objects[i] = MonthData()

        for data_insert in range(month_count):
            count= 0
            file_get = file_name_list[data_insert]
            path2 = path_to_dir + file_get
            # print(path2)
            file_data1 = open(path2, "r")
            current_month_data = file_data1.read()
            with open(path2, 'r') as count_file:
                csv_reader = csv.reader(count_file)
                for row in csv_reader:
                    count += 1
                    # print(count)
            # print(current_month_data)
            for month_num in range(count-1):
                pro_data = current_month_data.split('\n')
                day_data = pro_data[month_num + 1]
                # print(pro_data[month_num + 1])
                for day_num in range(1):
                    day_pro_data = day_data.split(',',8)
                    # print('date :',day_pro_data[0])
                    max_tmp_val = 0
                    min_tmp_val = 0
                    most_humid_val = 0
                    date3 = ''
                    max_tmp_val = day_pro_data[1]
                    min_tmp_val = day_pro_data[3]
                    most_humid_val = day_pro_data[7]
                    date3 = day_pro_data[0]
                    month_data_objects[data_insert].add_month_value(max_tmp_val, min_tmp_val, most_humid_val, date3)
                    # print('date :', date3)
                    # print('max_temp :', max_tmp_val)
                    # print('min_temp :', min_tmp_val)
                    # print('humidity :', most_humid_val)

            # stored_object = month_list_tmp[0]
            # print('\n \n ')
            month_data_objects[data_insert].view_month_value()
            h_temp ,l_temp, m_humid, pro_date = month_data_objects[data_insert].view_month_temp()
            # print(h_temp)
            # print(l_temp)
            # print(m_humid)
            # print(pro_date)

            h_temp_val = max(h_temp)
            h_temp_index = h_temp.index(h_temp_val) 
            month_highest_temp.append(h_temp_val)
            date_highest_temp.append(pro_date[h_temp_index])

            # print('highest temp')
            # print(month_highest_temp)
            # print(date_highest_temp)

            low_tmp_get = []
            low_temp_getdate = []
            for min_tp in range(count-1):
                if l_temp[min_tp] != '':
                    low_tmp_get.append(l_temp[min_tp])
                    low_temp_getdate.append(pro_date[min_tp])


            l_temp_val = min(low_tmp_get)
            l_temp_index = low_tmp_get.index(l_temp_val) 
            month_lowest_temp.append(l_temp_val)
            date_lowest_temp.append(low_temp_getdate[l_temp_index])

            # print('lowest temp')
            # print(month_lowest_temp)
            # print(date_lowest_temp)


            humidity_val = max(m_humid)
            humidity_index = m_humid.index(humidity_val) 
            month_mosthumid_val.append(humidity_val)
            date_most_humid.append(pro_date[humidity_index])


            # print('most humid ')
            # print(month_mosthumid_val)
            # print(date_most_humid)
            # print(' \n new month ................................................')



        year_highest_temp = 0
        year_lowest_temp = 0
        year_most_humid = 0
        date_highest_tmp = ''
        date_lowest_tmp = ''
        date_mosthumid = ''


        results_high_tmp = list(map(int, month_highest_temp))

        year_highest_temp = max(results_high_tmp)
        date_highest_temp_index = results_high_tmp.index(year_highest_temp)
        date_highest_tmp = date_highest_temp[date_highest_temp_index]

        d1 = datetime.strptime(date_highest_tmp, '%Y-%m-%d')

        #print(datetime.strftime(d1,'%b %d'))

        print('Maximum: ', year_highest_temp, 'C','on ',datetime.strftime(d1,'%B %d'))

        results_low_tmp = list(map(int, month_lowest_temp))

        year_lowest_temp = min(results_low_tmp)
        date_lowest_temp_index = results_low_tmp.index(year_lowest_temp)
        date_lowest_tmp = date_lowest_temp[date_lowest_temp_index]
        d1 = datetime.strptime(date_lowest_tmp, '%Y-%m-%d')


        print('Lowest: ', year_lowest_temp , 'C', 'on ',datetime.strftime(d1,'%B %d'))

        results_humidity = list(map(int, month_mosthumid_val))

        year_most_humid = max(results_humidity)
        date__humid_index = results_humidity.index(year_most_humid)
        date_mosthumid = date_most_humid[date__humid_index]
        d1 = datetime.strptime(date_mosthumid, '%Y-%m-%d')

        print('Humidity: ', year_most_humid ,'%' , 'on ',datetime.strftime(d1,'%B %d'))


def monthly_average_report(path_to_dir,year_input): 
    split_month = year_input.split('/')
    convert_year_to_int = int(split_month[0])
    convert_month_to_int = int(split_month[1])
    if convert_year_to_int < 2004 or convert_year_to_int >= 2017:
        print('Data not found')

    else:   
        
        # print(convert_year_to_int,convert_month_to_int)
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        file_name = "Murree_weather_" + str(convert_year_to_int) + "_" + str(months[convert_month_to_int-1]) + ".txt"
        # print(file_name)
        path1 = path_to_dir + file_name
            # print(path1)
        count = 0
        if os.path.isfile(path_to_dir + file_name):
                # print('file found')
                file_date = open(path1, "r")
                currentdata = file_date.read()
                # print(file_date.read())
                # print(currentdata)

        with open(path1, 'r') as count_file:
            csv_reader = csv.reader(count_file)
            for row in csv_reader:
                count += 1 

        calculate_average_obj = CalculateAverages()

        for month_num in range(count-1):
                pro_data = currentdata.split('\n')
                day_data = pro_data[month_num + 1]
                # print(pro_data[month_num + 1])
                day_pro_data = day_data.split(',',9)
                # print(day_pro_data)
                max_tmp_val = 0
                min_tmp_val = 0
                mean_humid_val = 0
                max_tmp_val = day_pro_data[1]
                min_tmp_val = day_pro_data[3]
                mean_humid_val = day_pro_data[8]
                calculate_average_obj.populate_month_data(max_tmp_val, min_tmp_val, mean_humid_val)

        month_avrg_highest_temp = 0
        month_avrg_lowest_temp = 0
        month_avrg_mean_humid = 0
        max_temp_list, min_temp_list ,mean_humidity_list = calculate_average_obj.view_month_data()
        # print(max_temp_list)
        # print(min_temp_list)
        # print(mean_humidity_list)
        eliminate_junk_max_temp_list = []
        eliminate_junk_min_temp_list = []
        eliminate_junk_mean_humid_list = []
        count_max_temp = 0
        count_min_temp = 0
        count_mean_humid = 0

        for elements in range(len(max_temp_list)):
            if max_temp_list[elements] != '':
                eliminate_junk_max_temp_list.append(max_temp_list[elements])
                count_max_temp += 1

        
        results_high_tmp = list(map(int, eliminate_junk_max_temp_list))
        sum_max_temp = sum(results_high_tmp)
        # print(int(sum_max_temp/count_max_temp))
        month_avrg_highest_temp = int(sum_max_temp/count_max_temp)


        for elements in range(len(min_temp_list)):
            if min_temp_list[elements] != '':
                eliminate_junk_min_temp_list.append(min_temp_list[elements])
                count_min_temp += 1

        results_low_tmp = list(map(int, eliminate_junk_min_temp_list))
        sum_min_temp = sum(results_low_tmp)
        # print(int(sum_min_temp/count_min_temp))
        month_avrg_lowest_temp = int(sum_min_temp/count_min_temp)


        for elements in range(len(mean_humidity_list)):
            if mean_humidity_list[elements] != '':
                eliminate_junk_mean_humid_list.append(mean_humidity_list[elements])
                count_mean_humid += 1

        results_mean_humid = list(map(int, eliminate_junk_mean_humid_list))
        sum_mean_humid = sum(results_mean_humid)
        # print(int(sum_mean_humid/count_mean_humid))
        month_avrg_mean_humid = int(sum_mean_humid/count_mean_humid)
        calculate_average_obj.insert_avrg_calculations(month_avrg_highest_temp, month_avrg_lowest_temp,month_avrg_mean_humid)
        calculate_average_obj.view_avrg_calculations()

def monthly_graphic_report(path_to_dir,year_input):
    # print('graphic report')
    split_month = year_input.split('/')
    convert_year_to_int = int(split_month[0])
    convert_month_to_int = int(split_month[1])
    if convert_year_to_int < 2004 or convert_year_to_int >= 2017:
        print('Data not found')

    else:   
        currentdata = ''
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        file_name = "Murree_weather_" + str(convert_year_to_int) + "_" + str(months[convert_month_to_int-1]) + ".txt"
        # print(file_name)
        path1 = path_to_dir + file_name
        # print(path1)
        count = 0
        if os.path.isfile(path_to_dir + file_name):
                # print('file found')
                file_date = open(path1, "r")
                currentdata = file_date.read()
                # print(file_date.read())
                # print(currentdata)
        count = 0
        with open(path1, 'r') as count_file:
            csv_reader = csv.reader(count_file)
            for row in csv_reader:
                count += 1 

        month_report = CreateReports()
        for month_num in range(count-1):
                pro_data = currentdata.split('\n')
                day_data = pro_data[month_num + 1]
                # print(pro_data[month_num + 1])
                day_pro_data = day_data.split(',',9)
                # print(day_pro_data)
                max_tmp_val = 0
                min_tmp_val = 0
                max_tmp_val = day_pro_data[1]
                min_tmp_val = day_pro_data[3]
                month_report.populate_month_data(max_tmp_val, min_tmp_val)

        max_temp_list, min_temp_list = month_report.view_month_value()        
        d1 = datetime.strptime(year_input, '%Y/%m')
        print(datetime.strftime(d1,'%B'),split_month[0])
        for temp_value in range(len(max_temp_list)):
            if max_temp_list[temp_value] == '':
                print(temp_value+1, 'N/A')
                print(temp_value+1, 'N/A')

            else:
                convert_maxtmp_str_to_int = int(max_temp_list[temp_value])
                convert_mintmp_str_to_int = int(min_temp_list[temp_value])
                ttl_plus_max = '+'*convert_maxtmp_str_to_int
                print(temp_value+1, '\033[1;31m',ttl_plus_max, '\033[1;m', convert_maxtmp_str_to_int, 'C')
                
                ttl_plus_min = '+'*convert_mintmp_str_to_int
                print(temp_value+1,'\033[1;34m',ttl_plus_min, '\033[1;m',convert_mintmp_str_to_int, 'C')

        print('\n BONUS TASK')
        d1 = datetime.strptime(year_input, '%Y/%m')
        print(datetime.strftime(d1,'%B'),split_month[0])
        for temp_value in range(len(max_temp_list)):
            if max_temp_list[temp_value] == '':
                print(temp_value+1, 'N/A')
                print(temp_value+1, 'N/A')

            else:
                convert_maxtmp_str_to_int = int(max_temp_list[temp_value])
                convert_mintmp_str_to_int = int(min_temp_list[temp_value])
                ttl_plus_max = '+'*convert_maxtmp_str_to_int
                ttl_plus_min = '+'*convert_mintmp_str_to_int

                print(temp_value+1, '\033[1;34m',ttl_plus_min, '\033[1;m', '\033[1;31m',ttl_plus_max, '\033[1;m',
                convert_mintmp_str_to_int, 'C', '-', convert_maxtmp_str_to_int, 'C')
            

if len(sys.argv) <= 4:
    year_input = sys.argv[3]
    path_to_dir = sys.argv[1]
    if sys.argv[2]=='-e':
        year_report(year_input, path_to_dir)
    elif sys.argv[2]=='-a':
        monthly_average_report(path_to_dir, year_input)
    elif sys.argv[2]== '-c':
        monthly_graphic_report(path_to_dir, year_input)   
elif len(sys.argv) > 4 and len(sys.argv) == 6:
    year_input = sys.argv[3]
    path_to_dir = sys.argv[1]

    if sys.argv[2]=='-e':
        year_report(year_input, path_to_dir)
    elif sys.argv[2]=='-a':
        monthly_average_report(path_to_dir, year_input)
    elif sys.argv[2]== '-c':
        monthly_graphic_report(path_to_dir, year_input) 
    if sys.argv[4]=='-e':
        year_input = sys.argv[5]
        path_to_dir = sys.argv[1]
        year_report(year_input, path_to_dir)
    
    elif sys.argv[4]=='-a':
        year_input = sys.argv[5]
        path_to_dir = sys.argv[1]
        monthly_average_report(path_to_dir, year_input)

    elif sys.argv[4]=='-c':
        year_input = sys.argv[5]
        path_to_dir = sys.argv[1]
        monthly_graphic_report(path_to_dir, year_input) 

elif len(sys.argv) > 6 and len(sys.argv) == 8:
    year_input = sys.argv[3]
    path_to_dir = sys.argv[1]

    if sys.argv[2]=='-e':
        year_report(year_input, path_to_dir)
    elif sys.argv[2]=='-a':
        monthly_average_report(path_to_dir, year_input)
    elif sys.argv[2]== '-c':
        monthly_graphic_report(path_to_dir, year_input) 
    
    if sys.argv[4]=='-e':
        year_input = sys.argv[5]
        path_to_dir = sys.argv[1]
        year_report(year_input, path_to_dir)
    
    elif sys.argv[4]=='-a':
        year_input = sys.argv[5]
        path_to_dir = sys.argv[1]
        monthly_average_report(path_to_dir, year_input)

    elif sys.argv[4]=='-c':
        year_input = sys.argv[5]
        path_to_dir = sys.argv[1]
        monthly_graphic_report(path_to_dir, year_input) 

    if sys.argv[6]=='-e':
            year_input = sys.argv[7]
            path_to_dir = sys.argv[1]
            year_report(year_input, path_to_dir)
        
    elif sys.argv[6]=='-a':
        year_input = sys.argv[7]
        path_to_dir = sys.argv[1]
        monthly_average_report(path_to_dir, year_input)

    elif sys.argv[6]=='-c':
        year_input = sys.argv[7]
        path_to_dir = sys.argv[1]
        monthly_graphic_report(path_to_dir, year_input) 
    
    
else:
    print("Invalid input")

