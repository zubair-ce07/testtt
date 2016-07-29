import os
import sys
import re
import csv

Report_no = sys.argv[1]  # Type of report you want to see.
data_dir = sys.argv[2]  # Directory in which data to be processed is placed.
Report_no = int(Report_no)

os.chdir("..")
os.chdir(data_dir)
dir = os.getcwd()

#  initializing dictionary to store the data
keys = [1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011]
d = {}
# d[key][0]=Max-temp, d[key][1]=Min-temp, d[key][2]=Max-Humidity
# d[key][3]=Min-Humidity, d[key][4]=Hottest Day(Date), d[key][5]=Coolest Day(Date)
for key in keys:
    d[key] = [0, 000, 000, 000, '', '']


def is_key_present(x):
    if x in d.keys():
        return True
    else:
        return False


def is_empty(lis):
    if not lis:
        return False
    else:
        return True


def yearformat(str1):
    s = '/'
    lis1 = (re.split('-', str1))
    print(lis1)
    x = lis1[2]
    lis1[2] = lis1[0]
    lis1[0] = x
    return (s.join(lis1))


def report1():
    for filename in os.listdir(dir):
        with open(filename) as csvfile:
            Name = csvfile.name
            year = (re.split('_', Name))
            year1 = int(year[2])
            next(csvfile)
            reader = csv.DictReader(csvfile)
            mintemp_list = []
            minhum_list1 = []
            if (is_key_present(year1)) is True:
                for row in reader:
                    max_temp1 = row.get('Max TemperatureC')
                    min_temp = row.get('Min TemperatureC')
                    max_hum1 = row.get('Max Humidity')
                    min_hum = row.get(' Min Humidity')
                    if max_temp1 is None or max_temp1 == '':  # for maximum temperature
                        pass
                    else:
                        x = int(max_temp1)
                        if d[year1][0] < x:
                            d[year1][0] = x

                    if min_temp is None or min_temp is '':  # for storing 'Minimum Temperature' key values in mintemp_list
                        pass
                    else:
                        mintemp_list.append(min_temp)

                    if max_hum1 is None or max_hum1 == '':  # for maximum humidity
                        pass
                    else:
                        x = int(max_hum1)
                        if d[year1][2] < x:
                            d[year1][2] = x

                    if min_hum is None or min_hum is '':  # for storing 'Minimum Humidity' key values in minhum_list
                        pass
                    else:
                        minhum_list1.append(min_hum)

            if is_empty(mintemp_list) is False:
                pass
            else:
                min1 = min(mintemp_list)
                x = int(min1)

            if d[year1][1] == 0:
                d[year1][1] = x
            else:
                if d[year1][1] > x:
                    d[year1][1] = x

            if is_empty(minhum_list1) is False:
                pass
            else:
                min1 = min(minhum_list1)
                x = int(min1)

            if d[year1][3] == 0:
                d[year1][3] = x
            else:
                if d[year1][3] > x:
                    d[year1][3] = x

    print("This is report# 1")
    print(
        "Year" + "  " + "Maximum Temprature " + "  " + "Minimum Temprature" + "   " + "Maximum Humidity" + "   " + "Minimum Humidity")
    print("-----------------------------------------------------------------------------------")

    for key in d:
        print(key, "          ", d.get(key)[0], "                ", d.get(key)[1], "              ", d.get(key)[2],
              "               ", d.get(key)[3])


def report2():  # It will report the Hottest day of each year
    for filename in os.listdir(dir):
        with open(filename) as csvfile:
            Name = csvfile.name
            year = (re.split('_', Name))
            year1 = int(year[2])
            next(csvfile)
            reader = csv.DictReader(csvfile)
            if (is_key_present(year1)) is True:
                for row in reader:
                    max_temp1 = row.get('Max TemperatureC')
                    if max_temp1 is None or max_temp1 == '':
                        pass
                    else:
                        x = int(max_temp1)
                        if d[year1][0] < x:
                            d[year1][0] = x
    for filename in os.listdir(dir):
        with open(filename) as csvfile:
            Name = csvfile.name
            year = (re.split('_', Name))
            year1 = int(year[2])
            next(csvfile)
            reader = csv.DictReader(csvfile)
            HeaderList = reader.fieldnames
            if (is_key_present(year1)) is True:
                for row in reader:
                    max_temp1 = row.get('Max TemperatureC')
                    if max_temp1 is None or max_temp1 == '':
                        pass
                    else:
                        x = int(max_temp1)
                        if x == d[year1][0]:
                            if 'PKT' in HeaderList:
                                d[year1][4] = row.get('PKT')
                            if 'PKST' in HeaderList:
                                d[year1][4] = row.get('PKST')

    print("This is report# 2")
    print("year" + "             " + "Date" + "              " + "Temp")
    print("--------------------------------------------")
    for keys in d:
        print(keys, "          ", (d[keys][4]), "        ", d[keys][0])


def report3():  # It will report the coolest day of each year
    for filename in os.listdir(dir):
        with open(filename) as csvfile:
            Name = csvfile.name
            local_list = []
            year = (re.split('_', Name))
            year1 = int(year[2])
            next(csvfile)
            reader = csv.DictReader(csvfile)
            if (is_key_present(year1)) is True:
                for row in reader:
                    min_temp = row.get('Min TemperatureC')
                    if min_temp is None or min_temp is '':
                        pass
                    else:
                        local_list.append(min_temp)

        if is_empty(local_list) is False:
            pass
        else:
            min1 = min(local_list)
            x = int(min1)

        if d[year1][1] == 0:
            d[year1][1] = x
        else:
            if d[year1][1] > x:
                d[year1][1] = x

    for filename in os.listdir(dir):
        with open(filename) as csvfile:
            Name = csvfile.name
            year = (re.split('_', Name))
            year1 = int(year[2])
            next(csvfile)
            reader = csv.DictReader(csvfile)
            HeaderList = reader.fieldnames
            if (is_key_present(year1)) is True:
                for row in reader:
                    min_temp1 = row.get('Min TemperatureC')
                    if min_temp1 is None or min_temp1 == '':
                        pass
                    else:
                        x = int(min_temp1)
                        if x == d[year1][1]:
                            if 'PKT' in HeaderList:
                                d[year1][5] = row.get('PKT')
                            if 'PKST' in HeaderList:
                                d[year1][5] = row.get('PKST')

    print("This is report#3 showing coolest day of each year")
    print("year" + "             " + "Date" + "              " + "Temp")
    print("--------------------------------------------")
    for keys in d:
        print(keys, "          ", d[keys][5], "        ", d[keys][1])


if __name__ == '__main__':
    if Report_no == 1:
        report1()
    else:
        if Report_no == 2:
            report2()
        else:
            if Report_no == 3:
                report3()
            else:
                print("No such report found /n"
                      "select correct report number")
