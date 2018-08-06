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

file_name_list = []
file_data_list = []
month_highest_temp = []
date_highest_temp = []
month_lowest_temp = []
date_lowest_temp = []
month_mosthumid_val = []
date_most_humid = []

count = 0

count = 0



# print ('Number of arguments:', len(sys.argv), 'arguments.')
# print ('Argument List:', str(sys.argv))

# print(sys.argv[3])
year_input = sys.argv[3]

path_to_dir = sys.argv[1]
# print(path_to_dir)

# if sys.argv[2]=='-e':
    # print('yearly report')

# year_input = input("enter year")
# print(year_input)
# year_converted = str(year_input)
year_converted = year_input

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
years = ['2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012',
         '2013', '2014', '2015', '2016']
month_count = 0

for total_years in range(1):
    for total_months in range(11):
        file_name = "Murree_weather_" + year_converted + "_" + months[total_months] + ".txt"
        # print(file_name)
        path1 = '/home/zaid/homespace/weatherfiles/' + file_name
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

# print(max(h_temp))
# print(h_temp_index) 


# stored_object = month_list_tmp[1]
# print(a_list[1])
# stored_object.view_month_value()
# data = '2004-8-1,23,,22,18,18,18,68,68,68,,,,10.0,10.0,10.0,6,6,,0.0,,,-1'
# storage = []
# storage2 = []
# data1 = ''
# for i in range(1):
#         pro_data = data.split(',',8)
#         storage.append(pro_data)
#         print(pro_data)
#         data1 = pro_data[0]
#         # print(pro_data[0])
#         # print(pro_data[1])
#         print('date :',pro_data[0])
#         print('max_temp :',pro_data[1])
#         print('min_temp :',pro_data[3])
#         print('humidity :',pro_data[7])

#spliting date
# for i in range(1):
#     date_data = data1.split('-')
#     print(date_data)
