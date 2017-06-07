
import sys
import os
from termcolor import colored, cprint

labels = ['-e', '-a', '-c', '-b']
Year_Range = [1996, 2011]
Months = {
'Jan':'January',
 'Feb': 'February',
 'Mar':'March',
 'Apr':'April',
 'May':'May',
 'Jun':'June',
 'Jul':'July',
 'Aug':'August',
 'Sep':'September',
 'Oct':'October',
 'Nov':'November',
 'Dec':'December'
  }
Num_to_month = {
'1':'Jan',
'2':'Feb',
'3':'Mar',
'4':'Apr',
'5':'May',
'6':'Jun',
'7':'Jul',
'8':'Aug',
'9':'Sep',
'10':'Oct',
'11':'Nov',
'12':'Dec'
}


class ExtremeWeatherReport(object):
    def __init__(self):
        self.highest_temp_val = -999
        self.highest_temp_day = 'none'
        self.lowest_temp_val = 999
        self.lowest_temp_day = 'none'
        self.humidity_val = -999
        self.humidity_day = 'none'

def display_extreme_report(myreport):
    print('Highest: ' + str(myreport.highest_temp_val) + 'C on '
        + myreport.highest_temp_day)
    print('Lowest: ' + str(myreport.lowest_temp_val) + 'C on '
        + myreport.lowest_temp_day)
    print('Humid: ' + str(myreport.humidity_val) + '% on '
        + myreport.humidity_day)


def make_extreme_report(files_list,filepath):
    myreport = ExtremeWeatherReport()
    count = 0
    for temp_file in files_list:
        data_file = open(filepath + '/' + temp_file,'r')

        temp_a = temp_file.split('_')
        month_name = temp_a[3][0:3]
        month_name = Months[month_name]

        lines  = data_file.readlines()
        for x in lines:
            elements  = x.split(',')
            count = count + 1
            if count >= 3  and len(elements) > 1:
                date = str(count - 2)
                maxtemp = elements[1]
                if maxtemp != '' and int(maxtemp) > myreport.highest_temp_val:
                    myreport.highest_temp_val = int(maxtemp)
                    myreport.highest_temp_day = month_name + ' ' + date
                mintemp = elements[3]
                if mintemp != '' and int(mintemp) < myreport.lowest_temp_val:
                    myreport.lowest_temp_val = int(mintemp)
                    myreport.lowest_temp_day = month_name + ' ' + date
                maxhumid = elements[7]
                if maxhumid != '' and int(maxhumid) > myreport.humidity_val:
                    myreport.humidity_val = int(maxhumid)
                    myreport.humidity_day = month_name + ' ' + date
        count = 0
    return myreport

def extreme_weathers(year,filepath):
    if len(year) != 4:
        print('invalid year')
        exit()
    elif int(year) not in list(range(Year_Range[0], Year_Range[1] + 1)):
        print('invalid year')
        exit()

    list_all_files = os.listdir(filepath)
    list_required_files = []
    for files in list_all_files:
        if year in files:
            list_required_files.append(files)
    myreport = make_extreme_report(list_required_files,filepath)
    display_extreme_report(myreport)

class AverageWeatherReport(object):
    def __init__(self):
        self.avg_highest_temp = []
        self.avg_lowest_temp = []
        self.avg_humidity = []

def display_average_report(myreport):
    print('Highest Average: ' + str(myreport.avg_highest_temp) + 'C')
    print('Lowest Average: ' + str(myreport.avg_lowest_temp) + 'C')
    print('Average Humidity: ' + str(myreport.avg_humidity) + '%')



def make_average_report(filename, filepath):
    myreport = AverageWeatherReport()
    count = 0
    data_file = open(filepath + '/' + filename,'r')
    lines  = data_file.readlines()
    for x in lines:
        elements  = x.split(',')
        count = count + 1
        if count >= 3  and len(elements) > 1:
            maxtemp = elements[1]
            if maxtemp != '':
                myreport.avg_highest_temp.append(int(maxtemp))
            mintemp = elements[3]
            if mintemp != '':
                myreport.avg_lowest_temp.append(int(mintemp))
            maxhumid = elements[7]
            if maxhumid != '':
                myreport.avg_humidity.append(int(maxhumid))
    vals = myreport.avg_highest_temp
    myreport.avg_highest_temp = reduce(lambda x, y: x + y, vals) / len(vals)

    vals = myreport.avg_lowest_temp
    myreport.avg_lowest_temp = reduce(lambda x, y: x + y, vals) / len(vals)

    vals = myreport.avg_humidity
    myreport.avg_humidity = reduce(lambda x, y: x + y, vals) / len(vals)
    return myreport



def check_year_month(year,month):
    if len(year) != 4:
        print('invalid year format')
        exit()
    elif int(year) not in list(range(Year_Range[0], Year_Range[1] + 1)):
        print('invalid year')
        exit()
    elif len(month) > 2:
        print('invalid month format')
        exit()
    if len(month) == 2 and int(month) < 10:
        month = month[1:]
    if int(month) not in list(range(1, 13)):
        print('invalid month')
        exit()

def average_weathers(year_month,filepath):
    temp_list = year_month.split('/')
    year = temp_list[0]
    month = temp_list[1]
    check_year_month(year,month)
    if len(month) == 2 and int(month) < 10:
        month = month[1:]
    english_month = Num_to_month[month]

    list_all_files = os.listdir(filepath)
    list_required_files = []
    for files in list_all_files:
        if year in files:
            if english_month in files:
                list_required_files.append(files)

    if not list_required_files:
        print('Data for this month is not available')
        exit()
    myreport = make_average_report(list_required_files[0],filepath)
    display_average_report(myreport)


class WeatherChartReport(object):
    def __init__(self):
        self.year = 0
        self.month = "none"
        self.highest_temp = []
        self.lowest_temp = []

def display_chart(myreport):
    print(myreport.month + ' ' + str(myreport.year))
    days = len(myreport.highest_temp)
    num = 0
    while num < days:
        x = myreport.highest_temp[num]
        temp_max = ''
        for v in range(0,x):
            temp_max = temp_max + '+'

        y = myreport.lowest_temp[num]
        temp_min = ''
        for v in range(0,y):
            temp_min = temp_min + '+'

        t1 = colored(temp_max, 'red')
        t2 = colored(temp_min, 'blue')
        num = num + 1
        date = num
        if date < 10:
            date = '0' + str(num)
        else:
            date = str(date)

        if temp_max == '':
            x = 'Data not available'
            print(date + ' ' + x)
        else:
            print(date + ' ' + t1 + ' ' + str(x) + 'C')

        if temp_min == '':
            y = 'Data not available'
            print(date + ' ' + y)
        else:
            print(date + ' ' + t2 + ' ' + str(y) + 'C')

def display_bonus_chart(myreport):
    print(myreport.month + ' ' + str(myreport.year))
    days = len(myreport.highest_temp)
    num = 0
    while num < days:
        x = myreport.highest_temp[num]
        temp_max = ''
        for v in range(0,x):
            temp_max = temp_max + '+'

        y = myreport.lowest_temp[num]
        temp_min = ''
        for v in range(0,y):
            temp_min = temp_min + '+'

        t1 = colored(temp_max, 'red')
        t2 = colored(temp_min, 'blue')
        num = num + 1
        date = num
        if date < 10:
            date = '0' + str(num)
        else:
            date = str(date)

        x = str(x) + 'C'
        y = str(y) + 'C'

        if temp_max == '':
            x = 'Data not available'
        if temp_min == '':
            y = 'Data not available'

        print(date + ' ' + t2 + t1 + ' ' + y + ' - ' + x )



def make_chart_report(filename, filepath, year):
    myreport = WeatherChartReport()
    count = 0
    data_file = open(filepath + '/' + filename,'r')

    temp_a = filename.split('_')
    month_name = temp_a[3][0:3]
    month_name = Months[month_name]

    myreport.year = year
    myreport.month = month_name

    lines  = data_file.readlines()
    for x in lines:
        elements  = x.split(',')
        count = count + 1
        if count >= 3  and len(elements) > 1:
            maxtemp = elements[1]
            if maxtemp != '':
                myreport.highest_temp.append(int(maxtemp))
            else:
                myreport.highest_temp.append(0)
            mintemp = elements[3]
            if mintemp != '':
                myreport.lowest_temp.append(int(mintemp))
            else:
                myreport.lowest_temp.append(0)
    return myreport

def weather_charts(year_month, filepath, report_label):
    temp_list = year_month.split('/')
    year = temp_list[0]
    month = temp_list[1]
    check_year_month(year,month)
    if len(month) == 2 and int(month) < 10:
        month = month[1:]
    english_month = Num_to_month[month]

    list_all_files = os.listdir(filepath)
    list_required_files = []
    for files in list_all_files:
        if year in files:
            if english_month in files:
                list_required_files.append(files)

    if not list_required_files:
        print('Data for this month is not available')
        exit()
    myreport = make_chart_report(list_required_files[0],filepath, year)
    if report_label == '-c':
        display_chart(myreport)
    elif report_label == '-b':
        display_bonus_chart(myreport)

def check_report_type(report_label):
    if report_label not in labels:
        print('invalid report label')
        exit()

def check_args(list_args):
    if len(list_args) != 4:
        print('invalid number of args')
        exit()


def main():

    list_args = sys.argv
    check_args(list_args)

    report_label = list_args[1]
    year_month = list_args[2]
    file_path = list_args[3]  #check file path??

    check_report_type(report_label)

    if report_label == '-e':
        extreme_weathers(year_month,file_path)
    elif report_label == '-a':
        average_weathers(year_month,file_path)
    elif report_label == '-c' or report_label == '-b':
        weather_charts(year_month, file_path, report_label)



main()
